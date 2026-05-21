from dataclasses import dataclass
from typing import Annotated, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class Principal:
    subject: str
    tenant_id: str
    scopes: frozenset[str]


DEMO_TOKENS = {
    "partner-demo-token": Principal(
        subject="partner-integration-user",
        tenant_id="tenant_cincinnati",
        scopes=frozenset({"orders:read", "orders:write", "tools:invoke"}),
    ),
    "analyst-demo-token": Principal(
        subject="business-analyst",
        tenant_id="tenant_cincinnati",
        scopes=frozenset({"orders:read"}),
    ),
}


def get_principal(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
) -> Principal:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    principal = DEMO_TOKENS.get(credentials.credentials)
    if not principal:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return principal


def require_scopes(*required_scopes: str) -> Callable[[Principal], Principal]:
    def dependency(principal: Annotated[Principal, Depends(get_principal)]) -> Principal:
        missing = set(required_scopes) - set(principal.scopes)
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"message": "Insufficient scope", "missing": sorted(missing)},
            )
        return principal

    return dependency

