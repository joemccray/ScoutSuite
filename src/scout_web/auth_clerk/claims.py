from __future__ import annotations
from typing import Dict, Iterable, Optional
from django.conf import settings

class ClaimsPolicyError(Exception):
    pass

def validate_claims(payload: Dict, *, allow_audiences: Optional[Iterable[str]] = None) -> None:
    iss = payload.get("iss")
    if not iss or iss != settings.CLERK_ISSUER:
        raise ClaimsPolicyError("invalid `iss`")
    # `azp` = authorized party (the origin URL that minted the token)
    azp = payload.get("azp")
    if settings.CLERK_AUTHORIZED_PARTIES:
        if not azp or azp not in settings.CLERK_AUTHORIZED_PARTIES:
            raise ClaimsPolicyError("invalid `azp`")
    # optional audience checks if you use custom templates with `aud`
    aud = payload.get("aud")
    if settings.CLERK_ALLOWED_AUDIENCES and aud not in settings.CLERK_ALLOWED_AUDIENCES:
        raise ClaimsPolicyError("invalid `aud`")
