from infrastructure.security.token.exception.verify_exception import \
    TokenExpired, TokenDifferentAppId
from infrastructure.security.token.token import Token
import logging

logger = logging.getLogger("root")

class TokenVerifyProvider:

    @classmethod
    def verify(
            cls,
            token: str,
            token_requester
    ) -> bool:
        validate, payload = token_requester.request_for_validate(token)
        return validate