from flask import Flask

from api.auth.auth import validateAuth
from api.errorHandler import errorHandler

from api.status.getStatus import getStatus
from api.reservations.getAll import getAll

from db import postqresDB
db = postqresDB.PostqresDB()
db.connect()

app = Flask(__name__)

@app.route('/reservations/', methods = ['POST'])
@validateAuth
def index():
    return 'Web App with Python Flask! TEST'

app.register_blueprint(errorHandler)
app.register_blueprint(getAll)
app.register_blueprint(getStatus)
app.run(host='0.0.0.0', port=9000)
