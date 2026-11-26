import getpass
from src.services.authentication import create_user_by_admin
from src.services.destination_service import create_destination, list_destinations
from src.services.package_service import assign_destination_to_package, create_package, list_packages
from src.services.permissions import require_admin
from src.services.reservation_service import list_all_reservations, update_reservation_status

def show_admin_menu(session: dict):
    require_admin(session)

    while True:
        print("\n====================================")
        print(f"   ADMIN PANEL - {session['name']}")
        print("====================================")
        print("1. Manage Destinations (Create / List)")
        print("2. Manage Packages (Create / List)")
        print("3. Assign Destination to a Package")
        print("4. View All Reservations")
        print("5. Update Reservation Status")
        print("6. Create New User (Admin / Client)")
        print("7. Log out")

        option = input("Select an option: ").strip()

        try:
            if option == "1":
                _manage_destinations(session)
            elif option == "2":
                _manage_packages(session)
            elif option == "3":
                _assign_destination(session)
            elif option == "4":
                _view_all_reservations(session)
            elif option == "5":
                _update_reservation(session)
            elif option == "6":
                _create_user(session)
            elif option == "7":
                print("Logging out from Admin Panel...")
                break
            else:
                print("Invalid option. Please try again.")
        except (ValueError, PermissionError) as e:
            print(f"\n[Error]: {e}")


def _manage_destinations(session: dict):
    print("\n--- DESTINATIONS ---")
    print("1. List all destinations")
    print("2. Add new destination")
    sub = input("Choose: ").strip()

    if sub == "1":
        destinations = list_destinations()
        if not destinations:
            print("No destinations registered.")
        for d in destinations:
            print(f"[{d.id}] {d.name} - {d.description}")
    elif sub == "2":
        name = input("Destination name: ").strip()
        description = input("Description: ").strip()
        dest_id = create_destination(session, name, description)
        print(f"Destination created successfully (ID: {dest_id}).")
    else:
        print("Invalid option.")


def _manage_packages(session: dict):
    print("\n--- PACKAGES ---")
    print("1. List all packages")
    print("2. Create new package")
    sub = input("Choose: ").strip()

    if sub == "1":
        packages = list_packages()
        if not packages:
            print("No packages registered.")
        for p in packages:
            print(f"[{p.id}] {p.name} (${p.price:,.2f}) - {p.description}")
    elif sub == "2":
        name = input("Package name: ").strip()
        description = input("Description: ").strip()
        price = float(input("Price: ").strip())
        pkg_id = create_package(session, name, description, price)
        print(f"Package created successfully (ID: {pkg_id}).")
    else:
        print("Invalid option.")


def _assign_destination(session: dict):
    print("\n--- ASSIGN DESTINATION TO PACKAGE ---")
    package_id = int(input("Package ID: ").strip())
    destination_id = int(input("Destination ID: ").strip())
    start_date = input("Start date (YYYY-MM-DD): ").strip()
    end_date = input("End date (YYYY-MM-DD): ").strip()

    assign_destination_to_package(
        session, package_id, destination_id, start_date, end_date
    )
    print("Destination assigned to package successfully.")


def _view_all_reservations(session: dict):
    print("\n--- ALL RESERVATIONS ---")
    reservations = list_all_reservations(session)
    if not reservations:
        print("No reservations found.")
    for r in reservations:
        print(
            f"ID: {r.id} | User ID: {r.user_id} | Package ID: {r.package_id} "
            f"| Date: {r.reservation_date} | Status: {r.status}"
        )


def _update_reservation(session: dict):
    print("\n--- UPDATE RESERVATION STATUS ---")
    res_id = int(input("Reservation ID: ").strip())
    status = input("New status (pending / confirmed / cancelled): ").strip()
    update_reservation_status(session, res_id, status)
    print("Reservation status updated.")


def _create_user(session: dict):
    print("\n--- CREATE USER ---")
    name = input("Full Name: ").strip()
    email = input("Email: ").strip()
    password = getpass.getpass("Password: ")
    role = input("Role (admin / client) [client]: ").strip() or "client"

    user_id = create_user_by_admin(session, name, email, password, role)
    print(f"User created successfully (ID: {user_id}, Role: {role}).")