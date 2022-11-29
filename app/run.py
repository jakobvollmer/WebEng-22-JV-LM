from flask import Flask

from api.auth.auth import validateAuth

app = Flask(__name__)

@app.route('/reservations/', methods = ['POST'])
@validateAuth
def index():
    return 'Web App with Python Flask! TEST'

app.run(host='0.0.0.0', port=9000)