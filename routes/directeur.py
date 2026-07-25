from datetime import date

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from models import User, Cours
from extensions import db
from utils import role_required

directeur_bp = Blueprint('directeur', __name__)


@directeur_bp.before_request
@login_required
@role_required('directeur')
def before_request():
    """Protège TOUTES les routes de ce blueprint : réservé au rôle 'directeur'."""
    pass


@directeur_bp.route('/dashboard')
def dashboard():
    nb_coaches = User.query.filter_by(role='coach').count()
    nb_eleves = User.query.filter_by(role='eleve').count()
    nb_cours = Cours.query.count()
    cours_aujourdhui = Cours.query.filter_by(date_cours=date.today()).count()
    return render_template(
        'directeur/dashboard.html',
        nb_coaches=nb_coaches, nb_eleves=nb_eleves,
        nb_cours=nb_cours, cours_aujourdhui=cours_aujourdhui
    )


# ---------- Gestion des coaches ----------

@directeur_bp.route('/coaches')
def coaches():
    coaches = User.query.filter_by(role='coach').order_by(User.nom).all()
    return render_template('directeur/coaches.html', coaches=coaches)


@directeur_bp.route('/coaches/ajouter', methods=['GET', 'POST'])
def ajouter_coach():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        if User.query.filter_by(email=email).first():
            flash('Un compte existe déjà avec cet email.', 'danger')
            return redirect(url_for('directeur.ajouter_coach'))

        coach = User(
            nom=request.form.get('nom'),
            prenom=request.form.get('prenom'),
            email=email,
            telephone=request.form.get('telephone'),
            role='coach',
            specialite=request.form.get('specialite'),
        )
        coach.set_password(request.form.get('password'))
        db.session.add(coach)
        db.session.commit()
        flash('Coach ajouté avec succès.', 'success')
        return redirect(url_for('directeur.coaches'))

    return render_template('directeur/form_coach.html')


@directeur_bp.route('/coaches/<int:id>/supprimer', methods=['POST'])
def supprimer_coach(id):
    coach = User.query.get_or_404(id)
    db.session.delete(coach)
    db.session.commit()
    flash('Coach supprimé.', 'info')
    return redirect(url_for('directeur.coaches'))


# ---------- Gestion des élèves ----------

@directeur_bp.route('/eleves')
def eleves():
    eleves = User.query.filter_by(role='eleve').order_by(User.nom).all()
    return render_template('directeur/eleves.html', eleves=eleves)


@directeur_bp.route('/eleves/ajouter', methods=['GET', 'POST'])
def ajouter_eleve():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        if User.query.filter_by(email=email).first():
            flash('Un compte existe déjà avec cet email.', 'danger')
            return redirect(url_for('directeur.ajouter_eleve'))

        eleve = User(
            nom=request.form.get('nom'),
            prenom=request.form.get('prenom'),
            email=email,
            telephone=request.form.get('telephone'),
            role='eleve',
            abonnement_type=request.form.get('abonnement_type'),
        )
        eleve.set_password(request.form.get('password'))
        db.session.add(eleve)
        db.session.commit()
        flash('Élève ajouté avec succès.', 'success')
        return redirect(url_for('directeur.eleves'))

    return render_template('directeur/form_eleve.html')


@directeur_bp.route('/eleves/<int:id>/supprimer', methods=['POST'])
def supprimer_eleve(id):
    eleve = User.query.get_or_404(id)
    db.session.delete(eleve)
    db.session.commit()
    flash('Élève supprimé.', 'info')
    return redirect(url_for('directeur.eleves'))


# ---------- Vue globale des sessions ----------

@directeur_bp.route('/cours')
def cours():
    cours_list = Cours.query.order_by(Cours.date_cours, Cours.heure_debut).all()
    return render_template('directeur/cours.html', cours_list=cours_list)
