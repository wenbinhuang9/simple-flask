from ben_flask import Tinyflask

app = Tinyflask(__name__)

@app.rout(rule='/')
def hello_world():
    return "<h1>Hello, web!</h1>"

environ = {"PATH_INFO" :"/", "REQUEST_METHOD": "GET"}
def start_response(a, b):
    pass
app.run()
print(app.run_wsgi(environ, start_response))