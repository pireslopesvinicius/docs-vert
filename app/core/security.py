import secrets
import os
from pathlib import Path

# Token master - salvo em variável de ambiente ou arquivo
TOKEN_FILE = Path(__file__).parent.parent.parent / ".token"


def get_or_create_master_token() -> str:
    """
    Obtém ou cria o token master
    
    Returns:
        O token master
    """
    # Tenta obter de variável de ambiente
    env_token = os.getenv("DOCS_VERT_TOKEN")
    if env_token:
        return env_token
    
    # Tenta carregar do arquivo
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'r') as f:
            return f.read().strip()
    
    # Gera novo token
    token = f"docs-vert-{secrets.token_urlsafe(32)}"
    
    # Salva no arquivo
    with open(TOKEN_FILE, 'w') as f:
        f.write(token)
    
    # Mostra na tela para copiar
    print("\n" + "="*80)
    print("🔐 TOKEN MASTER GERADO")
    print("="*80)
    print(f"Token: {token}")
    print("\nUse este token em todas as requisições no header 'x-api-key'")
    print("="*80 + "\n")
    
    return token


def validate_token(token: str, master_token: str) -> bool:
    """
    Valida o token
    
    Args:
        token: Token enviado
        master_token: Token master
        
    Returns:
        True se válido
    """
    return token == master_token


# Carrega token master na inicialização
MASTER_TOKEN = get_or_create_master_token()

