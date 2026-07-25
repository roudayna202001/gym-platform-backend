from flask import Flask, redirect, url_for
from flask_login import current_user

from config import Config
from extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Init des extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
    login_manager.login_message_category = 'warning'

    # Enregistrement des 3 espaces (blueprints)
    from routes.auth import auth_bp
    from routes.directeur import directeur_bp
    from routes.coach import coach_bp
    from routes.eleve import eleve_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(directeur_bp, url_prefix='/directeur')
    app.register_blueprint(coach_bp, url_prefix='/coach')
    app.register_blueprint(eleve_bp, url_prefix='/eleve')

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.role == 'directeur':
                return redirect(url_for('directeur.dashboard'))
            elif current_user.role == 'coach':
                return redirect(url_for('coach.dashboard'))
            else:
                return redirect(url_for('eleve.dashboard'))
        return redirect(url_for('auth.login'))

    @app.errorhandler(403)
    def forbidden(e):
        return "Accès refusé : vous n'avez pas les droits pour cette page.", 403

    # Crée les tables si elles n'existent pas encore
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
