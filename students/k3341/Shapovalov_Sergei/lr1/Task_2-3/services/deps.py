from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.security import verify_token
from typing import Optional

security = HTTPBearer(auto_error=False)


def get_current_user(token: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if token is None:
        # Если токена нет, используем default user_id = 1
        return 1

    try:
        payload = verify_token(token.credentials)
        return payload["user_id"]
    except:
        # Если токен невалидный, также используем default user_id = 1
        return 1
