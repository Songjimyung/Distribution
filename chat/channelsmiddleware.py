from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware


@database_sync_to_async
def get_user(token_key):
    """
    작성자 : 박지홍
    내용 : 비동기 함수, 토큰 키를 사용하여 사용자를 가져오는 함수.
    최초 작성일 : 2023.06.06
    업데이트 일자 :
    """
    try:
        access_token = AccessToken(token_key)
        user_id = access_token.get("user_id", None)

    except user_id is None:
        return None

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


class TokenAuthMiddleware(BaseMiddleware):
    """
    작성자 : 박지홍
    내용 : 토큰 기반 인증을 위한 미들웨어로 웹 소켓 연결을 처리하기 전 토큰을 통해 유저를 검증한다.
    최초 작성일 : 2023.06.06
    업데이트 일자 :
    """
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token_key = (
                dict((x.split("=") for x in scope["query_string"].decode().split("&")))
            ).get("token", None)

        except ValueError:
            token_key = None
        scope["user"] = None if token_key is None else await get_user(token_key)

        return await super().__call__(scope, receive, send)
