import os
import glob
import os.path
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from datetime import datetime
import shutil

app = Flask(__name__)
app.secret_key = "#Drifa#"


# Chemin vers les documents PDF à classifier
pdf_dir = r'C:\Users\HP\Desktop\data'

# Dictionnaire des catégories de documents
categories = {
    'cvs': 'cv',
    'Autres': 'autre',
    'tps': 'tp',
}

# Création du pipeline de traitement de texte
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])

# Fonction pour extraire le texte d'un fichier PDF
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as f:
        pdf = PdfReader(f)
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
        return text

# Fonction pour entraîner le modèle
def train_model():
    data = []
    for category, folder in categories.items():
        folder_path = os.path.join(pdf_dir, folder)
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(file_path)
            data.append((text, category))
    train_data, test_data = train_test_split(data, test_size=0.2)
    pipeline.fit([x[0] for x in train_data], [x[1] for x in train_data])

def predict_category(file_path):
    text = extract_text_from_pdf(file_path)
    predicted_category = pipeline.predict([text])[0]
    return predicted_category

# Vérification du type de fichier
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

# Route pour afficher la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file_post():
    uploaded_files = request.files.getlist('file')
    results = []
    for file in uploaded_files:

        # Vérification que le fichier est au format PDF
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1]

        # Enregistrement du fichier et prédiction de sa catégorie
        file_path = os.path.join(pdf_dir, filename)
        file.save(file_path)
        predicted_category = predict_category(file_path)

        # Déplacement du fichier vers le dossier de la catégorie correspondante
        destination_dir = os.path.join(pdf_dir, categories[predicted_category])
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        destination_path = os.path.join(destination_dir, filename)

        # Si le fichier existe déjà dans la catégorie, le remplacer par le nouveau
        if os.path.exists(destination_path):
            shutil.move(file_path, destination_path)
        else:
            os.rename(file_path, destination_path)
        results.append((filename, predicted_category))

    return render_template('web.html', results=results)


@app.route('/classification')
def classification():
    return render_template('classification.html', categories=categories)

# Route pour afficher la catégorie prédite
@app.route('/result')
def result():
    predicted_category = request.args.get('predicted_category')
    return render_template('web.html', predicted_category=predicted_category)

@app.route('/recherche')
def recherche():
    query = request.args.get('query', '')
    results = []

    # Effectuer la recherche uniquement si une requête est fournie
    if query:
        # Parcourir le répertoire pdf_dir pour chercher des fichiers
        for dirpath, dirnames, filenames in os.walk(pdf_dir):
            for filename in filenames:
                # Vérifier que le fichier est un fichier PDF
                if filename.lower().endswith('.pdf'):
                    # Rechercher la requête dans le nom du fichier
                    if query.lower() in filename.lower():
                        # Ajouter le chemin du fichier à la liste des résultats
                        file_path = os.path.join(dirpath, filename)
                        results.append(file_path)

    if results:
        message = f"{len(results)} fichiers ont été trouvés."
    else:
        message = "Aucun fichier n'a été trouvé."

    return render_template('recherche.html', query=query, results=results, message=message)




@app.route('/apropos')
def apropos():
    return render_template('apropos.html')

@app.route('/documents')
def documents():
    files = {}
    for category, folder in categories.items():
        folder_path = os.path.join(pdf_dir, folder)
        file_list = os.listdir(folder_path)
        file_list.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
        files[category] = file_list
    return render_template('documents.html', files=files, categories=categories)


if __name__ == '__main__':
    train_model()
    app.run(debug=True)

