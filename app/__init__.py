from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_pymongo import PyMongo
from flask_apscheduler import APScheduler
# import logging
# from logging.handlers import SMTPHandler, RotatingFileHandler
# import os
from authlib.integrations.flask_client import OAuth


bootstrap = Bootstrap()
moment = Moment()
oauth = OAuth()
mongo = PyMongo()
scheduler = APScheduler()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    bootstrap.init_app(app)
    moment.init_app(app)
    oauth.init_app(app)
    mongo.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    with app.app_context():
        from . import models

        from .main import main_bp
        app.register_blueprint(main_bp)

        from .auth import auth_bp
        app.register_blueprint(auth_bp)

    # if not app.debug and not app.testing:
    #     if app.config['MAIL_SERVER']:
    #         auth = None
    #         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
    #             auth = (app.config['MAIL_USERNAME'],
    #                     app.config['MAIL_PASSWORD'])
    #         secure = None
    #         if app.config['MAIL_USE_TLS']:
    #             secure = ()
    #         mail_handler = SMTPHandler(
    #             mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
    #             fromaddr='no-reply@' + app.config['MAIL_SERVER'],
    #             toaddrs=app.config['ADMINS'], subject='Microblog Failure',
    #             credentials=auth, secure=secure)
    #         mail_handler.setLevel(logging.ERROR)
    #         app.logger.addHandler(mail_handler)
    #     if not os.path.exists('logs'):
    #         os.mkdir('logs')
    #     file_handler = RotatingFileHandler('logs/microblog.log',
    #                                        maxBytes=10240, backupCount=10)
    #     file_handler.setFormatter(logging.Formatter(
    #         '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    #     file_handler.setLevel(logging.INFO)
    #     app.logger.addHandler(file_handler)

    #     app.logger.setLevel(logging.INFO)
    #     app.logger.info('Microblog startup')

    return app
