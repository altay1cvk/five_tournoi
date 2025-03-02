from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('inscriptions.json')  # Crée une base de données TinyDB (fichier JSON)

@app.route('/')
def index():
    """Affiche la page d'accueil avec les équipes et les membres."""
    equipes = {
        'equipe1': get_membres('equipe1'),
        'equipe2': get_membres('equipe2'),
        'equipe3': get_membres('equipe3'),
        'equipe4': get_membres('equipe4'),
    }
    return render_template('index.html', equipes=equipes)

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    """Gère le formulaire d'inscription."""
    equipe_courante = request.args.get('equipe', '')  # Récupère l'équipe depuis l'URL
    erreur = None

    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        telephone = request.form['telephone']
        age = request.form['age']
        equipe = request.form['equipe']

        # Validation (comme en PHP)
        if not is_valid_email(email):
            erreur = "L'adresse email n'est pas valide."
        elif not is_valid_phone(telephone):
            erreur = "Le numéro de téléphone n'est pas valide (10 chiffres requis)."
        elif not age.isdigit() or not 1 <= int(age) <= 120:
            erreur = "L'âge doit être un nombre entre 1 et 120."
        elif count_membres(equipe) >= 5:
            erreur = f"L'équipe {equipe} est complète."
        else:
            # Insérer le joueur dans la base de données
            db.insert({
                'nom': nom,
                'prenom': prenom,
                'email': email,
                'telephone': telephone,
                'age': int(age),  # Convertit en entier
                'equipe': equipe
            })
            # Redirection vers la page d'accueil
            return redirect(url_for('index'))

    return render_template('inscription.html', equipe=equipe_courante, erreur=erreur)

# Fonctions utilitaires (pour la validation et l'accès à la base de données)
def is_valid_email(email):
    """Vérifie si une adresse email est valide (basique)."""
    import re
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    """Vérifie si un numéro de téléphone est valide (10 chiffres)."""
    import re
    return re.match(r"^[0-9]{10}$", phone)

def get_membres(equipe):
    """Récupère les membres d'une équipe depuis la base de données."""
    Membre = Query()
    membres = db.search(Membre.equipe == equipe)
    # Ajoute des entrées vides si l'équipe n'est pas complète
    membres += [{}] * (5 - len(membres))
    return membres

def count_membres(equipe):
    """Compte le nombre de membres d'une équipe."""
    Membre = Query()
    return len(db.search(Membre.equipe == equipe))

if __name__ == '__main__':
    app.run(debug=False, port=5000)  # Démarrage du serveur de développement (debug=True pour le débogage)