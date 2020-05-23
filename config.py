import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
envfile = os.path.join(basedir, '.env')
if os.path.isfile(envfile):
    load_dotenv(envfile)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(16)
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    ADMINS = ['asterix20@yandex.ru']
    POSTS_PER_PAGE = 3
    DECATHLON_CLIENT_ID = os.environ.get('DECATHLON_CLIENT_ID')
    DECATHLON_CLIENT_SECRET = os.environ.get('DECATHLON_CLIENT_SECRET')
    DECATHLON_REDIRECT_URI = os.environ.get('DECATHLON_REDIRECT_URI')
    # DECATHLON_SCOPE = os.environ.get('DECATHLON_SCOPE')
    DECATHLON_SCOPE = 'openid profile'
    DECATHLON_AUTHORIZATION_URL = os.environ.get('DECATHLON_AUTHORIZATION_URL')
    DECATHLON_ACCESS_TOKEN_URL = os.environ.get('DECATHLON_ACCESS_TOKEN_URL')
    MONGO_URI = os.environ.get('MONGO_URI')
    SCHEDULER_API_ENABLED = True
    LOGIN_DISABLED = False
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
