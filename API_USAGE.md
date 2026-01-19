# Docs Vert API - Documentação de Uso

## 📋 Visão Geral

API para converter arquivos DOCX (Word) para PDF usando LibreOffice.

**Base URL:** `https://31.220.50.21:9443/api/v1`

## 🔐 Autenticação

Todas as requisições requerem o header:

```
x-api-key: docs-vert-hL4aofb7JxJptcbtYvpNhSC5SrE3BamC2tqZ_eB27cQ
```

## ⚡ Rate Limiting

- **Conversões:** 10 requisições por minuto
- **Health check:** 30 requisições por minuto

Limite por IP.

---

## 🔄 Endpoints

### 1. Health Check

**GET** `/conversion/health`

Verifica se a API está operacional.

#### Requisição
```bash
curl -k -H "x-api-key: docs-vert-hL4aofb7JxJptcbtYvpNhSC5SrE3BamC2tqZ_eB27cQ" \
  https://31.220.50.21:9443/api/v1/conversion/health
```

#### Resposta (200 OK)
```json
{
  "status": "ok",
  "service": "conversion"
}
```

---

### 2. Converter DOCX para PDF

**POST** `/conversion/docx-to-pdf`

Converte um arquivo DOCX em PDF.

#### Requisição
```bash
curl -k -X POST \
  -H "x-api-key: docs-vert-hL4aofb7JxJptcbtYvpNhSC5SrE3BamC2tqZ_eB27cQ" \
  -F "file=@documento.docx" \
  https://31.220.50.21:9443/api/v1/conversion/docx-to-pdf \
  --output resultado.pdf
```

#### Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|------------|-----------|
| `file` | File | Sim | Arquivo DOCX a converter |

#### Resposta (200 OK)
- **Content-Type:** `application/pdf`
- **Body:** Arquivo PDF em binário

#### Erros

| Código | Descrição |
|--------|-----------|
| 400 | Arquivo não enviado ou formato inválido |
| 401 | Token inválido ou ausente |
| 429 | Rate limit excedido |
| 500 | Erro na conversão |

---

## 💻 Exemplos de Integração

### Python
```python
import requests

TOKEN = "docs-vert-hL4aofb7JxJptcbtYvpNhSC5SrE3BamC2tqZ_eB27cQ"
API_URL = "https://31.220.50.21:9443/api/v1/conversion/docx-to-pdf"

# Health check
response = requests.get(
    "https://31.220.50.21:9443/api/v1/conversion/health",
    headers={"x-api-key": TOKEN},
    verify=False  # Ignora certificado self-signed
)
print(response.json())

# Conversão
with open("documento.docx", "rb") as f:
    files = {"file": f}
    headers = {"x-api-key": TOKEN}
    
    response = requests.post(
        API_URL,
        files=files,
        headers=headers,
        verify=False
    )
    
    if response.status_code == 200:
        with open("output.pdf", "wb") as pdf:
            pdf.write(response.content)
        print("✓ Convertido com sucesso!")
    else:
        print(f"✗ Erro: {response.status_code} - {response.text}")
```

### JavaScript/Node.js
```javascript
const fetch = require('node-fetch');
const fs = require('fs');
const FormData = require('form-data');

const TOKEN = "docs-vert-hL4aofb7JxJptcbtYvpNhSC5SrE3BamC2tqZ_eB27cQ";
const API_URL = "https://31.220.50.21:9443/api/v1/conversion/docx-to-pdf";

// Health check
fetch("https://31.220.50.21:9443/api/v1/conversion/health", {
  headers: { "x-api-key": TOKEN },
  rejectUnauthorized: false
})
.then(r => r.json())
.then(data => console.log(data));

// Conversão
const form = new FormData();
form.append('file', fs.createReadStream('documento.docx'));

fetch(API_URL, {
  method: 'POST',
  headers: { "x-api-key": TOKEN },
  body: form,
  rejectUnauthorized: false
})
.then(r => r.arrayBuffer())
.then(buffer => {
  fs.writeFileSync('output.pdf', buffer);
  console.log('✓ Convertido com sucesso!');
})
.catch(err => console.error('✗ Erro:', err));
```

### PowerShell
```powershell
$TOKEN = "docs-vert-hL4aofb7JxJptcbtYvpNhSC5SrE3BamC2tqZ_eB27cQ"
$API_URL = "https://31.220.50.21:9443/api/v1/conversion/docx-to-pdf"

# Health check
curl.exe -k -H "x-api-key: $TOKEN" `
  https://31.220.50.21:9443/api/v1/conversion/health

# Conversão
curl.exe -k -X POST `
  -H "x-api-key: $TOKEN" `
  -F "file=@documento.docx" `
  $API_URL `
  -o resultado.pdf
```

### cURL (Bash)
```bash
TOKEN="docs-vert-hL4aofb7JxJptcbtYvpNhSC5SrE3BamC2tqZ_eB27cQ"
API_URL="https://31.220.50.21:9443/api/v1/conversion/docx-to-pdf"

# Health check
curl -k -H "x-api-key: $TOKEN" \
  https://31.220.50.21:9443/api/v1/conversion/health

# Conversão
curl -k -X POST \
  -H "x-api-key: $TOKEN" \
  -F "file=@documento.docx" \
  $API_URL \
  --output resultado.pdf
```

### Postman
1. **URL:** `https://31.220.50.21:9443/api/v1/conversion/docx-to-pdf`
2. **Method:** POST
3. **Headers:**
   - `x-api-key: docs-vert-hL4aofb7JxJptcbtYvpNhSC5SrE3BamC2tqZ_eB27cQ`
4. **Body:** Form-data
   - Key: `file`
   - Type: `File`
   - Value: Selecione arquivo DOCX
5. **SSL:** Desabilite verificação SSL (para self-signed cert)

---

## 🔧 Tratamento de Erros

### Exemplo de tratamento robusto (Python)

```python
import requests
from requests.exceptions import RequestException
import time

def convert_with_retry(file_path, max_retries=3):
    TOKEN = "docs-vert-hL4aofb7JxJptcbtYvpNhSC5SrE3BamC2tqZ_eB27cQ"
    API_URL = "https://31.220.50.21:9443/api/v1/conversion/docx-to-pdf"
    
    for attempt in range(max_retries):
        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                headers = {"x-api-key": TOKEN}
                
                response = requests.post(
                    API_URL,
                    files=files,
                    headers=headers,
                    verify=False,
                    timeout=30
                )
            
            if response.status_code == 200:
                return response.content
            
            elif response.status_code == 429:
                wait_time = 60  # Rate limited
                print(f"Rate limit! Aguardando {wait_time}s...")
                time.sleep(wait_time)
                continue
            
            elif response.status_code == 401:
                print("✗ Token inválido!")
                return None
            
            else:
                print(f"✗ Erro {response.status_code}: {response.text}")
                return None
        
        except RequestException as e:
            print(f"Tentativa {attempt + 1} falhou: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    
    return None

# Uso
pdf_data = convert_with_retry("documento.docx")
if pdf_data:
    with open("output.pdf", "wb") as f:
        f.write(pdf_data)
```

---

## 📊 Status da API

Monitore a saúde da API com verificações periódicas:

```bash
# A cada 5 minutos
*/5 * * * * curl -k -H "x-api-key: TOKEN" https://31.220.50.21:9443/api/v1/conversion/health
```

---

## ❓ FAQ

**P: Por que o certificado é self-signed?**
R: Para ambiente de produção com IP fixo. Se tiver domínio, migre para Let's Encrypt.

**P: Como aumentar o rate limit?**
R: Contacte o administrador ou edite `app/core/rate_limiting.py`.

**P: A conversão é assíncrona?**
R: Não, a resposta é síncrona (espera o PDF pronto).

**P: Arquivo fica salvo no servidor?**
R: Não, é deletado automaticamente após download.

**P: Posso testar sem certificado SSL?**
R: Sim, use `-k` (curl) ou `verify=False` (Python).

---

## 🆘 Suporte

- **Endpoint DOWN:** Verifique `sudo systemctl status docs-vert`
- **Lenta:** Veja recursos da VPS com `free -h` e `top`
- **Arquivo muito grande:** Limite é 100MB (ajustável em `pyproject.toml`)
