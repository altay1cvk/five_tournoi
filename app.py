from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query
import os # Ajout de cette ligne
import re

# Modification : On configure Flask pour qu'il cherche les templates et les fichiers statiques
# à la racine du projet.
app = Flask(__name__, template_folder='.', static_folder='.')
db = TinyDB('inscriptions.json')

@app.route('/')
def index():
    equipes = {
        'equipe1': get_membres('equipe1'),
        'equipe2': get_membres('equipe2'),
        'equipe3': get_membres('equipe3'),
        'equipe4': get_membres('equipe4'),
    }
    return render_template('index.html', equipes=equipes)

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    equipe_courante = request.args.get('equipe', '')
    erreur = None

    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        telephone = request.form['telephone']
        age = request.form['age']
        equipe = request.form['equipe']

        if not is_valid_email(email):
            erreur = "L'adresse email n'est pas valide."
        elif not is_valid_phone(telephone):
            erreur = "Le numéro de téléphone n'est pas valide (10 chiffres requis)."
        elif not age.isdigit() or not 1 <= int(age) <= 120:
            erreur = "L'âge doit être un nombre entre 1 et 120."
        elif count_membres(equipe) >= 5:
            erreur = f"L'équipe {equipe} est complète."
        else:
            db.insert({
                'nom': nom,
                'prenom': prenom,
                'email': email,
                'telephone': telephone,
                'age': int(age),
                'equipe': equipe
            })
            return redirect(url_for('index'))

    return render_template('inscription.html', equipe=equipe_courante, erreur=erreur)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^[0-9]{10}$", phone)

def get_membres(equipe):
    Membre = Query()
    membres = db.search(Membre.equipe == equipe)
    membres += [{}] * (5 - len(membres))
    return membres

def count_membres(equipe):
    Membre = Query()
    return len(db.search(Membre.equipe == equipe))
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
