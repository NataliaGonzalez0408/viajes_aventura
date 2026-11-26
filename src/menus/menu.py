from src.menus.admin_menu import show_admin_menu
from src.menus.client_menu import show_client_menu
from src.menus.login_menu import show_login_menu


def run_menu(initial_session: dict | None = None) -> None:
    """Dispatches between login, admin menu, and client menu based on session role."""
    session = initial_session

    while True:
        if session is None:
            session = show_login_menu()
            if session is None:
                break

        role = session.get("role")
        try:
            if role == "admin":
                show_admin_menu(session)
            elif role == "client":
                show_client_menu(session)
            else:
                raise PermissionError("Unsupported user role in session.")
        except (ValueError, PermissionError) as e:
            print(f"\n[Error]: {e}")

        session = None