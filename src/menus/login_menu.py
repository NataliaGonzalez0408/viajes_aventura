import getpass

from src.services.authentication import authenticate, register_user

def show_login_menu() -> dict | None:
    """Shows the login/registration menu and returns an active session dict or None on exit."""
    while True:
        print("\n====================================")
        print("       VIAJES AVENTURA - ACCESS")
        print("====================================")
        print("1. Log in")
        print("2. Register (Client)")
        print("3. Exit")

        option = input("Select an option: ").strip()

        try:
            if option == "1":
                email = input("Email: ").strip()
                password = getpass.getpass("Password: ")
                session = authenticate(email, password)
                if session:
                    print(f"Welcome, {session['name']} ({session['role']}).")
                    return session
                print("Invalid email or password.")
            elif option == "2":
                name = input("Full Name: ").strip()
                email = input("Email: ").strip()
                password = getpass.getpass("Password: ")
                register_user(name, email, password)
                print("Client account registered successfully. You can now log in.")
            elif option == "3":
                print("Exiting application...")
                return None
            else:
                print("Invalid option. Please try again.")
        except ValueError as e:
            print(f"\n[Error]: {e}")