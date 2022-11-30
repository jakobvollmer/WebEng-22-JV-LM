import logging, os
from const import DEFAULTS
from distutils.util import strtobool

logLevel:str = os.getenv("LOG_LEVEL", DEFAULTS.LOG_LEVEL).upper()
logFormat:str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logToConsole:bool = bool(strtobool(os.getenv("LOG_TO_CONSOLE", DEFAULTS.LOG_TO_CONSOLE)))

if logToConsole:
    logging.basicConfig(format=logFormat, level=logLevel)
else:
    logging.basicConfig(filename="./log/app.log", format=logFormat, level=logLevel)
    
log = logging.getLogger()
log.info("Init app...")

from flask import Flask

from api.errorHandler import errorHandler
from api.reservations.getAll import getReservationsAll
from api.reservations.getById import getReservationsById

from db.postqresDB import get_PostqresDB
db = get_PostqresDB()

app = Flask(__name__)
app.register_blueprint(errorHandler)
app.register_blueprint(getReservationsAll)
app.register_blueprint(getReservationsById)
app.run(host="0.0.0.0", port=os.getenv("RESERVATIONS_APP_PORT", DEFAULTS.RESERVATIONS_APP_PORT))