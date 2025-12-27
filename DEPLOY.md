# 🚀 Guia de Deploy na Hostinger

## Pré-requisitos
- Python 3.10+ instalado
- LibreOffice instalado
- Nginx (opcional, mas recomendado)
- SSH acesso à VPS

## 1. Preparar o Servidor

```bash
# Atualizar sistema
sudo apt update
sudo apt upgrade -y

# Instalar dependências
sudo apt install -y python3 python3-pip python3-venv python3-dev
sudo apt install -y libreoffice libreoffice-writer
sudo apt install -y nginx

# Criar usuário para a aplicação
sudo useradd -m -s /bin/bash docs-vert
sudo su - docs-vert
```

## 2. Clonar e Configurar Projeto

```bash
# Como usuário docs-vert
cd ~
git clone <seu-repo> docs-vert
cd docs-vert

# Executar setup (instala uv e dependências)
bash setup.sh

# Copiar .env.example para .env
cp .env.example .env

# Editar .env se necessário
nano .env
```

## 3. Testar Localmente

```bash
# Rodar com uv na porta 8000
uv run gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000 service:app

# Em outro terminal, testar
curl http://127.0.0.1:8000/
```

## 4. Configurar Systemd Service

```bash
# Como root
sudo cp /home/docs-vert/docs-vert/docs-vert.service /etc/systemd/system/

# Editar caminho se necessário
sudo nano /etc/systemd/system/docs-vert.service

# Ativar e iniciar
sudo systemctl daemon-reload
sudo systemctl enable docs-vert.service
sudo systemctl start docs-vert.service

# Verificar status
sudo systemctl status docs-vert.service

# Ver logs
sudo journalctl -u docs-vert.service -f
```

## 5. Configurar Nginx (Reverse Proxy)

```bash
# Como root
sudo cp /home/docs-vert/docs-vert/nginx.conf /etc/nginx/sites-available/docs-vert

# Editar arquivo com seu domínio
sudo nano /etc/nginx/sites-available/docs-vert

# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/docs-vert /etc/nginx/sites-enabled/

# Remover default se quiser
sudo rm /etc/nginx/sites-enabled/default

# Testar configuração
sudo nginx -t

# Recarregar nginx
sudo systemctl reload nginx
```

## 6. Configurar SSL com Let's Encrypt

```bash
# Instalar certbot
sudo apt install -y certbot python3-certbot-nginx

# Gerar certificado
sudo certbot certonly --nginx -d seu-dominio.com -d www.seu-dominio.com

# Certificado será salvo em /etc/letsencrypt/live/seu-dominio.com/
```

## 7. Monitoramento e Logs

```bash
# Logs da aplicação
sudo journalctl -u docs-vert.service -f

# Logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Monitorar uso de recursos
htop

# Ver processo
ps aux | grep gunicorn
```

## 8. Maintenance

```bash
# Reiniciar aplicação
sudo systemctl restart docs-vert.service

# Parar aplicação
sudo systemctl stop docs-vert.service

# Começar aplicação
sudo systemctl start docs-vert.service

# Atualizar código
cd /home/docs-vert/docs-vert
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart docs-vert.service
```

## Endpoints Disponíveis

```
POST   /api/v1/conversion/docx-to-pdf  (requer header x-api-key)
GET    /api/v1/conversion/health
GET    /                                (info da API)
GET    /health                          (health check simples)
```

## Troubleshooting

### Erro "ModuleNotFoundError"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### LibreOffice não encontrado
```bash
sudo apt install -y libreoffice libreoffice-writer

# Encontrar caminho
which soffice
```

### Permissões de arquivo
```bash
# Se tiver problema com uploads/
sudo chown -R docs-vert:docs-vert /home/docs-vert/docs-vert
chmod 755 /home/docs-vert/docs-vert
chmod 755 /home/docs-vert/docs-vert/uploads
```

### Porta já em uso
```bash
# Ver processo na porta 8000
sudo lsof -i :8000

# Matar processo
sudo kill -9 <PID>
```

---

**Dúvidas ou problemas?** Verifique logs com `sudo journalctl -u docs-vert.service -f`
