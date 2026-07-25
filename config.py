import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Clé secrète pour les sessions Flask (change-la en production)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-cette-cle-en-production')

    # Base de données : SQLite par defaut (fichier gym.db), remplaçable par
    # une variable d'environnement DATABASE_URL (ex: postgresql://... ou mysql://...)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'gym.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
