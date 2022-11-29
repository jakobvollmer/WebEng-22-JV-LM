from flask import Flask

from api.auth.auth import validateAuth
from api.errorHandler import errorHandler

from api.reservations.getAll import getReservationsAll
from api.reservations.getById import getReservationsById

from db.postqresDB import get_PostqresDB
db = get_PostqresDB()

app = Flask(__name__)

app.register_blueprint(errorHandler)
app.register_blueprint(getReservationsAll)
app.register_blueprint(getReservationsById)

app.run(host="0.0.0.0", port=9000)