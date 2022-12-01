import logging, os
from const import DEFAULTS
from distutils.util import strtobool
from flask import Flask

from api.errorHandler import errorHandler
from api.reservations.reservations import reservations

from db.postqresDB import get_PostqresDB

logLevel:str = os.getenv("LOG_LEVEL", DEFAULTS.LOG_LEVEL).upper()
logFormat:str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logToConsole:bool = bool(strtobool(os.getenv("LOG_TO_CONSOLE", DEFAULTS.LOG_TO_CONSOLE)))
encoding="utf-8"

if logToConsole:
    logging.basicConfig(format=logFormat, encoding=encoding, level=logLevel)
else:
    logging.basicConfig(filename="/log/app.log", encoding=encoding, format=logFormat, level=logLevel)
logging.getLogger("werkzeug").setLevel(logLevel)

log = logging.getLogger()
log.info("Init app...")

db = get_PostqresDB()

app = Flask(__name__)
app.register_blueprint(errorHandler)
app.register_blueprint(reservations)
app.run(host="0.0.0.0", port=os.getenv("RESERVATIONS_APP_PORT", DEFAULTS.RESERVATIONS_APP_PORT))