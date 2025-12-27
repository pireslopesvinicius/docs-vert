#!/bin/bash

# Script de inicialização para VPS com uv

# Parar se houver erro
set -e

echo "🚀 Iniciando Docs Vert API..."

# Instalar uv se não existir
if ! command -v uv &> /dev/null; then
    echo "📥 Instalando uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Instalar dependências com uv (cria venv automaticamente)
echo "📥 Instalando dependências com uv..."
uv sync

# Criar diretório de uploads se não existir
mkdir -p uploads

echo "✅ Pronto para rodar!"
echo ""
echo "Para iniciar o servidor:"
echo "  uv run gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 service:app"
echo ""
echo "Ou com uvicorn diretamente (não recomendado para produção):"
echo "  uv run uvicorn service:app --host 0.0.0.0 --port 8000"

