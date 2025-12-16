"""
Utilidad para generar tokens únicos seguros
"""
import secrets
import string


def generate_share_token(length: int = 16) -> str:
    """
    Genera un token aleatorio seguro para URLs de compartir
    
    Args:
        length: Longitud del token (default: 16 caracteres)
    
    Returns:
        Token alfanumérico seguro
    
    Example:
        >>> generate_share_token()
        'a7B3kD9mP2qR5wX8'
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_short_token(length: int = 8) -> str:
    """
    Genera un token corto para IDs visibles
    
    Args:
        length: Longitud del token (default: 8 caracteres)
    
    Returns:
        Token alfanumérico corto
    """
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
