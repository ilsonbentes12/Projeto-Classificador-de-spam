# Modelo de site proposto

A página serve para **testar a API de forma visual**. Vocês escolhem as tecnologias e o visual,
mas a página deve ter os elementos abaixo.

## Esboço

    +--------------------------------------------------------------+
    |  Classificador de spam              [versão v1] [Serviço OK] |
    +--------------------------------------------------------------+
    |  Chave de API                      |  Resultado              |
    |  [**************]                  |  [ spam ]  resposta 12ms|
    |                                    |  Probabilidade          |
    |  Mensagem                          |  [=======----]  0,67    |
    |  [                              ]  |  respondido pela v1     |
    |  [                              ]  |                         |
    |  [Classificar] [Ex. spam] [Ex. comum]                        |
    +--------------------------------------------------------------+
    |  Painel de operação              [Enviar 50 requisições]     |
    |  [ Requisições: 128 ] [ Erros 5xx: 0 ] [ Latência: 14 ms ]   |
    +--------------------------------------------------------------+

## O que a página deve fazer

**Obrigatório (Etapa 1)**
- Campo de **chave de API** (a chave nunca fica escrita no código da página).
- Caixa de texto para a **mensagem** e botão **Classificar**.
- Mostrar o **resultado**: rótulo (spam / não spam), probabilidade e **versão** que respondeu.
- Mostrar o **estado do serviço**, consultando `/health`.
- Mostrar uma mensagem clara quando a API falhar (por exemplo, erro 401 ou 500).
- Botões com **exemplos prontos** (um de spam e um de mensagem comum).

**Desejável (Etapas 3 e 4)**
- **Painel de operação** com requisições, erros 5xx e latência média (lidos de `/metrics`).
- Botão **Enviar 50 requisições** para gerar carga.

## Por que o selo de versão e o estado do serviço importam

Nas próximas etapas vocês vão publicar uma `v2` e fazer **rollback**. A página precisa mostrar
qual versão respondeu e se o serviço está saudável, para que o deploy e o rollback fiquem visíveis.
