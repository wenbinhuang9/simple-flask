from  wsgi_server import make_server
## how to deal with context variable ???
class Tinyflask():
    def __init__(self, import_name):
        self.import_name = import_name
        self.ip = "0.0.0.0"
        self.port = 5050
        self.server = None
        self.view_functions ={}

    def run(self):
        self.server = make_server((self.ip, self.port), self)
        self.server.serve_forever()
    def rout(self, rule,  **options):
        def decorator(f):
            self.add_for_url(rule, f)

        return decorator

    def add_for_url(self, url, function):
        self.view_functions[url] = function

    def __call__(self,  environ, start_response):
        return self.run_wsgi(environ, start_response)

    def get_request(self):
        return self.server.get_local().request

    def dispatch_request(self):
        request = self.get_request()

        rule = request.rule
        ##execute view function

        ## todo put arguments into function
        return self.view_functions[rule]()

    def make_response(self, response):
        return Response(response)

    def full_request_dispatch(self, ctx):

        response = self.dispatch_request()

        response = self.make_response(response)

        return response

    def request_context(self, environ):
        return Request(self, environ)

    def set_request_context(self, ctx):
        self.server.get_local().request = ctx

    def run_wsgi(self,  environ, start_response):
        ## todo deal with exception???
        ## get path? ge t function, run function ???
        #
        ctx = self.request_context(environ)

        self.set_request_context(ctx)

        ## todo what is response here ? how to deal with it ??
        response = self.full_request_dispatch(ctx)

        return response(environ, start_response)

class Request():
    def __init__(self, app, environ):
        self.environ = environ
        self.app = app
        self.rule = None
        self.method = None

        self.parse_environ(environ)

    def parse_environ(self, environ):
        self.rule = environ['PATH_INFO']
        self.method = environ['REQUEST_METHOD']

class Response():
    def __init__(self, response_body):
        self.response_body = response_body

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])

        return [self.response_body]
