# simple-flask
Re-wheel the framework of Flask. It is an **http server** based on WSGI protocol and support routing. 


# how to use 

```python
from ben_flask import Tinyflask

## new an application here 
app = Tinyflask(__name__)

## application api define 
@app.rout(rule='/')
def hello_world():
    return "<h1>Hello, web!</h1>"

@app.rout(rule='/name/<username>')
def hello_world(username):
    return "<h1>Hello, {0}!</h1>".format(username)

@app.rout(rule='/info/<info>/<username>')
def hello_world(info, username):
    return "<h1>My Name is {0}, Present, {1}!</h1>".format(username, info)

```
