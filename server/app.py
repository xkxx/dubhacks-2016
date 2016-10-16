from bottle import Bottle,static_file,run,request,get,post,response
import json
   
@post('/translate')
def get_translate():
    text = request.body.read()
    textDict = {"text":text,}
    return json.dumps(textDict)

@get('/static/:filepath')
def serve_static(filepath):
    return static_file(filepath, root='../client')

@get('/')
def serve_index():
    return serve_static('index.html')
 
run(host='0.0.0.0', port=8080)
