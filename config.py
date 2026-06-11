import secrets
from  dotenv import load_dotenv
import os
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_LIFETIME = 30
REFRESH_TOKEN_LIFETIME = 4