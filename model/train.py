"""Treina o classificador de spam e salva em model/modelo.joblib.

Uso:
    python model/train.py                     # usa data/mensagens.csv
    python model/train.py --csv outro.csv     # CSV com colunas texto,rotulo

Para usar o SMS Spam Collection, converta-o para CSV com as colunas
`texto` e `rotulo` (valores `spam` e `nao_spam`) e passe com --csv.
"""
import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

RAIZ = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default=str(RAIZ / "data" / "mensagens.csv"))
    parser.add_argument("--saida", default=str(RAIZ / "model" / "modelo.joblib"))
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    x_tr, x_te, y_tr, y_te = train_test_split(
        df["texto"], df["rotulo"], test_size=0.25, random_state=42, stratify=df["rotulo"]
    )
    modelo = Pipeline(
        [
            ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2))),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )
    modelo.fit(x_tr, y_tr)
    print(f"Acurácia no conjunto de teste: {modelo.score(x_te, y_te):.2f}")

    # Treina novamente com todos os dados antes de salvar
    modelo.fit(df["texto"], df["rotulo"])
    joblib.dump(modelo, args.saida)
    print(f"Modelo salvo em {args.saida}")


if __name__ == "__main__":
    main()
