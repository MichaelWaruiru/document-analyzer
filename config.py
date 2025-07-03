import os
from dotenv import load_dotenv

load_dotenv() # Load .env file

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024  # 4 MB max upload
     # Flask-Dance configs
    OAUTHLIB_INSECURE_TRANSPORT = True  # Only for local dev
    GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
