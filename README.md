# Classificador de Spam

Aplicação MLOps desenvolvida em Python para identificar mensagens de texto como **spam**
ou **não spam**.

A interface web permite informar uma chave de API, inserir uma mensagem, visualizar o
resultado e a probabilidade da classificação. A aplicação também consulta o estado da API,
exibe métricas operacionais e permite enviar 50 requisições consecutivas para teste de carga.

## Arquitetura

```text
Navegador
   |
   v
Interface Streamlit (app/page.py)
   |
   v
API FastAPI (app/main.py)
   |
   v
Modelo TF-IDF + Regressão Logística (model/modelo.joblib)
```

## Funcionalidades

- Classificação de mensagens como `spam` ou `nao_spam`
- Exibição da probabilidade da classe selecionada
- Exibição da versão do modelo e da latência da resposta
- Verificação automática da disponibilidade da API
- Proteção do endpoint de classificação por chave de API
- Exemplos prontos de mensagem spam e mensagem comum
- Painel de métricas:
  - requisições realizadas
  - erros HTTP 5xx
  - latência média
- Envio de 50 requisições reais para teste de carga

## Tecnologias

- Python
- FastAPI
- Uvicorn
- Streamlit
- scikit-learn 1.8.0
- joblib
- python-dotenv
- pytest

## Estrutura do projeto

```text
app/
  main.py          # API FastAPI
  page.py          # Interface Streamlit
model/
  modelo.joblib    # Modelo treinado
  train.py         # Script de treinamento
data/
  mensagens.csv    # Base de dados de treino
tests/
  test_api.py      # Testes dos endpoints
.env.example       # Modelo das variáveis de ambiente
requirements.txt   # Dependências da aplicação
run.py             # Inicia a API e a interface
.streamlit/        # Configuração visual do Streamlit
Dockerfile.api      # Empacotamento da API
Dockerfile.page     # Empacotamento da interface
docker-compose.yml  # Orquestração dos dois containers
```

## Requisitos

- Python 3.12, 3.13 ou 3.14
- pip
- Windows, Linux ou macOS

O projeto foi configurado para usar `scikit-learn==1.8.0`, pois essa versão corresponde ao
arquivo `model/modelo.joblib`.

## Instalação no Windows

Clone o repositório e entre na pasta do projeto:

```powershell
git clone <URL_DO_REPOSITORIO>
cd "Projeto MLOps"
```

Crie o ambiente virtual:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Crie o arquivo de configuração local:

```powershell
Copy-Item .env.example .env
```

## Configuração

As configurações ficam no arquivo `.env`, que não deve ser enviado ao Git.

Exemplo:

```text
APP_ENV=dev
MODEL_VERSION=v1
API_KEY=chave-ficticia-123
API_URL=http://127.0.0.1:8000
API_HOST=127.0.0.1
API_PORT=8000
```

Variáveis disponíveis:

| Variável | Descrição | Valor padrão |
|---|---|---|
| `APP_ENV` | Ambiente da aplicação | `dev` |
| `MODEL_VERSION` | Versão exibida pela API | `v1` |
| `API_KEY` | Chave exigida pelo endpoint `/predict` | não definida |
| `API_URL` | Endereço usado pela interface Streamlit | `http://127.0.0.1:8000` |
| `API_HOST` | Host usado pelo Uvicorn | `127.0.0.1` |
| `API_PORT` | Porta usada pela API | `8000` |

O arquivo `.env.example` contém os valores fictícios adequados para uso local.

## Executar a aplicação

Com o ambiente virtual ativado e o arquivo `.env` criado:

```powershell
python run.py
```

Esse comando inicia simultaneamente:

- API FastAPI: http://127.0.0.1:8000
- Interface Streamlit: http://127.0.0.1:8501
- Documentação Swagger: http://127.0.0.1:8000/docs

Para encerrar os dois processos, pressione `Ctrl+C` no terminal.

## Executar separadamente

API:

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Interface:

```powershell
python -m streamlit run app/page.py --server.port 8501
```

## Executar com Docker

É necessário ter Docker Desktop instalado e em execução.

As imagens Docker são identificadas pela tag `V1`:

- API: `projetomlops-api:V1`
- Interface: `projetomlops-page:V1`

Na raiz do projeto, construa as imagens com a tag configurada no Docker Compose e
inicie os containers:

```powershell
docker compose up --build
```

Para iniciar em segundo plano:

```powershell
docker compose up --build -d
```

Endereços:

- Interface: http://localhost:8501
- API: http://localhost:8000
- Documentação: http://localhost:8000/docs

As configurações podem ser informadas no `.env`:

```text
APP_ENV=dev
MODEL_VERSION=v1
API_KEY=chave-ficticia-123
API_PORT=8000
PAGE_PORT=8501
```

O Docker Compose também aceita os valores padrão caso `API_KEY` não esteja definida.

Para recriar apenas os containers a partir das imagens `V1` existentes:

```powershell
docker compose up -d
```

Para verificar as imagens locais:

```powershell
docker image ls projetomlops-api:V1
docker image ls projetomlops-page:V1
```

Comandos úteis:

```powershell
docker compose ps
docker compose logs -f
docker compose down
docker compose down --volumes
```

## Usar a interface

1. Abra http://127.0.0.1:8501.
2. No campo **Chave de API**, informe `chave-ficticia-123` ou o valor configurado em
   `API_KEY`.
3. Digite uma mensagem ou selecione um dos exemplos.
4. Clique em **Classificar**.
5. Consulte o rótulo, a probabilidade, a versão do modelo e a latência.

O botão **Enviar 50 requisições** envia classificações reais para a API e atualiza o painel
de operação.

## Endpoints da API

### Verificar estado

```text
GET /health
```

Exemplo de resposta:

```json
{
  "status": "ok",
  "versao": "v1",
  "ambiente": "dev"
}
```

### Classificar mensagem

```text
POST /predict
```

Cabeçalho quando `API_KEY` está configurada:

```text
X-API-Key: chave-ficticia-123
```

Corpo da requisição:

```json
{
  "texto": "Parabéns! Você ganhou um prêmio. Clique no link agora"
}
```

Exemplo de resposta:

```json
{
  "rotulo": "spam",
  "probabilidade": 0.567,
  "versao": "v1",
  "latencia_ms": 12.5
}
```

Exemplo com PowerShell:

```powershell
$body = @{
  texto = "Parabéns! Você ganhou um prêmio. Clique no link agora"
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri "http://127.0.0.1:8000/predict" `
  -ContentType "application/json" `
  -Headers @{ "X-API-Key" = "chave-ficticia-123" } `
  -Body $body
```

Erros importantes:

- `401` - chave ausente ou inválida
- `422` - texto vazio ou formato inválido
- `500` - falha interna durante a classificação

### Consultar métricas

```text
GET /metrics
```

Exemplo de resposta:

```json
{
  "requests": 128,
  "errors_5xx": 0,
  "latencia_media_ms": 14.2
}
```

## Testes

Execute a suíte de testes pela raiz do projeto:

```powershell
python -m pytest -q
```

Os testes verificam o estado da API, autenticação, rejeição de texto vazio e o resultado
válido de uma classificação.

## Retreinamento do modelo

Para instalar as dependências específicas de treinamento:

```powershell
python -m pip install -r requirements-treino.txt
```

Para treinar novamente a partir da base padrão:

```powershell
python model/train.py
```

Para usar outro CSV:

```powershell
python model/train.py --csv caminho/para/arquivo.csv --saida model/modelo.joblib
```

O CSV de treinamento deve possuir as colunas `texto` e `rotulo`, com os rótulos `spam`
e `nao_spam`.

## Segurança

- Nunca envie o arquivo `.env` ao repositório.
- Nunca inclua a chave real no código-fonte.
- Em uma publicação pública, configure `API_KEY` como variável de ambiente da plataforma.
- Use uma chave diferente da chave fictícia usada nos testes locais.
- Antes de publicar, revise o histórico Git para garantir que nenhum segredo tenha sido enviado.

## Solução de problemas

### Streamlit não inicia

Instale novamente as dependências:

```powershell
python -m pip install -r requirements.txt
```

### Erro ao carregar o modelo

Confirme a versão do scikit-learn:

```powershell
python -m pip show scikit-learn
```

O resultado deve indicar `Version: 1.8.0`.

### A chave é informada como inválida

A chave digitada na interface deve ser exatamente igual ao valor de `API_KEY`.

No projeto local, o valor padrão é:

```text
chave-ficticia-123
```

Se o arquivo `.env` foi alterado, reinicie a API para carregar o novo valor.

### A interface não consegue acessar a API

Confirme que:

- a API está ativa em http://127.0.0.1:8000;
- `API_URL` aponta para esse endereço;
- nenhuma outra aplicação está ocupando a porta 8000.

### Porta ocupada

Altere as portas no `.env` e reinicie os processos:

```text
API_HOST=127.0.0.1
API_PORT=8001
API_URL=http://127.0.0.1:8001
```
requirements-api.txt  # Dependências exclusivas da API
requirements-page.txt # Dependências exclusivas da interface
