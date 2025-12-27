# Docs Vert - API de Conversão de Documentos

API rápida e segura para conversão de documentos DOCX → PDF usando LibreOffice.

## ⚡ Quick Start

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Rodar servidor
python main.py

# 3. Acessar
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
```

## 🔐 Autenticação

Seu token está em `.token`. Use em todas as requisições:

```bash
TOKEN=$(cat .token)

curl -X POST http://localhost:8000/api/v1/conversion/docx-to-pdf \
  -H "x-api-key: $TOKEN" \
  -F "file=@documento.docx" \
  -o documento.pdf
```

## 📋 Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/v1/conversion/docx-to-pdf` | Converte DOCX para PDF |
| GET | `/api/v1/conversion/health` | Health check |
| GET | `/` | Info da API |

## 🔧 Configuração

Edite `.env` para ajustar:

```env
DEBUG=False
HOST=0.0.0.0
PORT=8000
LIBREOFFICE_PATH=/usr/bin/soffice
LOG_LEVEL=info
```

## 📦 Produção

Para deploy em VPS, veja [DEPLOY.md](DEPLOY.md)

## 📊 Rate Limits

- 🔄 Conversão: **10 requisições/minuto**
- ❤️ Health: **30 requisições/minuto**

## ⚙️ Requisitos do Sistema

- Python 3.10+
- LibreOffice (para conversão)
- 512 MB RAM mínimo

## 📁 Estrutura

```
docs-vert/
├── app/
│   ├── api/routes/           # Endpoints
│   ├── core/                 # Configuração e segurança
│   ├── models/               # Schemas Pydantic
│   ├── services/             # Lógica de negócio
│   └── utils/                # Utilidades
├── uploads/                  # Arquivos temporários
├── main.py                   # Entry point
├── service.py                # App FastAPI
├── requirements.txt          # Dependências
└── .env.example              # Variáveis de exemplo
```

## 🐛 Logs

```bash
# Desenvolvimento
python main.py

# Produção
tail -f logs/app.log
```

## 📝 Licença

MIT