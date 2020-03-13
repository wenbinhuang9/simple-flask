from wsgi_server import make_server
import re

class Tinyflask():
    def __init__(self, import_name):
        self.import_name = import_name
        self.ip = "0.0.0.0"
        self.port = 5050
        self.server = None
        self.view_functions ={}
        self.url_to_rule = {}

    def run(self):
        self.server = make_server((self.ip, self.port), self)
        self.server.serve_forever()

    def rout(self, rule,  **options):
        def decorator(f):
            self.add_for_url(rule, f)

        return decorator

    def add_for_url(self, url, function):
        rule = Rule(url)
        url = rule.url
        print("url={0}|rule={1}".format(url, rule))
        self.view_functions[url] = function
        self.url_to_rule[url] = rule


    def __call__(self,  environ, start_response):
        return self.run_wsgi(environ, start_response)

    def get_request(self):
        return self.server.get_local().request

    def dispatch_request(self):
        request = self.get_request()

        url = request.url

        ##execute view function
        print("dispatch_request|view_args={0}".format(request.view_args))

        return self.view_functions[url](**request.view_args)

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

        ctx = self.request_context(environ)

        self.set_request_context(ctx)

        response = self.full_request_dispatch(ctx)

        return response(environ, start_response)

class Rule():
    def __init__(self, rule, **options):
        self.rule = rule
        self.url = None
        self.method = None
        self.view_args_name = set([])
        self.parse_rule(rule)

    def parse_rule(self, rule):
        arg_pattern = "<(.+?)>"
        url_pattern = "(.*?)[<.*>].*"

        arg_list = re.findall(arg_pattern, rule)
        for arg in arg_list:
            self.view_args_name.add(arg)

        if len(self.view_args_name) == 0:
            ## no arguments in rule
            self.url = rule
        else:
            url_list = re.findall(url_pattern, rule)
            self.url = url_list[0]
        print("Rule|parse_url|url = {0}".format(self.url))

        if self.url != "/" and self.url.endswith("/"):
            self.url = self.url[:-1]
    def __str__(self):
        return "url={0}|view_args_name={1}|rule={2}".format(self.url, self.view_args_name, self.rule)


class Request():
    def __init__(self, app, environ):
        self.environ = environ
        self.app = app
        self.url = None
        self.method = None
        self.view_args = None
        self.http_arguments = None
        self.parse_environ(environ)
        self.rule = self.parse_rule()


        self.view_args = self.get_view_args(self.rule, self.http_arguments)

    def get_view_args(self, rule, http_arguments):
        view_args = {}
        print("get_view_args|rule={0}".format(rule))
        for arg_name in rule.view_args_name:
            view_args[arg_name] = http_arguments.get(arg_name)

        return view_args

    def parse_rule(self):
        print("Request|parse_rule|url={0}".format(self.url))
        rule = self.app.url_to_rule[self.url]
        return rule

    def parse_environ(self, environ):
        self.url = environ['PATH_INFO']
        self.method = environ['REQUEST_METHOD']
        self.query_string = environ['QUERY_STRING']

        self.http_arguments = self.parse_query_string(self.query_string)

    def parse_query_string(self, query_string):
        res = {}
        print(type(query_string))
        print (query_string)
        if self.query_string == None or self.query_string == '':
            return res

        key_value_list = query_string.split('&')
        for key_value in key_value_list:
            temp = key_value.split('=')
            key = temp[0].strip()
            val = temp[1].strip()
            res[key] = val

        return res

class Response():
    def __init__(self, response_body):
        self.response_body = response_body

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])

        return [self.response_body]
