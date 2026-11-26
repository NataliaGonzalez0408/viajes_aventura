from services.package_service import get_package_details, list_packages
from services.permissions import demand_session
from services.reservation_service import cancel_my_reservation, create_reservation, list_reservations_by_user


def show_client_menu(session: dict):
    demand_session(session)
    active = True

    while active:
        print("\n====================================")
        print(f"   CLIENT MENU - {session['name']}")
        print("====================================")
        print("1. Browse Available Packages")
        print("2. View Package Itinerary (Destinations & Dates)")
        print("3. Book a Package")
        print("4. My Reservations")
        print("5. Cancel a Reservation")
        print("6. Log out")

        option = input("Select an option: ").strip()

        try:
            if option == "1":
                _browse_packages()
            elif option == "2":
                _view_package_itinerary()
            elif option == "3":
                _book_package(session)
            elif option == "4":
                _view_my_reservations(session)
            elif option == "5":
                _cancel_reservation(session)
            elif option == "6":
                print("Logging out...")
                active = False
            else:
                print("Invalid option. Please try again.")
        except (ValueError, PermissionError) as e:
            print(f"\n[Error]: {e}")


def _browse_packages():
    print("\n--- AVAILABLE TRAVEL PACKAGES ---")
    packages = list_packages()
    if not packages:
        print("No packages available at the moment.")
        return

    for p in packages:
        print(f"[{p.id}] {p.name} - ${p.price:,.2f}")
        print(f"    {p.description}")


def _view_package_itinerary():
    package_id = int(input("\nEnter Package ID to view details: ").strip())
    details = get_package_details(package_id)

    print(f"\nPackage: {details['name']} (${details['price']:,.2f})")
    print(f"Description: {details['description']}")
    print("Included Destinations:")
    if not details["destinations"]:
        print("  - No destinations assigned yet.")
    for item in details["destinations"]:
        print(
            f"  * {item['destination_name']} ({item['start_date']} to"
            f" {item['end_date']})"
        )


def _book_package(session: dict):
    print("\n--- BOOK A PACKAGE ---")
    package_id = int(input("Enter Package ID to book: ").strip())
    res_id = create_reservation(session, package_id)
    print(f"Reservation created! Your reservation ID is {res_id}.")


def _view_my_reservations(session: dict):
    print("\n--- MY RESERVATIONS ---")
    reservations = list_reservations_by_user(session)
    if not reservations:
        print("You have no reservations yet.")
        return

    for r in reservations:
        print(
            f"Reservation #{r.id} | Package ID: {r.package_id} "
            f"| Date: {r.reservation_date} | Status: {r.status}"
        )


def _cancel_reservation(session: dict):
    res_id = int(input("\nEnter Reservation ID to cancel: ").strip())
    cancel_my_reservation(session, res_id)
    print(f"Reservation #{res_id} has been cancelled.")