"""Really simple debug server for serving up debug webpages"""
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi
import threading
import urlparse

class DebugHTTPServer(object):
    
    def __init__(self, port=8080):
        self.port = port
        self.callback_dict = {}
        self._server = _MiddlewareHTTPServer(port, self.callback_dict)
    
    def add_handler(self, path, handler_fn):
        """Register a handler for the specified path"""
        self.callback_dict[path] = handler_fn
        
    def add_application(self, feature, base_path=''):
        """Applications are abstractions which group callbacks and paths"""
        for path, handler in feature.path_map.iteritems():
            full_path = '/'.join([base_path, path]).replace('//', '/')
            self.add_handler(full_path, handler)
    
    def remove_application(self, feature, base_path=''):
        """Remove the application from this debug server"""
        for path, handler in feature.path_map.iteritems():
            full_path = '/'.join([base_path, path]).replace('//', '/')
            self.remove_handler(full_path, handler)
    
    def handle_path(self, path):
        """Decorator that marks the decorated function as handler for some path
        
        Example::
            
            @debug_server.handle_path('/foo/bar')
            def foo_bar_handler(method, headers, baz='25'):
                return 'text/plain', 'Nice!'
                
        Which is really just the same as...
        
            def foo_bar_handler(method, headers, baz='25'):
                return 'text/plain', 'Nice!'
            
            debug_server.add_handler('/foo/bar/', foo_bar_handler)
        """
        def _handler_decorator(fn):
            self.add_handler(path, fn)
            return fn
        return _handler_decorator
    
    def remove_handler(self, path):
        """Remove the handler registered for the provided path"""
        del self.callback_dict[path]
    
    def start(self):
        """Start the debug server"""
        self._server.start()

    def stop(self):
        """Stop the debug server"""
        self._server.stop()
        
#===============================================================================
# The rest of this crud can be pretty safely ignored.  If you want something
# efficient, I would just implement the DebugHTTPServer interface and make
# the backend use something better than what is in the stdlib.
#===============================================================================
def _create_bound_request_handler(callback_dict):
    # Create an HTTP request handler that has access to the callback dictionary
    # it should use for mapping requests to responses
    
    class _MiddlewareRequestHandler(BaseHTTPRequestHandler):    
        """Request handler that bridges the gap, making things look like digi platform"""
        
        def do_GET(self):
            """Handle GET request"""
            # callback(method, path, headers, args)
            method = self.command
            headers = self.headers.dict
            args = {}
            url = urlparse.urlparse(self.path)
            for key, value in cgi.parse_qs(url[4]).iteritems():
                args[key] = value[0]
            path = url[2]
            
            try:
                content_type, contents = callback_dict[path](method, headers, args)
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(contents)
            except Exception: # pylint: disable-msg=W0703
                import traceback
                traceback.print_exc(file=self.wfile)
        
        def do_QUIT (self):
            """Handle QUIT"""
            self.send_response(200)
            self.end_headers()
            self.server.run = False
    
    return _MiddlewareRequestHandler

class _MiddlewareHTTPServer(HTTPServer, threading.Thread):
    """Dummy HTTP Server"""
    
    def __init__(self, port, callback_dict):
        self.port = port
        threading.Thread.__init__(self, name="Bugger Debug HTTP Server")
        HTTPServer.__init__(self, ('', self.port), _create_bound_request_handler(callback_dict))
    
    # pylint: disable-msg=E0202
    def run(self):
        """Main thread loop"""
        self.run = True
        while self.run:
            self.handle_request()
    
    def stop(self):
        """Send QUIT request to http server running on 127.0.0.1:<port>"""
        import httplib
        self.run = False
        conn = httplib.HTTPConnection("127.0.0.1:%d" % self.port)
        conn.request("QUIT", "/")
        conn.getresponse()
