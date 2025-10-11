import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta

from src.config import settings




class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, password:str, hashed_password:str)->str:
        return self.pwd_context.verify(password, hashed_password)

    def create_access_token(self,data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def hash_password(self, password):
        return self.pwd_context.hash(password)

    def decode_token(self, token)->str:
        try:
                return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Invalid token")
