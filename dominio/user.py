import hashlib
import hmac
import os


class User:
    """Represents a system user with secure password hashing and role management."""

    def __init__(
        self,
        id: int | None,
        name: str,
        email: str,
        password_hash: str,
        role: str = "client",
    ):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role  # 'admin' or 'client'

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Hashes a plain-text password using PBKDF2-HMAC-SHA256 with a random salt."""
        salt = os.urandom(16)
        pwd_hash = hashlib.pbkdf2_hmac(
            "sha256", plain_password.encode("utf-8"), salt, 100_000
        )
        return f"{salt.hex()}${pwd_hash.hex()}"

    def verify_password(self, plain_password: str) -> bool:
        """Verifies a plain-text password against the stored salted hash."""
        try:
            salt_hex, hash_hex = self.password_hash.split("$")
            salt = bytes.fromhex(salt_hex)
            expected_hash = bytes.fromhex(hash_hex)

            new_hash = hashlib.pbkdf2_hmac(
                "sha256", plain_password.encode("utf-8"), salt, 100_000
            )
            return hmac.compare_digest(new_hash, expected_hash)
        except ValueError:
            return False

    def is_admin(self) -> bool:
        """Checks if the user has administrator privileges."""
        return self.role == "admin"

    def to_tuple(self) -> tuple:
        """Returns user attributes as a tuple for database insertion."""
        return (self.name, self.email, self.password_hash, self.role)