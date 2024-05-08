import codecs

with codecs.open(r'C:\Users\Zakariae\Desktop\walo.txt', 'r', encoding='utf-8', errors='ignore') as file:
    text = file.read()

print(text)
