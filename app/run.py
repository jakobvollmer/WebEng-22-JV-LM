from flask import Flask

from api.auth.auth import validateAuth
from api.errorHandler import errorHandler

from db import postqresDB
db = postqresDB.PostqresDB()
db.connect()

app = Flask(__name__)

@app.route('/reservations/', methods = ['POST'])
@validateAuth
def index():
    return 'Web App with Python Flask! TEST'

app.register_blueprint(errorHandler)
app.run(host='0.0.0.0', port=9000)