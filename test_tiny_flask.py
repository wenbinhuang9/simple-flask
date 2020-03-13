from ben_flask import Tinyflask

app = Tinyflask(__name__)

@app.rout(rule='/')
def hello_world():
    return "<h1>Hello, web!</h1>"

@app.rout(rule='/name/<username>')
def hello_world(username):
    return "<h1>Hello, {0}!</h1>".format(username)

@app.rout(rule='/info/<info>/<username>')
def hello_world(info, username):
    return "<h1>My Name is {0}, Present, {1}!</h1>".format(username, info)

app.run()