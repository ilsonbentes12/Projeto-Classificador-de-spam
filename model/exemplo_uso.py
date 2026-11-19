"""Exemplo mínimo de uso do modelo. Rode na raiz do projeto: python model/exemplo_uso.py"""
import joblib

modelo = joblib.load("model/modelo.joblib")

mensagens = [
    "Parabéns! Você ganhou um prêmio, clique no link para resgatar agora",
    "A reunião de amanhã foi adiada para quinta",
]

for texto in mensagens:
    probabilidades = modelo.predict_proba([texto])[0]  # uma probabilidade por classe
    indice = probabilidades.argmax()  # classe mais provável
    rotulo = modelo.classes_[indice]  # "spam" ou "nao_spam"
    print(f"{rotulo} ({probabilidades[indice]:.2f}): {texto}")
