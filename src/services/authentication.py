import bcrypt
from domain.user import User
from persistence.user_dao import UserDAO
from services.permissions import require_admin

MAX_BYTES_BCRYPT = 72

def create_hash(password: str) -> str:
    password = User.validate_password(password)
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Maximum 72 UTF-8 bytes allowed for bcrypt.")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def register_user(name: str, email: str, password: str) -> int:
    """Public self-registration for standard clients."""
    clean_name = name.strip()
    if not clean_name:
        raise ValueError("User name cannot be empty.")

    normalized_email = User.normalize_email(email)
    if UserDAO.find_by_email(normalized_email) is not None:
        raise ValueError("An account with this email already exists.")

    saved_hash = create_hash(password)

    user = User(
        id=None,
        name=clean_name,
        email=normalized_email,
        password_hash=saved_hash,
        role="client",
    )

    saved_user = UserDAO.insert(user)
    return saved_user.id


def create_user_by_admin(
    current_session: dict,
    name: str,
    email: str,
    password: str,
    role: str = "client",
) -> int:
    """Admin-only user creation allowing custom role assignment (e.g., 'admin' or 'client')."""
    require_admin(current_session)

    clean_name = name.strip()
    if not clean_name:
        raise ValueError("User name cannot be empty.")

    normalized_email = User.normalize_email(email)
    if UserDAO.find_by_email(normalized_email) is not None:
        raise ValueError(f"A user with email '{normalized_email}' already exists.")

    saved_hash = create_hash(password)

    user = User(
        id=None,
        name=clean_name,
        email=normalized_email,
        password_hash=saved_hash,
        role=role,
    )

    saved_user = UserDAO.insert(user)
    return saved_user.id


def authenticate(email: str, password: str) -> dict | None:
    normalized_email = User.normalize_email(email)
    if not isinstance(password, str):
        return None

    password_bytes = password.encode("utf-8")
    if not 0 < len(password_bytes) <= MAX_BYTES_BCRYPT:
        return None

    account = UserDAO.find_by_email(normalized_email)
    if account is None:
        return None

    if not bcrypt.checkpw(password_bytes, account.password_hash.encode("utf-8")):
        return None

    return {
        "id": account.id,
        "name": account.name,
        "email": account.email,
        "role": account.role,
}