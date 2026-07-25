from datetime import date

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from models import Cours, Inscription
from extensions import db
from utils import role_required

eleve_bp = Blueprint('eleve', __name__)


@eleve_bp.before_request
@login_required
@role_required('eleve')
def before_request():
    """Protège TOUTES les routes de ce blueprint : réservé au rôle 'eleve'."""
    pass


@eleve_bp.route('/dashboard')
def dashboard():
    mes_inscriptions = (
        Inscription.query.filter_by(eleve_id=current_user.id)
        .join(Cours)
        .filter(Cours.date_cours >= date.today())
        .order_by(Cours.date_cours, Cours.heure_debut)
        .all()
    )
    return render_template('eleve/dashboard.html', mes_inscriptions=mes_inscriptions)


@eleve_bp.route('/cours-disponibles')
def cours_disponibles():
    cours_list = (
        Cours.query.filter(Cours.date_cours >= date.today())
        .order_by(Cours.date_cours, Cours.heure_debut)
        .all()
    )
    mes_ids = [i.cours_id for i in Inscription.query.filter_by(eleve_id=current_user.id).all()]
    return render_template('eleve/cours_disponibles.html', cours_list=cours_list, mes_ids=mes_ids)


@eleve_bp.route('/cours/<int:id>/inscrire', methods=['POST'])
def inscrire(id):
    cours = Cours.query.get_or_404(id)
    deja_inscrit = Inscription.query.filter_by(cours_id=id, eleve_id=current_user.id).first()

    if deja_inscrit:
        flash('Vous êtes déjà inscrit à cette session.', 'warning')
    elif cours.nb_inscrits >= cours.capacite_max:
        flash('Cette session est complète.', 'danger')
    else:
        db.session.add(Inscription(eleve_id=current_user.id, cours_id=id))
        db.session.commit()
        flash('Inscription réussie !', 'success')

    return redirect(url_for('eleve.cours_disponibles'))


@eleve_bp.route('/cours/<int:id>/annuler', methods=['POST'])
def annuler(id):
    inscription = Inscription.query.filter_by(cours_id=id, eleve_id=current_user.id).first()
    if inscription:
        db.session.delete(inscription)
        db.session.commit()
        flash('Inscription annulée.', 'info')
    return redirect(url_for('eleve.dashboard'))


@eleve_bp.route('/profil')
def profil():
    return render_template('eleve/profil.html')
