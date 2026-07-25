from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Instances partagées (évite les imports circulaires entre app.py et models.py)
db = SQLAlchemy()
login_manager = LoginManager()
