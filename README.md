# MCP Server - Integração Google Sheets

Este projeto expõe um endpoint REST via *FastAPI* que permite executar ações em uma planilha do *Google Sheets*.  
O acesso à planilha é feito com uma *Service Account* do Google Cloud utilizando credenciais no formato ⁠ credentials.json ⁠.

O serviço tbm expoe um endpoint /mcp.json com o contrato dos endpoints

---

## 💡 O que é ⁠ credentials.json ⁠?

⁠O credentials.json ⁠é o arquivo gerado pelo Google Cloud contendo as credenciais da sua *Service Account*.  
Ele permite que o servidor acesse APIs do Google (Google Sheets e Google Drive) sem necessidade de login manual, garantindo integração automática.

⚠ *Importante:* este arquivo é sensível e *não deve ser versionado* no Git. Adicione seu nome ao ⁠ .gitignore ⁠.

---

## 🛠 Como gerar o ⁠ credentials.json ⁠

1.⁠ ⁠*Acesse o Google Cloud Console*  
   👉 [https://console.cloud.google.com/](https://console.cloud.google.com/)

2.⁠ ⁠*Crie ou selecione um projeto*

3.⁠ ⁠*Ative as APIs necessárias*
   - Ative *Google Sheets API*
   - Ative *Google Drive API*

4.⁠ ⁠*Crie uma Service Account*
   - Vá em ⁠ IAM e Admin > Service Accounts ⁠
   - Clique em *Criar Service Account*
   - Defina um nome (ex.: ⁠ mcp-bot ⁠)
   - Conclua a criação

5.⁠ ⁠*Gere a chave JSON*
   - Dentro da Service Account criada, vá para a aba *Chaves*
   - Clique em "Adicionar chave" > "Criar nova chave" > Tipo *JSON*
   - Um arquivo ⁠ .json ⁠ será baixado — renomeie para ⁠ credentials.json ⁠ e coloque na raiz do projeto (ou outro local seguro)

6.⁠ ⁠*Dê acesso à planilha*
   - Abra a planilha no Google Sheets
   - Compartilhe com o e-mail da Service Account (no JSON: ⁠ "client_email": "xxxx@project.iam.gserviceaccount.com" ⁠)
   - Dê permissão de *Editor*

---

## ⚙ Configuração do ⁠ .env ⁠

Crie um arquivo ⁠ .env ⁠ na raiz do projeto:

```
PLANILHA_NOME=NomeExatoDaSuaPlanilha
GOOGLE_CREDS_PATH=credentials.json
```

## Executando o Projeto

```bash
uvicorn main:app --reload --port 5000
```

## 📡 Endpoint /execute
O endpoint permite ler, adicionar, editar ou remover dados de uma aba da planilha.

POST /execute
Request Body

```json
{
  "acao": "ler",
  "aba": "Aba1",
  "dados": null
}
```

Campos:

acao → "ler", "adicionar", "editar" ou "remover"
aba → Nome da aba dentro da planilha
dados → Estrutura varia conforme a ação:
   ler: null
   adicionar: { "coluna1": "valor1", "coluna2": "valor2" }
   editar: { "linha": 2, "coluna": 3, "novo_valor": "texto" }
   remover: { "linha": 5 }

## Exemplos:

### Ler
```bash
curl -X POST http://localhost:5000/executar \
-H "Content-Type: application/json" \
-d '{"acao": "ler", "aba": "Aba1"}'
```

### Adicionar
```bash
curl -X POST http://localhost:5000/executar \
-H "Content-Type: application/json" \
-d '{
  "acao": "adicionar",
  "aba": "Aba1",
  "dados": { "ticker": "PETR4", "quantidade": 100, "preco": 37.5 }
}'
```

### Editar
```bash
curl -X POST http://localhost:5000/executar \
-H "Content-Type: application/json" \
-d '{
  "acao": "editar",
  "aba": "Aba1",
  "dados": { "linha": 2, "coluna": 3, "novo_valor": "texto atual" }
}'
```

### Remover
```bash
curl -X POST http://localhost:5000/executar \
-H "Content-Type: application/json" \
-d '{
  "acao": "remover",
  "aba": "Aba1",
  "dados": { "linha": 5 }
}'
```

## 📜 Resposta Padrão
```json
{
  "status": "ok",
  "mensagem": "Linha adicionada com sucesso",
  "dados": [ ... ] // Apenas na ação de leitura
}
```

## ⚠ Segurança
Nunca exponha o credentials.json publicamente.
Ajuste permissões da planilha para evitar acessos indesejados.

### 📄 Manifesto MCP

O manifesto mcp.json descreve o servidor, suas ferramentas e schemas.
Exemplo de uso:

```bash
curl http://localhost:8000/mcp.json
```
