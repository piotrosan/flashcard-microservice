from starlette.authentication import AuthenticationBackend

from infrastructure.database.sql.models.auth import User
from infrastructure.security.middleware.exception.auth_exception import \
    TokenAuthException
from infrastructure.security.token.requester import TokenRequester


class TokenAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        try:
            token = request.headers["Authorization"]
        except KeyError as exc:
            return None, None

        tr = TokenRequester()
        validate, payload = tr.request_for_validate(token)

        if not validate:
            raise TokenAuthException(
                detail='Invalid JWT Token.',
                status_code=400
            )
        return None, User(hash_identifier=payload['user_identifier'])