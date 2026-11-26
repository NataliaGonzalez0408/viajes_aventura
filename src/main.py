import getpass

from src.menus.admin_menu import show_admin_menu
from src.menus.client_menu import show_client_menu
from src.persistence.create_bd import create_tables
from src.persistence.seed_bd import seed_data
from src.services.authentication import authenticate, register_user


def initialize_system():
    create_tables()
    seed_data()


def handle_login() -> dict | None:
    print("\n--- LOGIN ---")
    email = input("Email: ").strip()
    password = getpass.getpass("Password: ")

    session = authenticate(email, password)
    if session is None:
        print("Invalid email or password.")
        return None

    print(f"\nWelcome, {session['name']} ({session['role']})!")
    return session


def handle_register():
    print("\n--- REGISTER NEW ACCOUNT ---")
    name = input("Full Name: ").strip()
    email = input("Email: ").strip()
    password = getpass.getpass("Password: ")

    try:
        user_id = register_user(name, email, password)
        print(f"Account created successfully (ID: {user_id}). You can now log in.")
    except ValueError as e:
        print(f"Registration error: {e}")


def run_session_menu(session: dict):
    """Routes the authenticated user to the appropriate role-based menu."""
    role = session.get("role")
    if role == "admin":
        show_admin_menu(session)
    elif role == "client":
        show_client_menu(session)
    else:
        print("Unrecognized role. Logging out.")


def main():
    initialize_system()
    running = True

    while running:
        print("\n==============================")
        print("   TRAVEL AGENCY SYSTEM")
        print("==============================")
        print("1. Log in")
        print("2. Register")
        print("3. Exit")

        option = input("Select an option: ").strip()

        if option == "1":
            session = handle_login()
            if session:
                run_session_menu(session)
        elif option == "2":
            handle_register()
        elif option == "3":
            print("Goodbye!")
            running = False
        else:
            print("Invalid option. Please try again.")
            
if __name__ == "__main__":
    main()            