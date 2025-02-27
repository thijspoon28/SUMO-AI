from app.auth.schemas.jwt import RefreshTokenSchema, TokensSchema
from app.auth.schemas.auth import LoginSchema
from app.auth.services.jwt import JwtService
from app.auth.services.utils import verify_password
from app.auth.exceptions.auth import BadCredentialsException
from app.user.services.user import UserService
from sqlalchemy.orm import Session


class AuthService:
    def __init__(self, session: Session) -> None:
        self.user_serv = UserService(session)
        self.jwt_serv = JwtService(session)

    async def login(self, schema: LoginSchema) -> TokensSchema:
        user = await self.user_serv.get_by_username(schema.username)
        if not user:
            raise BadCredentialsException()
        if not verify_password(schema.password, user.password):
            raise BadCredentialsException()
        
        return await self.jwt_serv.create_login_tokens(user_id=user.id)

    async def refresh(self, schema: RefreshTokenSchema):
        return await self.jwt_serv.refresh_tokens(refresh_token=schema.refresh_token)
