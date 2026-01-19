# 🚀 Guia Rápido: Git → VPS

## 1️⃣ NO SEU COMPUTADOR (Local)

### Preparar Git

```bash
# Já deve estar pronto
cd c:\Dev\docs-vert

# Ver se está no Git
git status

# Se não estiver, inicializar
git init
git add .
git commit -m "Initial commit: Docs Vert API"
git remote add origin https://github.com/seu-usuario/docs-vert.git
git push -u origin main
```

### Arquivos que DEVEM estar no Git

```
docs-vert/
├── app/                      ✅ Sim
├── uploads/                  ❌ Não (adicionar em .gitignore)
├── .venv/ ou venv/           ❌ Não (adicionar em .gitignore)
├── main.py                   ✅ Sim
├── service.py                ✅ Sim
├── .token                    ❌ Não (adicionar em .gitignore)
├── .env                      ❌ Não (adicionar em .gitignore)
├── api_keys.json             ❌ Não (gerado na VPS)
├── pyproject.toml            ✅ Sim
├── requirements.txt          ✅ Sim
├── setup.sh                  ✅ Sim
├── docs-vert.service         ✅ Sim
├── nginx.conf                ✅ Sim
├── DEPLOY.md                 ✅ Sim
├── README.md                 ✅ Sim
├── .gitignore                ✅ Sim (criar)
└── .env.example              ✅ Sim
```

### Criar .gitignore

```bash
cat > .gitignore << 'EOF'
# Ambiente
.venv
venv
__pycache__
*.pyc
.env
.token

# Uploads
uploads/

# Arquivos gerados
api_keys.json
*.pdf
*.docx

# IDE
.vscode
.idea
*.swp
*.swo

# Sistema
.DS_Store
Thumbs.db
EOF

git add .gitignore
git commit -m "Add .gitignore"
git push
```

---

## 2️⃣ NA VPS (Hostinger)

### Estrutura de Diretórios

```
/home/
  ├── docs-vert/              👤 Usuário de sistema
  │   └── docs-vert/          📁 Pasta do projeto (do Git)
  │       ├── app/
  │       ├── setup.sh
  │       └── ...
  │
  └── nginx/
      └── sites-available/
          └── docs-vert       📄 Config do Nginx
```

### Passo 1: SSH na VPS

```bash
ssh usuario@seu-ip-ou-dominio
# ou via Hostinger: "Gerenciar" → "SSH Access"
```

### Passo 2: Preparar Sistema (como root)

```bash
# Virar root
sudo su -

# Atualizar
apt update && apt upgrade -y

# Instalar dependências
apt install -y python3 python3-pip python3-dev
apt install -y git
apt install -y libreoffice libreoffice-writer
apt install -y nginx
apt install -y curl

# Criar usuário para a app
useradd -m -s /bin/bash docs-vert
```

### Passo 3: Clonar Projeto (como usuário docs-vert)

```bash
# Virar usuário docs-vert
su - docs-vert

# Clonar do Git
git clone https://github.com/seu-usuario/docs-vert.git
cd docs-vert

# Executar setup (instala uv e dependências)
bash setup.sh

# Copiar .env.example para .env
cp .env.example .env

# Editar .env se necessário
nano .env

# Testar localmente
é p

# Em outro terminal
curl http://127.0.0.1:8000/
```

### Passo 4: Copiar Nginx Config (como root)

```bash
# Virar root
sudo su -

# Copiar config
cp /home/docs-vert/docs-vert/nginx.conf /etc/nginx/sites-available/docs-vert

# Editar: SUBSTITUIR seu-dominio.com pelo seu domínio real
nano /etc/nginx/sites-available/docs-vert

# Criar link
ln -s /etc/nginx/sites-available/docs-vert /etc/nginx/sites-enabled/

# Testar
nginx -t

# Recarregar
systemctl reload nginx
```

### Passo 5: Copiar Systemd Service (como root)

```bash
# Copiar
cp /home/docs-vert/docs-vert/docs-vert.service /etc/systemd/system/

# Recarregar daemon
systemctl daemon-reload

# Ativar no boot
systemctl enable docs-vert.service

# Iniciar
systemctl start docs-vert.service

# Verificar
systemctl status docs-vert.service

# Ver logs
journalctl -u docs-vert.service -f
```

### Passo 6: SSL com Let's Encrypt (como root)

```bash
# Instalar
apt install -y certbot python3-certbot-nginx

# Gerar certificado (SUBSTITUIR seu-dominio.com)
certbot certonly --nginx -d seu-dominio.com -d www.seu-dominio.com

# Automático! Nginx.conf já está configurado
systemctl reload nginx
```

---

## 📝 Checklist Final

```
Após clonar na VPS:

☐ Git clone feito
☐ setup.sh executado
☐ .env copiado e editado
☐ Testou localmente (curl)
☐ Nginx config copiado
☐ Nginx config editado com domínio correto
☐ Nginx recarregado
☐ Systemd service copiado
☐ Systemd service ativado
☐ Serviço iniciado
☐ SSL certificado gerado
☐ Teste final: curl https://seu-dominio.com/
```

---

## 🔄 Atualizar Código Depois

```bash
# Como usuário docs-vert
cd ~/docs-vert
git pull
uv sync
sudo systemctl restart docs-vert.service
```

---

## 🐛 Troubleshooting

```bash
# Ver status da API
systemctl status docs-vert.service

# Ver logs
journalctl -u docs-vert.service -n 50 -f

# Testar Nginx
curl http://127.0.0.1:8000/

# Testar HTTPS
curl https://seu-dominio.com/

# Ver processo
ps aux | grep gunicorn

# Ver porta 8000
lsof -i :8000

# Ver Nginx ativo
systemctl status nginx
```

---

**Dúvida? Veja [DEPLOY.md](DEPLOY.md) para o guia completo!**
