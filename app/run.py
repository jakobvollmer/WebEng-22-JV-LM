from flask import Flask
import jwt

from api.auth import auth
app = Flask(__name__)


@app.route('/reservations/', methods = ['POST'])
def index():
    auth.validateAuth()
    return 'Web App with Python Flask! TEST'

app.run(host='0.0.0.0', port=9000)