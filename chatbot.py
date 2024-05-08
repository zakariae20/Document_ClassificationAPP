import nltk
from nltk.chat.util import Chat, reflections

# Charger les données du fichier texte
with open(r'C:\Users\Zakariae\Desktop\chatbot.txt','r') as file:
    pairs = [line.strip().split(';') for line in file if ';' in line]

# Créer le chatbot
reflections = {
    'je': 'tu',
    'moi': 'toi',
    'mon': 'ton',
    'ton': 'mon',
    'toi': 'moi',
    'vous': 'nous',
    'nous': 'vous',
    'votre': 'notre',
    'notre': 'votre',
    'monself': 'yourself',
    'yourself': 'myself'
}

chatbot = Chat(pairs, reflections)

# Définir la fonction de chat

def chat():
    print("Bonjour, je suis un chatbot. Comment puis-je vous aider ? (tapez 'quitter' pour sortir)")
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == 'quitter':
                break
            response = chatbot.respond(user_input)
            print(response)
        except (KeyboardInterrupt, EOFError, SystemExit):
            break


# Lancer le chatbot
chat()
