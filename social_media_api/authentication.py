from typing import Optional, Tuple

from rest_framework.request import Request
from rest_framework_simplejwt import authentication, tokens

from social_media_user.models import BlacklistedAccessToken


class UserCustomAuthentication(authentication.JWTAuthentication):
    def authenticate(
        self,
        request: Request
    ) -> Optional[Tuple[authentication.AuthUser, tokens.Token]]:

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        raw_token = auth_header.split(" ")[1] if " " in auth_header else auth_header

        if BlacklistedAccessToken.objects.filter(token=raw_token).exists():
            return None

        return super().authenticate(request=request)
