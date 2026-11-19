# Classificador de spam: repositório-base da atividade "Do notebook à produção"

Componente curricular **MLOps e Deploy** · Atividade em **dupla**

## 1. A história

Vocês são a "squad de MLOps" de uma startup. Uma cientista de dados criou um **classificador de
mensagens spam** que funciona no notebook dela. A empresa precisa dele **rodando de forma
confiável, versionada e monitorada**, com uma página web para testar, e acessível pela internet.

Seu trabalho **não** é melhorar o modelo. É colocá-lo em produção sem cair no "funciona só na
minha máquina". Nesta etapa vocês constroem a API, a página web e publicam a primeira versão.

## 2. O modelo

| | |
|---|---|
| **O que faz** | Lê uma mensagem de texto e diz se é `spam` ou `nao_spam`, com a probabilidade |
| **Para que serve** | Filtrar mensagens indesejadas (golpes, promoções falsas, links suspeitos) |
| **Tipo** | TF-IDF + Regressão Logística (scikit-learn) |
| **Arquivo** | `model/modelo.joblib` (poucos KB) |
| **Dados de treino** | `data/mensagens.csv`: 66 mensagens em português, rotuladas pelo professor |
| **Entrada** | Um texto |
| **Saída** | Um rótulo (`spam` ou `nao_spam`) e a probabilidade de cada classe |

**Limitações (importante):**
- O conjunto de treino é **pequeno**; o modelo erra com facilidade e as probabilidades são baixas
  (algo como 0,6 a 0,7). Isso é esperado: a atividade é sobre **entrega e operação**, não sobre acurácia.
- Para carregar o `.joblib`, é necessário **Python com `scikit-learn==1.8.0`**. Outra versão pode
  dar erro ou resultados diferentes.
- Se quiserem retreinar: `pip install -r requirements-treino.txt` e `python model/train.py`.

### Como usar o modelo em Python

Veja o arquivo `model/exemplo_uso.py`. Resumo:

    import joblib
    modelo = joblib.load("model/modelo.joblib")
    probabilidades = modelo.predict_proba(["Você ganhou um prêmio! Clique aqui"])[0]
    rotulo = modelo.classes_[probabilidades.argmax()]      # "spam" ou "nao_spam"

## 3. O que vocês vão construir

    [ Página web ]  --->  [ API de inferência ]  --->  [ Modelo (.joblib) ]
     (navegador)            /health  /predict

- **API:** completem o esqueleto em `app/main.py`.
- **Página web:** sigam o modelo de site em `docs/modelo_de_pagina.md`.
- **Tecnologias:** **vocês decidem.** A API precisa carregar o modelo `.joblib`, então precisa
  rodar em **Python** (o esqueleto usa FastAPI, mas Flask também serve). A página pode ser HTML +
  JavaScript simples ou um framework, e pode ficar junto da API ou em outro serviço.
  **Anotem e justifiquem** as escolhas no README de vocês.

## 4. Contrato da API (não mudem, a página e as próximas etapas dependem dele)

**`GET /health`** devolve status 200 e:

    {"status": "ok", "versao": "v1", "ambiente": "dev"}

**`POST /predict`** recebe:

    {"texto": "Parabéns! Você ganhou um prêmio, clique no link"}

e devolve:

    {"rotulo": "spam", "probabilidade": 0.67, "versao": "v1"}

Regras:
- Texto vazio deve ser rejeitado (erro 4xx).
- Se a variável `API_KEY` estiver definida, o `/predict` exige o cabeçalho `X-API-Key` com o
  mesmo valor; sem ele, responda **401**. O `/health` nunca exige chave.
- A `versao` vem da variável de ambiente `MODEL_VERSION`.

## 5. Etapa 1: passo a passo

### 5.1 Preparação
Este repositório-base é entregue em **pendrive**. Vocês vão criar o repositório da dupla **do zero**
no GitHub.

1. Cada pessoa usa sua conta no **GitHub**.
2. Copiem a pasta do pendrive para o computador de vocês.
3. Uma pessoa cria um repositório **vazio** no GitHub (sugestão de nome: `mlops-spam-nome1-nome2`).
   Adicionem a outra pessoa da dupla e **o professor** como colaboradores
   (*Settings > Collaborators*). O professor informará o usuário dele em sala.
4. Na pasta copiada, iniciem o Git e enviem o primeiro commit:

       git init -b main
       git add .
       git commit -m "chore: importa repositório-base"
       git remote add origin <url-do-repositorio>
       git push -u origin main

5. A outra pessoa clona o repositório: `git clone <url>`.
6. Instalem o ambiente:

       python -m venv .venv
       source .venv/bin/activate        # no Windows: .venv\Scripts\activate
       pip install -r requirements.txt

### 5.2 API
1. Completem `GET /health` e `POST /predict` em `app/main.py`.
2. Rodem: `uvicorn app.main:app --reload` e abram `http://localhost:8000/docs` para testar.
3. Testem com `curl` ou pela página `/docs` (exemplos prontos: veja `model/exemplo_uso.py`).

### 5.3 Configuração e segredos
- **Nada de configuração fixa no código.** Leiam tudo de variáveis de ambiente
  (`MODEL_VERSION`, `APP_ENV`, `API_KEY`).
- Copiem `.env.example` para `.env` (o `.gitignore` já impede o envio ao Git).
- A chave de API deste exercício é **fictícia**. Mesmo assim, tratem como segredo: nunca no
  código nem no repositório. Em produção, ela é configurada na plataforma de hospedagem.
- `APP_ENV=dev` (na sua máquina) e `APP_ENV=test` (online): o que muda entre os dois?
  Definam e documentem.

### 5.4 Página web
- Sigam `docs/modelo_de_pagina.md`.
- A página **não deve ter a chave embutida**: o usuário digita a chave em um campo.
- Testem os casos de erro: chave errada (401), API fora do ar, texto vazio.

### 5.5 Git (os dois fazem commits)
- **Commits pequenos e frequentes**, com mensagens claras. Exemplos:
  `feat: implementa endpoint /health` · `fix: trata texto vazio no /predict` · `docs: explica como rodar`.
- Os **dois** integrantes devem ter commits no histórico. Usem **pareamento**: uma pessoa digita
  (piloto) e a outra revisa e orienta (copiloto), e troquem a cada tarefa.
- Antes de começar a trabalhar: `git pull`. Depois de terminar uma tarefa: `git add`, `git commit`, `git push`.
- Sugestão: uma branch por tarefa e *pull request* no GitHub para a outra pessoa revisar.

### 5.6 Publicar online
Com internet, vocês vão testar **localmente e online**. O professor sugere o **Render**, mas a escolha é de vocês: escolham uma plataforma de hospedagem
gratuita para publicar a API e a página. Algumas opções (confiram as condições atuais, pois
planos gratuitos mudam):

| Opção | Observação |
|---|---|
| **Render** (sugestão do professor) | Serviços web e sites estáticos gratuitos, publicando direto do GitHub; o serviço gratuito "hiberna" após alguns minutos sem uso, então a primeira requisição pode demorar |
| **GitHub Pages** | Só para páginas estáticas (a API precisa ficar em outro lugar) |
| Outras | Pesquisem e justifiquem a escolha |

Configurem as variáveis de ambiente **na plataforma** (não no código) e anotem a URL.
Depois, repitam os testes na versão online.

### 5.7 Documentação
Escrevam um `README` da dupla (substituam este ou criem `README_DUPLA.md`) com: o que foi
construído, tecnologias escolhidas e por quê, como rodar localmente, variáveis de ambiente
necessárias, a URL online e quem fez o quê.

## 6. Entrega e critérios de aceite da Etapa 1

- [ ] API com `/health` e `/predict` funcionando **localmente**, conforme o contrato
- [ ] `/predict` devolve 401 sem a chave correta (quando `API_KEY` está definida) e erro 4xx para texto vazio
- [ ] Página web funcionando localmente, com os itens obrigatórios do modelo de site
- [ ] Configuração por variáveis de ambiente e `.env.example` presente
- [ ] Nenhum segredo no repositório (conferir o histórico, não só os arquivos atuais)
- [ ] Repositório no GitHub com histórico de commits **dos dois integrantes** e o **professor adicionado como colaborador**
- [ ] Tag **`v1`** criada no commit entregue (`git tag v1 && git push origin v1`)
- [ ] Primeira versão **publicada online**, testada pela URL pública
- [ ] README da dupla com instruções, escolhas de tecnologia e URL. **O professor vai clonar o repositório e rodar seguindo só o README**, então ele precisa estar completo (versão do Python, comandos, variáveis de ambiente)

## 7. O que vem depois

Nas próximas etapas vocês vão **empacotar** o serviço (Docker), **implantar** em um cluster local,
montar um **pipeline de CI/CD**, adicionar **logs e métricas** e, por fim, enfrentar um **incidente
simulado** com rollback. Por isso, o que vocês construírem agora precisa ser organizado, com
configuração fora do código e testes fáceis de rodar.

## 8. Erros comuns

- **`InconsistentVersionWarning` ou erro ao abrir o modelo:** a versão do scikit-learn não é a 1.8.0.
- **A página não consegue chamar a API estando em outro endereço:** pesquisem sobre **CORS**.
- **Serviço online demora muito na primeira requisição:** plano gratuito hibernando; é esperado.
- **Subiram uma chave por engano:** apaguem do código, troquem a chave e avisem o professor.
  Apagar o arquivo depois do commit não remove a chave do histórico.
# Projeto-Classificador-de-spam
