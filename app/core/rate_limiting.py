from slowapi import Limiter
from slowapi.util import get_remote_address

# Rate limiter global
limiter = Limiter(key_func=get_remote_address)

# Limites padrão
DEFAULT_RATE_LIMIT = "10/minute"  # 10 requisições por minuto
CONVERSION_RATE_LIMIT = "10/minute"  # 10 conversões por minuto
API_KEY_RATE_LIMIT = "3/hour"  # 3 gerações de key por hora
