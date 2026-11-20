"""Interface Streamlit para testar e acompanhar a API de classificação de spam."""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import streamlit as st


API_URL = os.getenv("API_URL", "http://localhost:8000").rstrip("/")
SPAM_EXAMPLE = "Parabéns! Você ganhou um prêmio, clique no link para resgatar agora"
COMMON_EXAMPLE = "A reunião de amanhã foi adiada para quinta"

st.set_page_config(page_title="Classificador de spam", page_icon="🛡️", layout="centered")
st.markdown(
    """
    <style>
    html, body, [class*="css"] { font-family: "Segoe UI", sans-serif; }
    .stApp { background: #191a20; color: #f2f3f7; }
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"], [data-testid="stMainMenu"],
    footer { visibility: hidden; height: 0; }
    [data-testid="stAppViewContainer"] { background: #191a20; }
    .block-container {
        max-width: 760px;
        padding: 1.5rem 1.75rem 2rem 1.75rem;
        margin: 0 auto;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #343640;
        border-radius: 10px;
        background: #20232d;
        padding: 22px 31px 24px 31px;
    }
    [data-testid="stMarkdownContainer"] p {
        color: #f2f3f7;
    }
    .stTextInput label, .stTextArea label {
        color: #d8dbeb !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        background: #262936 !important;
        color: #f2f3f7 !important;
        border: 1px solid #3b3e4d !important;
        border-radius: 7px !important;
    }
    div[data-testid="stTextInput"] input { height: 44px; }
    div[data-testid="stTextArea"] textarea { height: 56px !important; min-height: 56px !important; }
    div[data-testid="stTextArea"] {
        height: 70px;
        overflow: hidden;
    }
    div[data-testid="stVerticalBlock"] { gap: 0.45rem; }
    div[data-testid="stTextArea"] textarea::placeholder,
    div[data-testid="stTextInput"] input::placeholder {
        color: #aaadbb !important;
    }
    div.stButton > button {
        border-radius: 7px;
        min-height: 42px;
        border: 1px solid #454858;
        background: #282b39;
        color: #dfe1ec;
        font-weight: 600;
    }
    div[data-testid="stButton"] button[kind="primary"],
    div[data-testid="stButton"] button[kind="primary"]:hover,
    div[data-testid="stButton"] button[kind="primary"]:active,
    div[data-testid="stButton"] button[kind="primary"]:focus {
        background: #f6f6f6 !important;
        color: #111111 !important;
        border: 1px solid #f6f6f6 !important;
    }
    div[data-testid="stButton"] button[kind="primary"] *,
    div[data-testid="stButton"] button[kind="primary"] p,
    div[data-testid="stButton"] button[kind="primary"] span {
        color: #111111 !important;
        opacity: 1 !important;
    }
    div[data-testid="stProgress"] {
        height: 8px;
        margin-top: 6px;
    }
    div[data-testid="stProgress"] > div {
        background: #3a3d49;
        border-radius: 2px;
        height: 8px;
    }
    div[data-testid="stProgress"] > div > div {
        background: #e27a84;
        border-radius: 2px;
        height: 8px;
    }
    hr { border-color: #343740; }
    [data-testid="stColumn"] { gap: 0.5rem; }
    [data-testid="stMetric"] {
        background: transparent;
        border: 0;
        padding: 0;
    }
    [data-testid="stMetricLabel"] {
        color: #c8cada;
        font-size: 14px;
    }
    [data-testid="stMetricValue"] {
        color: #f2f3f7;
        font-size: 27px;
        font-weight: 500;
    }
    .reference-result {
        margin-top: 4px;
        margin-bottom: 12px;
    }
    .reference-result-line {
        display: flex;
        align-items: center;
        gap: 14px;
        color: #c7c9d7;
        font-size: 14px;
        margin: 5px 0 18px 0;
    }
    .reference-result-line .label {
        color: #ed7c86;
        font-weight: 700;
    }
    .reference-probability-title {
        color: #cfd1dd;
        font-size: 14px;
        margin-bottom: 4px;
    }
    .reference-probability-value {
        display: flex;
        justify-content: space-between;
        color: #58a8ff;
        font-size: 14px;
        margin-top: 6px;
    }
    .operation-metrics {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        margin-top: 16px;
    }
    .operation-metric {
        text-align: left;
    }
    .operation-metric-label {
        color: #c5c7d4;
        font-size: 14px;
    }
    .operation-metric-value {
        color: #f2f3f7;
        font-size: 27px;
        font-weight: 500;
        line-height: 1.15;
        margin-top: 5px;
    }
    .header-title {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #f2f3f7;
        font-size: 22px;
        font-weight: 700;
        height: 44px;
    }
    .header-title .shield {
        color: #61a4ff;
        font-size: 24px;
    }
    .version-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        height: 24px;
        min-width: 82px;
        border-radius: 14px;
        background: #282f45;
        color: #62a6ff;
        border: 1px solid #3a4e74;
        font-size: 12px;
        font-weight: 700;
    }
    .health-badge {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 7px;
        height: 44px;
        color: #45d66a;
        font-size: 14px;
        font-weight: 600;
    }
    .health-badge.down { color: #ed7c86; }
    .health-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #45d66a;
        box-shadow: 0 0 9px #45d66a;
    }
    .health-badge.down .health-dot {
        background: #ed7c86;
        box-shadow: 0 0 9px #ed7c86;
    }
    .result-heading {
        font-size: 14px;
        font-weight: 700;
        color: #cfd1dd;
        margin: 18px 0 12px 0;
    }
    .operation-heading {
        color: #cfd1dd;
        font-size: 14px;
        font-weight: 700;
        margin: 0;
        height: 42px;
        display: flex;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def api_request(path: str, api_key: str = "", payload: dict | None = None) -> dict:
    headers = {"Accept": "application/json"}
    body = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(payload).encode("utf-8")
    if api_key:
        headers["X-API-Key"] = api_key

    request = Request(f"{API_URL}{path}", data=body, headers=headers)
    try:
        with urlopen(request, timeout=8) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(response_body).get("detail", response_body)
        except json.JSONDecodeError:
            detail = response_body or str(exc)
        raise RuntimeError(f"API retornou HTTP {exc.code}: {detail}") from exc
    except (URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(f"Não foi possível conectar à API em {API_URL}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("A API retornou uma resposta inválida.") from exc


def use_example(text: str) -> None:
    st.session_state["message"] = text


if "message" not in st.session_state:
    st.session_state["message"] = SPAM_EXAMPLE

with st.container(border=True):
    header = st.columns([5, 1.5, 2])
    with header[0]:
        st.markdown(
            '<div class="header-title"><span class="shield">🛡️</span><span>Classificador de spam</span></div>',
            unsafe_allow_html=True,
        )

    try:
        health = api_request("/health")
        version = health.get("versao", "—")
        with header[1]:
            st.markdown(
                f'<div style="height:44px;display:flex;align-items:center;"><span class="version-badge">versão {version}</span></div>',
                unsafe_allow_html=True,
            )
        with header[2]:
            st.markdown(
                '<div class="health-badge"><span class="health-dot"></span><span>Serviço saudável</span></div>',
                unsafe_allow_html=True,
            )
    except RuntimeError as exc:
        with header[1]:
            st.markdown(
                '<div style="height:44px;display:flex;align-items:center;"><span class="version-badge">versão —</span></div>',
                unsafe_allow_html=True,
            )
        with header[2]:
            st.markdown(
                '<div class="health-badge down"><span class="health-dot"></span><span>Serviço indisponível</span></div>',
                unsafe_allow_html=True,
            )
        st.caption(str(exc))

    api_key = st.text_input(
        "Chave de API",
        type="password",
        placeholder="chave-ficticia-123",
        help="Use o mesmo valor de API_KEY definido no arquivo .env.",
    ).strip()
    message = st.text_area("Mensagem", key="message", height=96)

    buttons = st.columns([1, 1.55, 1.5])
    classify = buttons[0].button("Classificar", type="primary", width="stretch")
    buttons[1].button(
        "Exemplo de spam",
        on_click=use_example,
        args=(SPAM_EXAMPLE,),
        width="stretch",
    )
    buttons[2].button(
        "Exemplo comum",
        on_click=use_example,
        args=(COMMON_EXAMPLE,),
        width="stretch",
    )

    st.markdown('<div class="result-heading">Resultado</div>', unsafe_allow_html=True)
    if classify:
        if not message.strip():
            st.error("Digite uma mensagem antes de classificar.")
        else:
            try:
                with st.spinner("Classificando mensagem..."):
                    result = api_request("/predict", api_key, {"texto": message})
                st.session_state["result"] = result
                st.session_state["result_error"] = None
            except RuntimeError as exc:
                st.session_state["result_error"] = str(exc)
                st.session_state.pop("result", None)

    if st.session_state.get("result_error"):
        st.error(st.session_state["result_error"])
    elif result := st.session_state.get("result"):
        label = result["rotulo"]
        probability = float(result["probabilidade"])
        label_text = "spam" if label == "spam" else "não spam"
        st.markdown(
            '<div class="reference-result-line">'
            f'<span style="color:#ed7c86;font-size:18px;">⚠</span>'
            f'<span class="label">{label_text}</span>'
            f'<span>resposta em {result.get("latencia_ms", "—")} ms</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="reference-probability-title">Probabilidade</div>',
            unsafe_allow_html=True,
        )
        st.progress(max(0.0, min(probability, 1.0)))
        st.markdown(
            '<div class="reference-probability-value">'
            f'<span>{probability:.2f}'.replace(".", ",") + '</span>'
            f'<span>respondido pela versão {result["versao"]}</span>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.caption("O resultado da classificação aparecerá aqui.")

    st.divider()
    operation_header = st.columns([3, 2], vertical_alignment="center")
    operation_header[0].markdown(
        '<div class="operation-heading">Painel de operação</div>',
        unsafe_allow_html=True,
    )
    run_batch = operation_header[1].button(
        "▷ Enviar 50 requisições", width="stretch"
    )
    if run_batch:
        if not message.strip():
            st.error("Digite uma mensagem antes de enviar as requisições.")
        else:
            progress = st.progress(0)
            failures = 0
            for index in range(50):
                try:
                    api_request("/predict", api_key, {"texto": message})
                except RuntimeError:
                    failures += 1
                progress.progress((index + 1) / 50)
            if failures:
                st.warning(f"Concluído: {50 - failures} sucesso(s) e {failures} falha(s).")
            else:
                st.success("As 50 requisições foram concluídas.")

    try:
        operation_metrics = api_request("/metrics", api_key)
        st.markdown(
            '<div class="operation-metrics">'
            f'<div class="operation-metric"><div class="operation-metric-label">Requisições</div>'
            f'<div class="operation-metric-value">{operation_metrics["requests"]}</div></div>'
            f'<div class="operation-metric"><div class="operation-metric-label">Erros 5xx</div>'
            f'<div class="operation-metric-value">{operation_metrics["errors_5xx"]}</div></div>'
            f'<div class="operation-metric"><div class="operation-metric-label">Latência média</div>'
            f'<div class="operation-metric-value">{operation_metrics["latencia_media_ms"]} ms</div></div>'
            '</div>',
            unsafe_allow_html=True,
        )
    except RuntimeError as exc:
        st.caption(f"Métricas indisponíveis: {exc}")
