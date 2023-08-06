import cgi
import gc
import os
import sys
import threading
import time
from StringIO import StringIO
from types import FrameType, ModuleType

from pkg_resources import resource_filename
# 
# import Image
# import ImageDraw

from trac.core import *
from trac.web.api import IRequestHandler, HTTPNotFound, HTTPForbidden
from trac.web.chrome import ITemplateProvider, add_stylesheet, add_script

from genshi.core import Markup
from genshi.builder import tag

# from paste import fileapp
# from paste import urlparser
# from pkg_resources import resource_filename
# from webob import Request, Response
# from webob import exc

from tracdeveloper.dozer import reftree

localDir = os.path.join(os.getcwd(), os.path.dirname(__file__))

def get_repr(obj, limit=250):
    return cgi.escape(reftree.get_repr(obj, limit))

class _(object): pass
dictproxy = type(_.__dict__)

method_types = [type(tuple.__le__),                 # 'wrapper_descriptor'
                type([1].__le__),                   # 'method-wrapper'
                type(sys.getcheckinterval),         # 'builtin_function_or_method'
                type(cgi.FieldStorage.getfirst),    # 'instancemethod'
                ]

def url(req, path):
    if path.startswith('/'):
        path = path[1:]
    base_path = req.base_path
    if base_path.endswith('/'):
        return base_path + path
    else:
        return base_path + '/' + path


def template(req, name, **params):
    p = {'maincss': url(req, "/media/main.css"),
         'home': url(req, "/index"),
         }
    p.update(params)
    return open(os.path.join(localDir, 'media', name)).read() % p


class Dozer(Component):
    """Sets up a page that displays object information to help
    troubleshoot memory leaks"""
    period = 5
    maxhistory = 300
    
    implements(IRequestHandler, ITemplateProvider)
    
    def __init__(self):
        self.history = {}
        self.samples = 0
        self.runthread = threading.Thread(target=self.start)
        self.runthread.start()
    
    # IRequestHandler methods
    def match_request(self, req):
        return req.path_info.startswith('/developer/dozer')

    def process_request(self, req):
        if req.environ.get('wsgi.multiprocess'):
            raise TracError('Dozer middlewar is not usable in a multi-process environment')
        path_info = req.path_info[17:]
        if '/' in path_info:
            path_info = path_info[:path_info.find('/')]
        if not path_info:
            path_info = 'index'
        method = getattr(self, path_info, None)
        if method is None:
            raise HTTPNotFound('Nothing could be found to match %s' % path_info)
        if not getattr(method, 'exposed', False):
            raise HTTPForbidden('Access to %s is forbidden' % path_info)
        add_stylesheet(req, 'dozer/main.css')
        return method(req)
    
    # ITemplateProvider methods
    def get_htdocs_dirs(self):
        yield 'dozer', resource_filename(__name__, 'htdocs')
            
    def get_templates_dirs(self):
        self.log.debug('templates=%s', resource_filename(__name__, 'templates'))
        yield resource_filename(__name__, 'templates')
    
    # Internal methods
    def start(self):
        self.running = True
        while self.running:
            self.tick()
            time.sleep(self.period)
    
    def tick(self):
        gc.collect()
        
        typecounts = {}
        for obj in gc.get_objects():
            objtype = type(obj)
            if objtype in typecounts:
                typecounts[objtype] += 1
            else:
                typecounts[objtype] = 1
        
        for objtype, count in typecounts.iteritems():
            typename = objtype.__module__ + "." + objtype.__name__
            if typename not in self.history:
                self.history[typename] = [0] * self.samples
            self.history[typename].append(count)
        
        samples = self.samples + 1
        
        # Add dummy entries for any types which no longer exist
        for typename, hist in self.history.iteritems():
            diff = samples - len(hist)
            if diff > 0:
                hist.extend([0] * diff)
        
        # Truncate history to self.maxhistory
        if samples > self.maxhistory:
            for typename, hist in self.history.iteritems():
                hist.pop(0)
        else:
            self.samples = samples
    
    def stop(self):
        self.running = False
    
    # Subpage handlers
    def index(self, req):
        data = {}
        # floor = req.args.get('floor', 0)
        # rows = []
        # typenames = self.history.keys()
        # typenames.sort()
        # for typename in typenames:
        #     hist = self.history[typename]
        #     maxhist = max(hist)
        #     if maxhist > int(floor):
        #         row = ('<div class="typecount">%s<br />'
        #                '<img class="chart" src="%s" style="height: 20px;" /><br />'
        #                'Min: %s Cur: %s Max: %s <a href="%s">TRACE</a></div>'
        #                % (cgi.escape(typename),
        #                   req.href.developer('dozer', 'chart', typename), #url(req, "chart/%s" % typename),
        #                   min(hist), hist[-1], maxhist,
        #                   req.href.developer('dozer', 'trace', typename), #url(req, "trace/%s" % typename),
        #                   )
        #                )
        #         rows.append(row)
        #res = Response()
        #res.body = template(req, "graphs.html", output="\n".join(rows))
        #return res
        #data['output'] = Markup('\n'.join(rows))
        data['history'] = self.history
        add_script(req, 'dozer/excanvas.compiled.js')
        add_script(req, 'dozer/jspark.js')
        return 'graphs.html', data, None
    index.exposed = True
    
    # def chart(self, req):
    #     """Return a sparkline chart of the given type."""
    #     typename = req.path_info[23:]
    #     data = self.history[typename]
    #     height = 20.0
    #     scale = height / max(data)
    #     im = Image.new("RGB", (len(data), int(height)), 'white')
    #     draw = ImageDraw.Draw(im)
    #     draw.line([(i, int(height - (v * scale))) for i, v in enumerate(data)],
    #               fill="#009900")
    #     del draw
    #     
    #     f = StringIO()
    #     im.save(f, "PNG")
    #     result = f.getvalue()
    #     
    #     req.send(result, 'image/png')
    # chart.exposed = True
    
    def trace(self, req):
        typename = req.path_info[23:]
        objid = None
        if '/' in typename:
            objid = typename[typename.find('/')+1:]
            typename = typename[:typename.find('/')]
        gc.collect()
        
        if objid is None:
            rows = self.trace_all(req, typename)
        else:
            rows = self.trace_one(req, typename, objid)
        
        #res = Response()
        #res.body =template(req, "trace.html", output="\n".join(rows),
        #                typename=cgi.escape(typename),
        #                objid=str(objid or ''))
        #return res
        data = {}
        data['output'] = Markup('\n'.join(rows))
        data['typename'] = typename
        data['objid'] = str(objid or '')
        return 'trace.html', data, None
    trace.exposed = True
    
    def trace_all(self, req, typename):
        rows = []
        for obj in gc.get_objects():
            objtype = type(obj)
            if objtype.__module__ + "." + objtype.__name__ == typename:
                rows.append("<p class='obj'>%s</p>"
                            % ReferrerTree(obj, req).get_repr(obj))
        if not rows:
            rows = ["<h3>The type you requested was not found.</h3>"]
        return rows
    
    def trace_one(self, req, typename, objid):
        rows = []
        objid = int(objid)
        all_objs = gc.get_objects()
        for obj in all_objs:
            if id(obj) == objid:
                objtype = type(obj)
                if objtype.__module__ + "." + objtype.__name__ != typename:
                    rows = ["<h3>The object you requested is no longer "
                            "of the correct type.</h3>"]
                else:
                    # Attributes
                    rows.append('<div class="obj"><h3>Attributes</h3>')
                    for k in dir(obj):
                        v = getattr(obj, k)
                        if type(v) not in method_types:
                            rows.append('<p class="attr"><b>%s:</b> %s</p>' %
                                        (k, get_repr(v)))
                        del v
                    rows.append('</div>')
                    
                    # Referrers
                    rows.append('<div class="refs"><h3>Referrers (Parents)</h3>')
                    rows.append('<p class="desc"><a href="%s">Show the '
                                'entire tree</a> of reachable objects</p>'
                                % req.href.developer('dozer', 'tree', typename, objid)) #url(req, "/tree/%s/%s" % (typename, objid)))
                    tree = ReferrerTree(obj, req)
                    tree.ignore(all_objs)
                    for depth, parentid, parentrepr in tree.walk(maxdepth=1):
                        if parentid:
                            rows.append("<p class='obj'>%s</p>" % parentrepr)
                    rows.append('</div>')
                    
                    # Referents
                    rows.append('<div class="refs"><h3>Referents (Children)</h3>')
                    for child in gc.get_referents(obj):
                        rows.append("<p class='obj'>%s</p>" % tree.get_repr(child))
                    rows.append('</div>')
                break
        if not rows:
            rows = ["<h3>The object you requested was not found.</h3>"]
        return rows
    
    def tree(self, req):
        typename = req.path_info[22:]
        objid = None
        if '/' in typename:
            objid = typename[typename.find('/')+1:]
            typename = typename[:typename.find('/')]
        gc.collect()
        
        rows = []
        objid = int(objid)
        all_objs = gc.get_objects()
        for obj in all_objs:
            if id(obj) == objid:
                objtype = type(obj)
                if objtype.__module__ + "." + objtype.__name__ != typename:
                    rows = ["<h3>The object you requested is no longer "
                            "of the correct type.</h3>"]
                else:
                    rows.append('<div class="obj">')
                    
                    tree = ReferrerTree(obj, req)
                    tree.ignore(all_objs)
                    for depth, parentid, parentrepr in tree.walk(maxresults=1000):
                        rows.append(parentrepr)
                    
                    rows.append('</div>')
                break
        if not rows:
            rows = ["<h3>The object you requested was not found.</h3>"]
        
        params = {'output': Markup("\n".join(rows)),
                  'typename': typename,
                  'objid': str(objid),
                  }
        # res = Response()
        #         res.body = template(req, "tree.html", **params)
        #         return res
        return 'tree.html', params, None
    tree.exposed = True



class ReferrerTree(reftree.Tree):
    
    ignore_modules = True
    
    def _gen(self, obj, depth=0):
        if self.maxdepth and depth >= self.maxdepth:
            yield depth, 0, "---- Max depth reached ----"
            raise StopIteration
        
        if isinstance(obj, ModuleType) and self.ignore_modules:
            raise StopIteration
        
        refs = gc.get_referrers(obj)
        refiter = iter(refs)
        self.ignore(refs, refiter)
        thisfile = sys._getframe().f_code.co_filename
        for ref in refiter:
            # Exclude all frames that are from this module or reftree.
            if (isinstance(ref, FrameType)
                and ref.f_code.co_filename in (thisfile, self.filename)):
                continue
            
            # Exclude all functions and classes from this module or reftree.
            mod = getattr(ref, "__module__", "")
            if "dozer" in mod or "reftree" in mod or mod == '__main__':
                continue
            
            # Exclude all parents in our ignore list.
            if id(ref) in self._ignore:
                continue
            
            # Yield the (depth, id, repr) of our object.
            yield depth, 0, '%s<div class="branch">' % (" " * depth)
            if id(ref) in self.seen:
                yield depth, id(ref), "see %s above" % id(ref)
            else:
                self.seen[id(ref)] = None
                yield depth, id(ref), self.get_repr(ref, obj)
                
                for parent in self._gen(ref, depth + 1):
                    yield parent
            yield depth, 0, '%s</div>' % (" " * depth)
    
    def get_repr(self, obj, referent=None):
        """Return an HTML tree block describing the given object."""
        objtype = type(obj)
        typename = objtype.__module__ + "." + objtype.__name__
        prettytype = typename.replace("__builtin__.", "")
        
        name = getattr(obj, "__name__", "")
        if name:
            prettytype = "%s %r" % (prettytype, name)
        
        key = ""
        if referent:
            key = self.get_refkey(obj, referent)
        return ('<a class="objectid" href="%s">%s</a> '
                '<span class="typename">%s</span>%s<br />'
                '<span class="repr">%s</span>'
                % (self.req.href.developer('dozer', 'trace', typename, id(obj)), #url(self.req, "/trace/%s/%s" % (typename, id(obj))),
                   id(obj), prettytype, key, get_repr(obj, 100))
                )
    
    def get_refkey(self, obj, referent):
        """Return the dict key or attribute name of obj which refers to referent."""
        if isinstance(obj, dict):
            for k, v in obj.iteritems():
                if v is referent:
                    return " (via its %r key)" % k
        
        for k in dir(obj) + ['__dict__']:
            if getattr(obj, k, None) is referent:
                return " (via its %r attribute)" % k
        return ""

