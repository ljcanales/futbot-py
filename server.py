from flask import Flask
from os import environ

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
	return "Not Found."

@app.route('/', methods=['GET'])
def index():
	return "Hello I'm FutBot."

app.run(host='0.0.0.0', port=environ['PORT'])