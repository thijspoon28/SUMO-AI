from app.auth.schemas.jwt import TokensSchema
from app.user.services.user import UserService
from core.helpers.token import token_checker
from core.helpers.token import TokenHelper
from core.exceptions.base import UnauthorizedException
from core.helpers.hashids import encode, decode_single
from sqlalchemy.orm import Session


class JwtService:
    def __init__(self, session: Session):
        self.user_serv = UserService(session)

    async def create_login_tokens(self, user_id: int):
        enc_user_id = encode(user_id)

        at_payload = {"user_id": enc_user_id}
        rt_payload = {"user_id": enc_user_id}

        if await self.user_serv.is_admin(user_id):
            at_payload["is_admin"] = True

        return TokensSchema(
            access_token=TokenHelper.encode_access(payload=at_payload),
            refresh_token=TokenHelper.encode_refresh(payload=rt_payload),
        )

    async def refresh_tokens(
        self,
        refresh_token: str,
    ) -> TokensSchema:
        refresh_token = TokenHelper.decode(token=refresh_token)

        user_id = decode_single(refresh_token.get("user_id"))
        enc_user_id = encode(user_id)

        at_payload = {"user_id": enc_user_id}
        rt_payload = {"user_id": enc_user_id}

        if await self.user_serv.is_admin(user_id):
            at_payload["is_admin"] = True

        try:
            jti = token_checker.generate_add(refresh_token.get("jti"))

        except (ValueError, KeyError) as exc:
            raise UnauthorizedException from exc

        rt_payload["jti"] = jti

        return TokensSchema(
            access_token=TokenHelper.encode_access(payload={"user_id": enc_user_id}),
            refresh_token=TokenHelper.encode_refresh(payload=rt_payload),
        )
