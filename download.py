from flask import Flask, request, jsonify, render_template, send_file
from weasyprint import HTML
import io
import uuid

app = Flask(__name__)

# Variable globale pour stocker les données de préinscription
user_data = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    global user_data
    req = request.get_json(silent=True, force=True)
    
    # Extraire les données de la requête de Dialogflow
    parameters = req.get('queryResult', {}).get('parameters', {})
    
    # Générer un code de préinscription unique
    code_preinscription = str(uuid.uuid4())
    
    # Mettez à jour les données de préinscription avec les paramètres reçus
    user_data = {
        'code': code_preinscription,
        'nom': parameters.get('name', ''),
        'date_naissance': parameters.get('dob', ''),
        'date_precise': parameters.get('exact-date', ''),
        'lieu_naissance': parameters.get('location', ''),
        'sexe': parameters.get('sexe', ''),
        'statut_matrimonial': parameters.get('statut', ''),
        'situation_professionnelle': parameters.get('profession', ''),
        'premiere_langue': parameters.get('language', ''),
        'email': parameters.get('email', ''),
        'telephone': parameters.get('number', ''),
        'cni': parameters.get('CNI', ''),
        'adresse': parameters.get('adresse', ''),
        'date_rdv': parameters.get('ddv', ''),
        'nationalite': parameters.get('nationality', ''),
        'region_origine': parameters.get('ville-origin', ''),
        'departement_origine': parameters.get('departement-origin', ''),
        'nom_pere': parameters.get('nom-p', ''),
        'profession_pere': parameters.get('taf-p', ''),
        'nom_mere': parameters.get('nom_M', ''),
        'profession_mere': parameters.get('taf-M', ''),
        'contact_nom': parameters.get('emergency', ''),
        'contact_telephone': parameters.get('emergency-num', ''),
        'contact_ville': parameters.get('emergency-v', ''),
        'filiere': parameters.get('filiere', ''),
        'choix1': parameters.get('choix1', ''),
        'choix2': parameters.get('choix2', ''),
        'choix3': parameters.get('choix3', ''),
        'niveau': parameters.get('niveau', ''),
        'statut': parameters.get('nationality-E', ''),
        'type_diplome': parameters.get('diplome', ''),
        'moyenne': parameters.get('moyenne', ''),
        'mention': parameters.get('mention', ''),
        'diplome_delivre_par': parameters.get('exam-structure', ''),
        'date_delivrance': parameters.get('diplome-date', ''),
        'num_transaction': parameters.get('num_transaction', ''),
        'agence_paiement': parameters.get('agence', ''),
        'frais_preinscription': parameters.get('frais', ''),
        'pratique_sport': parameters.get('sport', ''),
        'pratique_art': parameters.get('art', ''),
        'num_certificat': parameters.get('num_certificat', ''),
        'lieu_certificat': parameters.get('lieu_certificat', '')
    }

    # Répondre à Dialogflow pour indiquer que le webhook a reçu les données
    return jsonify({'fulfillmentText': 'Les données ont été reçues et mises à jour.'})

@app.route('/')
def index():
    return render_template('fiche.html', user_data=user_data)

@app.route('/download_pdf')
def download_pdf():
    html = render_template('fiche.html', user_data=user_data)
    pdf = HTML(string=html).write_pdf(stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"])
    return send_file(io.BytesIO(pdf), download_name='fiche_preinscription.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
