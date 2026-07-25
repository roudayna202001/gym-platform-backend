"""
Script d'initialisation de la base de données avec des comptes de démonstration.
A lancer UNE FOIS avant le premier démarrage : `python seed.py`
"""
from datetime import date, time, timedelta

from app import create_app
from extensions import db
from models import User, Cours, Inscription

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # ---- Directeur ----
    directeur = User(
        nom="Ben Salah", prenom="Karim", email="directeur@gym.com",
        role="directeur", telephone="20111222"
    )
    directeur.set_password("123456")

    # ---- Coaches ----
    coach1 = User(
        nom="Trabelsi", prenom="Sami", email="coach@gym.com",
        role="coach", specialite="Musculation & Cross Training", telephone="20333444"
    )
    coach1.set_password("123456")

    coach2 = User(
        nom="Gharbi", prenom="Nour", email="coach2@gym.com",
        role="coach", specialite="Yoga & Pilates", telephone="20555666"
    )
    coach2.set_password("123456")

    # ---- Élèves ----
    eleve1 = User(
        nom="Jlassi", prenom="Ahmed", email="eleve@gym.com",
        role="eleve", telephone="20777888",
        abonnement_type="Mensuel",
        abonnement_debut=date.today(),
        abonnement_fin=date.today() + timedelta(days=30),
    )
    eleve1.set_password("123456")

    eleve2 = User(
        nom="Mansour", prenom="Yasmine", email="eleve2@gym.com",
        role="eleve", telephone="20999000",
        abonnement_type="Annuel",
        abonnement_debut=date.today(),
        abonnement_fin=date.today() + timedelta(days=365),
    )
    eleve2.set_password("123456")

    db.session.add_all([directeur, coach1, coach2, eleve1, eleve2])
    db.session.commit()

    # ---- Sessions de démo ----
    cours1 = Cours(
        nom="Cross Training", coach_id=coach1.id,
        description="Séance intense full-body",
        date_cours=date.today() + timedelta(days=1),
        heure_debut=time(9, 0), heure_fin=time(10, 0),
        capacite_max=15, salle="Salle 1",
    )
    cours2 = Cours(
        nom="Yoga Flow", coach_id=coach2.id,
        description="Séance de yoga tout niveau",
        date_cours=date.today() + timedelta(days=1),
        heure_debut=time(18, 0), heure_fin=time(19, 0),
        capacite_max=12, salle="Salle 2",
    )
    cours3 = Cours(
        nom="Musculation", coach_id=coach1.id,
        description="Renforcement musculaire",
        date_cours=date.today() + timedelta(days=2),
        heure_debut=time(17, 0), heure_fin=time(18, 0),
        capacite_max=10, salle="Salle 1",
    )

    db.session.add_all([cours1, cours2, cours3])
    db.session.commit()

    db.session.add(Inscription(eleve_id=eleve1.id, cours_id=cours1.id))
    db.session.commit()

    print("Base de données initialisée avec succès !")
    print("Comptes de démo (mot de passe : 123456) :")
    print("  - Directeur : directeur@gym.com")
    print("  - Coach     : coach@gym.com / coach2@gym.com")
    print("  - Élève     : eleve@gym.com / eleve2@gym.com")
