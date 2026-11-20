import os

os.environ["API_KEY"] = "chave-teste"
os.environ["MODEL_VERSION"] = "v-test"

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_does_not_require_api_key():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["versao"] == "v-test"


def test_predict_requires_api_key():
    response = client.post("/predict", json={"texto": "Mensagem de teste"})

    assert response.status_code == 401


def test_predict_rejects_empty_text():
    response = client.post(
        "/predict",
        json={"texto": "   "},
        headers={"X-API-Key": "chave-teste"},
    )

    assert response.status_code == 422


def test_predict_returns_valid_result_with_api_key():
    response = client.post(
        "/predict",
        json={"texto": "Parabens! Voce ganhou um premio. Clique no link agora"},
        headers={"X-API-Key": "chave-teste"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["rotulo"] in {"spam", "nao_spam"}
    assert 0.0 <= body["probabilidade"] <= 1.0
    assert body["versao"] == "v-test"
