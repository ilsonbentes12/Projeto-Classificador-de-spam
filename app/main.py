"""Esqueleto da API de classificação de spam.

Complete os pontos marcados com TODO. O contrato da API está no README.md.
Para rodar:  uvicorn app.main:app --reload
"""
import os
import hmac
import logging
from threading import Lock
from time import perf_counter
from pathlib import Path

import joblib
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# --- Configuração (vem de variáveis de ambiente, nunca escrita no código) ---
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1")
APP_ENV = os.getenv("APP_ENV", "dev")
API_KEY = os.getenv("API_KEY")
MODEL_PATH = Path(
    os.getenv("MODEL_PATH", str(Path(__file__).resolve().parent.parent / "model" / "modelo.joblib"))
)

# --- Modelo: carregado uma vez, quando a API inicia ---
modelo = joblib.load(MODEL_PATH)

app = FastAPI(title="API de classificação de spam")
logger = logging.getLogger(__name__)
metrics_lock = Lock()
metrics = {"requests": 0, "errors_5xx": 0, "latency_total_ms": 0.0}


class Mensagem(BaseModel):
    texto: str = Field(min_length=1, max_length=2000)


@app.get("/health")
def health():
    return {"status": "ok", "versao": MODEL_VERSION, "ambiente": APP_ENV}


@app.post("/predict")
def predict(msg: Mensagem, x_api_key: str | None = Header(default=None)):
    if API_KEY and (x_api_key is None or not hmac.compare_digest(x_api_key, API_KEY)):
        raise HTTPException(status_code=401, detail="Chave de API inválida ou ausente")
    if not msg.texto.strip():
        raise HTTPException(status_code=422, detail="O texto não pode ficar vazio")

    started_at = perf_counter()
    latency_ms = 0.0
    try:
        probabilities = modelo.predict_proba([msg.texto])[0]
        index = probabilities.argmax()
        label = str(modelo.classes_[index])
        probability = float(probabilities[index])
        latency_ms = round((perf_counter() - started_at) * 1000, 2)
    except Exception as exc:
        logger.exception("Falha ao classificar mensagem")
        with metrics_lock:
            metrics["requests"] += 1
            metrics["errors_5xx"] += 1
            metrics["latency_total_ms"] += latency_ms
        raise HTTPException(status_code=500, detail="Falha ao classificar mensagem") from exc

    with metrics_lock:
        metrics["requests"] += 1
        metrics["latency_total_ms"] += latency_ms
    return {
        "rotulo": label,
        "probabilidade": probability,
        "versao": MODEL_VERSION,
        "latencia_ms": latency_ms,
    }


@app.get("/metrics")
def get_metrics():
    with metrics_lock:
        requests = metrics["requests"]
        latency = metrics["latency_total_ms"] / requests if requests else 0.0
        return {
            "requests": requests,
            "errors_5xx": metrics["errors_5xx"],
            "latencia_media_ms": round(latency, 2),
        }
