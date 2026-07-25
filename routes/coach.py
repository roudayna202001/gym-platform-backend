from datetime import datetime, date

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from models import Cours, Inscription
from extensions import db
from utils import role_required

coach_bp = Blueprint('coach', __name__)


@coach_bp.before_request
@login_required
@role_required('coach')
def before_request():
    """Protège TOUTES les routes de ce blueprint : réservé au rôle 'coach'."""
    pass


@coach_bp.route('/dashboard')
def dashboard():
    mes_cours = (
        Cours.query.filter_by(coach_id=current_user.id)
        .filter(Cours.date_cours >= date.today())
        .order_by(Cours.date_cours, Cours.heure_debut)
        .all()
    )
    return render_template('coach/dashboard.html', mes_cours=mes_cours)


@coach_bp.route('/cours/ajouter', methods=['GET', 'POST'])
def ajouter_cours():
    if request.method == 'POST':
        try:
            cours = Cours(
                nom=request.form.get('nom'),
                description=request.form.get('description'),
                coach_id=current_user.id,
                date_cours=datetime.strptime(request.form.get('date_cours'), '%Y-%m-%d').date(),
                heure_debut=datetime.strptime(request.form.get('heure_debut'), '%H:%M').time(),
                heure_fin=datetime.strptime(request.form.get('heure_fin'), '%H:%M').time(),
                capacite_max=int(request.form.get('capacite_max') or 20),
                salle=request.form.get('salle'),
            )
            db.session.add(cours)
            db.session.commit()
            flash('Session créée avec succès.', 'success')
            return redirect(url_for('coach.dashboard'))
        except (ValueError, TypeError):
            flash("Merci de vérifier le format de la date et des heures.", 'danger')

    return render_template('coach/form_cours.html')


@coach_bp.route('/cours/<int:id>/eleves')
def eleves_cours(id):
    cours = Cours.query.get_or_404(id)
    if cours.coach_id != current_user.id:
        flash("Vous n'avez pas accès à cette session.", 'danger')
        return redirect(url_for('coach.dashboard'))

    inscriptions = Inscription.query.filter_by(cours_id=id).all()
    return render_template('coach/eleves_cours.html', cours=cours, inscriptions=inscriptions)


@coach_bp.route('/cours/<int:cours_id>/presence/<int:inscription_id>', methods=['POST'])
def marquer_presence(cours_id, inscription_id):
    inscription = Inscription.query.get_or_404(inscription_id)
    if inscription.cours.coach_id != current_user.id:
        flash("Action non autorisée.", 'danger')
        return redirect(url_for('coach.dashboard'))

    inscription.present = request.form.get('present') == 'true'
    db.session.commit()
    flash('Présence enregistrée.', 'success')
    return redirect(url_for('coach.eleves_cours', id=cours_id))


@coach_bp.route('/cours/<int:id>/supprimer', methods=['POST'])
def supprimer_cours(id):
    cours = Cours.query.get_or_404(id)
    if cours.coach_id == current_user.id:
        db.session.delete(cours)
        db.session.commit()
        flash('Session supprimée.', 'info')
    return redirect(url_for('coach.dashboard'))
