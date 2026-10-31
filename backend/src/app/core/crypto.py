"""Symmetric encryption for refresh tokens stored in the database."""

from __future__ import annotations

from cryptography.fernet import Fernet, InvalidToken

from app.core.errors import DomainError


def _cipher(key: str) -> Fernet:
    return Fernet(key.encode())


def encrypt(key: str, plaintext: str) -> bytes:
    """Encrypt a secret for storage.

    Args:
        key: URL-safe base64 Fernet key.
        plaintext: Value to protect.

    Returns:
        Ciphertext suitable for a binary column.

    Raises:
        DomainError: If the configured key is not a valid Fernet key.
    """
    try:
        return _cipher(key).encrypt(plaintext.encode())
    except (ValueError, TypeError) as exc:
        raise DomainError("token encryption key is not a valid Fernet key") from exc


def decrypt(key: str, token: bytes) -> str:
    """Decrypt a stored secret.

    Args:
        key: URL-safe base64 Fernet key.
        token: Ciphertext produced by :func:`encrypt`.

    Returns:
        The original plaintext.

    Raises:
        DomainError: If the key is invalid or the ciphertext was tampered with.
    """
    try:
        return _cipher(key).decrypt(token).decode()
    except (InvalidToken, ValueError, TypeError) as exc:
        raise DomainError("stored token cannot be decrypted with the current key") from exc
