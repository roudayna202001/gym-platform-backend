from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db, login_manager


class User(db.Model, UserMixin):
    """
    Table unique pour les 3 profils (directeur / coach / eleve),
    différenciés par le champ `role`. Simple à requêter et à faire évoluer.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'directeur' | 'coach' | 'eleve'
    telephone = db.Column(db.String(20))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    actif = db.Column(db.Boolean, default=True)

    # Champs spécifiques "coach"
    specialite = db.Column(db.String(150))

    # Champs spécifiques "eleve"
    abonnement_type = db.Column(db.String(50))       # ex: Mensuel / Trimestriel / Annuel
    abonnement_debut = db.Column(db.Date)
    abonnement_fin = db.Column(db.Date)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'


class Cours(db.Model):
    """Une session / cours donné par un coach à une date et heure précises."""
    __tablename__ = 'cours'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)          # ex: "Cross Training"
    description = db.Column(db.Text)
    coach_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_cours = db.Column(db.Date, nullable=False)
    heure_debut = db.Column(db.Time, nullable=False)
    heure_fin = db.Column(db.Time, nullable=False)
    capacite_max = db.Column(db.Integer, default=20)
    salle = db.Column(db.String(100))

    coach = db.relationship('User', backref='cours_donnes')

    @property
    def nb_inscrits(self):
        return len(self.inscriptions)

    @property
    def places_restantes(self):
        return max(self.capacite_max - self.nb_inscrits, 0)


class Inscription(db.Model):
    """Réservation d'un élève à une session donnée."""
    __tablename__ = 'inscriptions'

    id = db.Column(db.Integer, primary_key=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cours_id = db.Column(db.Integer, db.ForeignKey('cours.id'), nullable=False)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    present = db.Column(db.Boolean, nullable=True)  # None = pas encore marqué

    eleve = db.relationship('User', backref='inscriptions')
    cours = db.relationship('Cours', backref='inscriptions')

    __table_args__ = (
        db.UniqueConstraint('eleve_id', 'cours_id', name='uq_eleve_cours'),
    )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
