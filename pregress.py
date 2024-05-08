import time
import PyPDF2
from tkinter import ttk

def process_file(self):
    file_path = self.selected_file_label["text"]
    if file_path != "Aucun fichier sélectionné":
        # créer une barre de progression
        progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        progress.pack()

        # traiter le fichier et mettre à jour la barre de progression
        pdf_file = open(file_path, "rb")
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        total_pages = pdf_reader.getNumPages()

        for i in range(total_pages):
            page = pdf_reader.getPage(i)
            content = page.extractText()

            # traitement à faire avec le contenu de la page...

            # mise à jour de la barre de progression
            progress["value"] = int((i + 1) * 100 / total_pages)
            self.update_idletasks()

            # attendre un peu pour simuler un traitement
            time.sleep(0.1)

        pdf_file.close()

        # détruire la barre de progression
        progress.destroy()
