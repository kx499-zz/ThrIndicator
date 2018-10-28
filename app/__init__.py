from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


from app import views, models

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    #acces logs
    a_logger = logging.getLogger('werkzeug')
    handler = RotatingFileHandler('tmp/access.log', 'a', 1 * 1024 * 1024, 10)
    a_logger.addHandler(handler)

    #error/app info logs
    file_handler = RotatingFileHandler('tmp/app.log', 'a', 1 * 1024 * 1024, 10)
    fmt = logging.Formatter('%(asctime)s %(module)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(fmt)
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('App startup')




