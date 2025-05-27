from starlette.authentication import AuthenticationBackend, AuthenticationError, \
    SimpleUser
from infrastructure.security.middleware.exception.auth_exception import \
    TokenAuthException
from infrastructure.security.token.requester import TokenRequester


class TokenAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        try:
            token = request.headers["Authorization"]
        except KeyError as exc:
            raise TokenAuthException(
                detail='Empty headers, fill token in Authorization key',
                status_code=400
            )

        tr = TokenRequester()
        validate, payload = tr.request_for_validate(token)

        if not validate:
            raise TokenAuthException(
                detail='Invalid JWT Token.',
                status_code=400
            )
        return None, SimpleUser(username=payload['user_identifier'])