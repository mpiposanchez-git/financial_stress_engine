from __future__ import annotations

import os

from fastapi import Depends, HTTPException, status

from .auth import AuthContext, require_auth


def _premium_subject_allowlist() -> set[str]:
    raw = os.getenv("PREMIUM_SUBJECT_ALLOWLIST", "")
    return {subject.strip() for subject in raw.split(",") if subject.strip()}


def is_premium(auth: AuthContext) -> bool:
    return auth.subject in _premium_subject_allowlist()


def require_premium(auth: AuthContext = Depends(require_auth)) -> AuthContext:
    if not is_premium(auth):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium entitlement required",
        )
    return auth
