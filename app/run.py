from flask import Flask
import jwt

from api.auth import auth
app = Flask(__name__)

@app.route('/')
def index():
    return 'Web App with Python Flask!'

app.run(host='0.0.0.0', port=9000)