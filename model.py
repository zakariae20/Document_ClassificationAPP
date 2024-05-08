# -*- coding: utf-8 -*-
import os
import PyPDF2
from PyPDF2 import PdfFileReader, PdfReader
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# chemin vers les documents PDF à classifier
pdf_dir = r'C:\Users\Zakariae\Desktop\bro\bro2'

# dictionnaire des catégories de documents
categories = {
    'cvs': 'cv',
    'Autres': 'autre',
    'tps': 'tp'
}

# fonction pour extraire le texte d'un document PDF
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as f:
        pdf = PdfReader(f)
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
        return text



# créer un ensemble de données en extrayant le texte de chaque document PDF et en l'associant à sa catégorie
data = []
for category, folder in categories.items():
    folder_path = os.path.join(pdf_dir, folder)
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        text = extract_text_from_pdf(file_path)
        data.append((text, category))

# séparer les données en ensemble d'entraînement et ensemble de test
from sklearn.model_selection import train_test_split
train_data, test_data = train_test_split(data, test_size=0.2)

# créer un pipeline de traitement de texte qui vectorise les données et utilise un classificateur Naive Bayes multinomial
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])

# entraîner le modèle
pipeline.fit([x[0] for x in train_data], [x[1] for x in train_data])

# évaluer le modèle sur l'ensemble de test
from sklearn.metrics import accuracy_score
predictions = pipeline.predict([x[0] for x in test_data])
true_categories = [x[1] for x in test_data]
accuracy = accuracy_score(true_categories, predictions)
print('Accuracy:', accuracy)

# utiliser le modèle pour classer de nouveaux documents
new_pdf_path = r'C:\Users\Zakariae\Desktop\ziko.pdf'
new_text = extract_text_from_pdf(new_pdf_path)
predicted_category = pipeline.predict([new_text])[0]
print('Predicted category:', predicted_category)
