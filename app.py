import tkinter as tk
from tkinter import filedialog, NW
import os
import PyPDF2
import self
from PyPDF2 import PdfFileReader, PdfReader
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.background_image_tk = None
        self.select_file_img = None
        self.select_file_btn = None
        self.master = master
        self.master.geometry("600x400") # Changer la taille de la fenêtre
        self.pack()
        self.create_widgets()

        # chemin vers les documents PDF à classifier
        self.pdf_dir = r'C:\Users\Zakariae\Desktop\bro\bro2'

        # dictionnaire des catégories de documents
        self.categories = {
            'cvs': 'cv',
            'Autres': 'autre',
            'tps': 'tp'
        }

        # créer un pipeline de traitement de texte qui vectorise les données et utilise un classificateur Naive Bayes multinomial
        self.pipeline = Pipeline([
            ('vectorizer', CountVectorizer()),
            ('classifier', MultinomialNB())
        ])

        # entraîner le modèle
        self.train_model()



    def create_widgets(self):
        self.select_file_btn = tk.Button(self)
        self.select_file_btn["text"] = "Click here!"
        self.select_file_btn.configure(bd=4, relief="solid", highlightbackground="white")
        self.select_file_btn["command"] = self.select_file
        self.select_file_btn.pack(side="top")

        self.file_label = tk.Label(self, text="(Cliquez sur le bouton ci-dessus pour sélectionner un fichier PDF)")
        self.file_label.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", command=self.master.destroy, bg="#d32f2f", fg="white", bd=2,
                              relief="groove")
        self.quit.pack(side="bottom", pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            predicted_category = self.predict_category(file_path)
            tk.messagebox.showinfo("Catégorie prédite", f"La catégorie prédite pour ce fichier est: {predicted_category}")

    def extract_text_from_pdf(self, file_path):
        with open(file_path, 'rb') as f:
            pdf = PdfReader(f)
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
            return text

    def train_model(self):
        # créer un ensemble de données en extrayant le texte de chaque document PDF et en l'associant à sa catégorie
        data = []
        for category, folder in self.categories.items():
            folder_path = os.path.join(self.pdf_dir, folder)
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                text = self.extract_text_from_pdf(file_path)
                data.append((text, category))

        # séparer les données en ensemble d'entraînement et ensemble de test
        train_data, test_data = train_test_split(data, test_size=0.2)

        # entraîner le modèle
        self.pipeline.fit([x[0] for x in train_data], [x[1] for x in train_data])

    def predict_category(self, file_path):
        text = self.extract_text_from_pdf(file_path)
        predicted_category = self.pipeline.predict([text])[0]
        return predicted_category


root = tk.Tk()
app = Application(master=root)
app.mainloop()
