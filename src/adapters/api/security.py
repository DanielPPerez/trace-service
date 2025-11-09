# src/adapters/api/security.py
import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.config import settings

# Esta URL es ficticia. Le dice a Swagger UI dónde debe ir el cliente para obtener un token.
# Aunque nuestro servicio no emite tokens, sí los valida.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No se pudieron validar las credenciales",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> uuid.UUID:
    """
    Decodifica el token JWT para obtener el ID del usuario.
    Esta función es una dependencia de FastAPI que se puede inyectar en los endpoints.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise CREDENTIALS_EXCEPTION
            
        # Convierte el string del ID a un objeto UUID
        user_id = uuid.UUID(user_id_str)
        
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    except (ValueError, TypeError): # Error al convertir a UUID
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El ID de usuario en el token es inválido."
        )
        
    return user_id