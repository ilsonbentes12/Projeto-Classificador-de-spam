"""Esqueleto da API de classificação de spam.

Complete os pontos marcados com TODO. O contrato da API está no README.md.
Para rodar:  uvicorn app.main:app --reload
"""
import os
from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# --- Configuração (vem de variáveis de ambiente, nunca escrita no código) ---
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1")
MODEL_PATH = Path(
    os.getenv("MODEL_PATH", str(Path(__file__).resolve().parent.parent / "model" / "modelo.joblib"))
)
# TODO: ler APP_ENV e API_KEY e decidir como proteger o /predict (veja o README)

# --- Modelo: carregado uma vez, quando a API inicia ---
modelo = joblib.load(MODEL_PATH)

app = FastAPI(title="API de classificação de spam")


class Mensagem(BaseModel):
    texto: str = Field(min_length=1, max_length=2000)


@app.get("/health")
def health():
    # TODO: devolver {"status": "ok", "versao": ..., "ambiente": ...}
    raise HTTPException(status_code=501, detail="não implementado")


@app.post("/predict")
def predict(msg: Mensagem):
    # TODO: usar o modelo (veja model/exemplo_uso.py) e devolver
    #       {"rotulo": ..., "probabilidade": ..., "versao": ...}
    raise HTTPException(status_code=501, detail="não implementado")


# TODO (para a página web): decidir como a página vai chamar a API
#   - página servida pela própria API, ou
#   - página em outro serviço (neste caso, pesquise sobre CORS)
