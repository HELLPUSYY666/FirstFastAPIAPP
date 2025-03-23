import datetime
from dataclasses import dataclass
from jose import jwt, JWTError
from exception import UserNotFoundException, UserNotCorrectPasswordException, TokenExpiredException, \
    TokenNotCorrectException
from models import UserProfile
from repository import UserRepository
from schema import UserLoginSchema
from datetime import timedelta
from settings import settings


@dataclass
class AuthService:
    user_repository: UserRepository

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = (datetime.datetime.utcnow() + timedelta(days=7)).timestamp()
        token = jwt.encode(
            {"user_id": user_id, "expire": expires_date_unix},
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ENCODE_ALGORITHM
        )
        return token

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(access_token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ENCODE_ALGORITHM])
        except JWTError:
            raise TokenNotCorrectException
        if payload["expire"] < (datetime.datetime.utcnow().timestamp()):
            raise TokenExpiredException
        return payload["user_id"]
