
import os
from dotenv import load_dotenv

load_dotenv()
print(os.environ.get("DATABASE_URL"))

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get(
        'SECRET_KEY',
        'change-cette-cle-en-production'
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'gym.db')
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False