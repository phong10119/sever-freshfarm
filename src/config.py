import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SEND_FILE_MAX_AGE_DEFAULT = 0
    SECRET_KEY = "secret"
    EMAIL_API = os.environ.get('EMAIL_API')
    FACEBOOK_OAUTH_CLIENT_ID = os.environ.get("FACEBOOK_OAUTH_CLIENT_ID")
    FACEBOOK_OAUTH_CLIENT_SECRET = os.environ.get("FACEBOOK_OAUTH_CLIENT_SECRET")