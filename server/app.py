from bottle import Bottle,static_file,run,request,get,post,response
import json
from translate import transform
   
@post('/translate')
def get_translate():
    req = json.load(request.body)
    text = req['text']
    transformed_text = transform(text)
    textDict = {"text":'In other words: ' + transformed_text, }
    return json.dumps(textDict)

@get('/')
def serve_index():
    return serve_static('index.html')

@get('/<path:path>')
def serve_static(path):
    return static_file(path, root='../client/build/')
 
run(host='0.0.0.0', port=8080)
