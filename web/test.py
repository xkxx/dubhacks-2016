from bottle import Bottle,static_file,run,request,post,response
from json import dumps
app = Bottle()

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='C:\Users\littlepirlo\Desktop\web')
@app.route('\array')
def returnarray():
    
    rv = [{ "id": 1, "name": "Test Item 1" }, { "id": 2, "name": "Test Item 2" }]
    response.content_type = 'application/json'
    return json.dumps()
    
@post('/translate')
def getpost():
    text = request.body
    textDict = {"text":text,}
    return json.dumps(textDict)
    print text
run(app, host='localhost', port=8080)