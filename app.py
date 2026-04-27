from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# MODÈLE PATIENT
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    sexe = db.Column(db.String(20))
    date_naissance = db.Column(db.String(20))
    telephone = db.Column(db.String(20))
    ville = db.Column(db.String(100))
    motif = db.Column(db.String(300))
    depuis_quand = db.Column(db.String(100))
    constance = db.Column(db.String(50))
    symptomes = db.Column(db.String(300))
    douleur_intensite = db.Column(db.Integer)
    localisation_douleur = db.Column(db.String(100))
    aggravants = db.Column(db.String(200))
    soulageants = db.Column(db.String(200))
    chroniques = db.Column(db.String(300))
    maladies_passees = db.Column(db.String(300))
    hospitalisations = db.Column(db.String(300))
    chirurgies = db.Column(db.String(300))
    allergies = db.Column(db.String(300))
    medicaments = db.Column(db.String(300))
    famille = db.Column(db.String(300))
    famille_detail = db.Column(db.String(300))
    tabac = db.Column(db.String(50))
    alcool = db.Column(db.String(50))
    drogues = db.Column(db.String(50))
    sport = db.Column(db.String(50))
    alimentation = db.Column(db.String(50))
    sommeil = db.Column(db.String(50))
    autres_habitudes = db.Column(db.String(300))
    stress = db.Column(db.String(50))
    humeur = db.Column(db.String(50))
    anxiete = db.Column(db.String(50))
    psy_detail = db.Column(db.String(300))
    poids = db.Column(db.Float)
    taille = db.Column(db.Float)
    tension = db.Column(db.String(20))
    fc = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    date_enregistrement = db.Column(db.String(30))
# FONCTION STATISTIQUES
def calc_stats(data):
    data = [x for x in data if x is not None]
    if len(data) == 0:
        return {
            'moyen': 0, 'mediane': 0, 'ecart': 0,
            'q1': 0, 'q3': 0, 'min': 0, 'max': 0,
            'data': []
        }
    if len(data) == 1:
        return {
            'moyen': round(data[0], 1),
            'mediane': round(data[0], 1),
            'ecart': 0,
            'q1': round(data[0], 1),
            'q3': round(data[0], 1),
            'min': round(data[0], 1),
            'max': round(data[0], 1),
            'data': data
        }
    data_sorted = sorted(data)
    n = len(data_sorted)
    return {
        'moyen': round(statistics.mean(data), 1),
        'mediane': round(statistics.median(data), 1),
        'ecart': round(statistics.stdev(data), 1),
        'q1': round(data_sorted[n//4], 1),
        'q3': round(data_sorted[3*n//4], 1),
        'min': round(min(data), 1),
        'max': round(max(data), 1),
        'data': data
    }
# FONCTION RÉGRESSION LINÉAIRE
def calc_regression(x_data, y_data):
    points = [(x, y) for x, y in zip(x_data, y_data)
              if x is not None and y is not None]
    if len(points) < 2:
        return {'a': 0, 'b': 0, 'points': [], 'r2': 0}
    n = len(points)
    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]
    sum_x = sum(x_vals)
    sum_y = sum(y_vals)
    sum_xy = sum(x*y for x, y in points)
    sum_x2 = sum(x**2 for x in x_vals)
    denom = n * sum_x2 - sum_x ** 2
    if denom == 0:
        return {'a': 0, 'b': 0, 'points': [], 'r2': 0}
    a = round((n * sum_xy - sum_x * sum_y) / denom, 3)
    b = round((sum_y - a * sum_x) / n, 3)
    # R²
    y_mean = sum_y / n
    ss_tot = sum((y - y_mean)**2 for y in y_vals)
    ss_res = sum((y - (a*x + b))**2 for x, y in points)
    r2 = round(1 - ss_res/ss_tot, 3) if ss_tot != 0 else 0
    x_min = min(x_vals)
    x_max = max(x_vals)
    return {
        'a': a, 'b': b, 'r2': r2,
        'points': [{'x': x, 'y': y} for x, y in points],
        'line': [
            {'x': x_min, 'y': round(a*x_min + b, 1)},
            {'x': x_max, 'y': round(a*x_max + b, 1)}
        ]
    }
# ROUTES
@app.route('/')
def accueil():
    total_patients = Patient.query.count()
    return render_template('accueil.html',
        total_patients=total_patients)
@app.route('/formulaire')
def formulaire():
    return render_template('formulaire.html')
@app.route('/enregistrer', methods=['POST'])
def enregistrer():
    symptomes = ', '.join(request.form.getlist('symptomes'))
    chroniques = ', '.join(request.form.getlist('chroniques'))
    allergies = ', '.join(request.form.getlist('allergies'))
    famille = ', '.join(request.form.getlist('famille'))
    def get_float(field):
        try:
            return float(request.form.get(field))
        except:
            return None
    def get_int(field):
        try:
            return int(request.form.get(field))
        except:
            return None
    patient = Patient(
        nom=request.form.get('nom'),
        prenom=request.form.get('prenom'),
        sexe=request.form.get('sexe'),
        date_naissance=request.form.get('date_naissance'),
        telephone=request.form.get('telephone'),
        ville=request.form.get('ville'),
        motif=request.form.get('motif'),
        depuis_quand=request.form.get('depuis_quand'),
        constance=request.form.get('constance'),
        symptomes=symptomes,
        douleur_intensite=get_int('douleur_intensite'),
        localisation_douleur=request.form.get('localisation_douleur'),
        aggravants=request.form.get('aggravants'),
        soulageants=request.form.get('soulageants'),
        chroniques=chroniques,
        maladies_passees=request.form.get('maladies_passees'),
        hospitalisations=request.form.get('hospitalisations'),
        chirurgies=request.form.get('chirurgies'),
        allergies=allergies,
        medicaments=request.form.get('medicaments'),
        famille=famille,
        famille_detail=request.form.get('famille_detail'),
        tabac=request.form.get('tabac'),
        alcool=request.form.get('alcool'),
        drogues=request.form.get('drogues'),
        sport=request.form.get('sport'),
        alimentation=request.form.get('alimentation'),
        sommeil=request.form.get('sommeil'),
        autres_habitudes=request.form.get('autres_habitudes'),
        stress=request.form.get('stress'),
        humeur=request.form.get('humeur'),
        anxiete=request.form.get('anxiete'),
        psy_detail=request.form.get('psy_detail'),
        poids=get_float('poids'),
        taille=get_float('taille'),
        tension=request.form.get('tension'),
        fc=get_int('fc'),
        temperature=get_float('temperature'),
        date_enregistrement=datetime.now().strftime('%d/%m/%Y %H:%M')
    )
    db.session.add(patient)
    db.session.commit()
    return redirect('/tableau_bord')
@app.route('/tableau_bord')
def tableau_bord():
    patients = Patient.query.all()
    total = len(patients)
    return render_template('tableau_bord.html',
        patients=patients, total=total)
@app.route('/patient/<int:id>')
def voir_patient(id):
    patient = Patient.query.get_or_404(id)
    return render_template('voir_patient.html', patient=patient)
@app.route('/statistiques')
def statistiques():
    patients = Patient.query.all()
    poids = calc_stats([p.poids for p in patients])
    taille = calc_stats([p.taille for p in patients])
    fc = calc_stats([p.fc for p in patients])
    temp = calc_stats([p.temperature for p in patients])
    imc_list = []
    for p in patients:
        if p.poids and p.taille and p.taille > 0:
            imc = round(p.poids / ((p.taille/100) ** 2), 1)
            imc_list.append(imc)
    imc = calc_stats(imc_list)
    sexe_data = {}
    for p in patients:
        s = p.sexe or 'Non précisé'
        sexe_data[s] = sexe_data.get(s, 0) + 1
    # RÉGRESSION : poids vs taille
    reg_poids_taille = calc_regression(
        [p.taille for p in patients],
        [p.poids for p in patients]
    )
    # RÉGRESSION : taille vs FC
    reg_taille_fc = calc_regression(
        [p.taille for p in patients],
        [p.fc for p in patients]
    )
    stats = {
        'total': len(patients),
        'poids_moyen': poids['moyen'],
        'poids_mediane': poids['mediane'],
        'poids_ecart': poids['ecart'],
        'poids_q1': poids['q1'],
        'poids_q3': poids['q3'],
        'poids_min': poids['min'],
        'poids_max': poids['max'],
        'poids_data': poids['data'],
        'taille_moyen': taille['moyen'],
        'taille_mediane': taille['mediane'],
        'taille_ecart': taille['ecart'],
        'taille_q1': taille['q1'],
        'taille_q3': taille['q3'],
        'taille_min': taille['min'],
        'taille_max': taille['max'],
        'taille_data': taille['data'],
        'fc_moyen': fc['moyen'],
        'fc_mediane': fc['mediane'],
        'fc_ecart': fc['ecart'],
        'fc_q1': fc['q1'],
        'fc_q3': fc['q3'],
        'fc_min': fc['min'],
        'fc_max': fc['max'],
        'fc_data': fc['data'],
        'temp_moyen': temp['moyen'],
        'temp_mediane': temp['mediane'],
        'temp_ecart': temp['ecart'],
        'temp_q1': temp['q1'],
        'temp_q3': temp['q3'],
        'temp_min': temp['min'],
        'temp_max': temp['max'],
        'imc_moyen': imc['moyen'],
        'imc_mediane': imc['mediane'],
        'imc_ecart': imc['ecart'],
        'imc_q1': imc['q1'],
        'imc_q3': imc['q3'],
        'imc_min': imc['min'],
        'imc_max': imc['max'],
        'imc_data': imc_list,
        'sexe_data': sexe_data,
        'reg_poids_taille': reg_poids_taille,
        'reg_taille_fc': reg_taille_fc,
    }
    return render_template('statistiques.html', stats=stats)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)