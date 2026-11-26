VALID_ROLES = ("admin", "client")


def demand_session(session: dict) -> None:
    if not isinstance(session, dict):
        raise PermissionError("Please log in.")
    if session.get("role") not in VALID_ROLES:
        raise PermissionError("Access denied.")
    user_id = session.get("id")
    if type(user_id) is not int or user_id <= 0:
        raise PermissionError("Invalid session.")


def require_admin(session: dict) -> None:
    demand_session(session)
    if session["role"] != "admin":
        raise PermissionError("Administrator privileges required.")


def get_field(data, field: str, default=None):
    if data is None:
        return default
    if isinstance(data, dict):
        return data.get(field, default)
    return getattr(data, field, default)