from persistence.conexion import get_engine, open_connection
from services.authentication import create_hash


def seed_data():
  connection = open_connection()
  cursor = connection.cursor()

  try:
    # 1. Check if the database already has data (Idempotency)
    cursor.execute("SELECT COUNT(*) FROM users;")
    if cursor.fetchone()[0] > 0:
      print("The database already contains records. Seeding skipped.")
      return

    # Determine the query placeholder based on the DB engine (? for SQLite, %s for MySQL/PostgreSQL)
    engine = get_engine()
    ph = "?" if engine == "sqlite" else "%s"

    # 2. Insert Users
    pass_hash = create_hash("Admin123*")
    users = [
        ("Juan Martínez", "juan.martinez@travel.com", pass_hash, "admin"),
        ("María García", "maria.garcia@travel.com", pass_hash, "admin"),
        ("Pedro Rodríguez", "pedro.rodriguez@travel.com", pass_hash, "client"),
        ("Ana López", "ana.lopez@travel.com", pass_hash, "client"),
        ("Carlos Pérez", "carlos.perez@travel.com", pass_hash, "client"),
    ]
    sql_users = f"INSERT INTO users (name, email, password_hash, role) VALUES ({ph}, {ph}, {ph}, {ph});"
    cursor.executemany(sql_users, users)

    # 3. Insert Destinations
    destinations = [
        (
            "San Pedro de Atacama",
            "Desert landscapes, salt flats, and geysers in northern Chile.",
        ),
        (
            "Torres del Paine",
            "Granite peaks, glaciers, and trekking routes in Patagonia.",
        ),
        (
            "Valle del Elqui",
            "Stargazing tours, pisco distilleries, and scenic valleys.",
        ),
        ("Chiloé Island", "Wooden churches, palafitos, and coastal culture."),
        (
            "Rapa Nui",
            "Moai statues, volcanic craters, and Polynesian heritage.",
        ),
    ]
    sql_destinations = (
        f"INSERT INTO destinations (name, description) VALUES ({ph}, {ph});"
    )
    cursor.executemany(sql_destinations, destinations)

    # 4. Insert Packages
    packages = [
        (
            "Northern Adventure",
            "5-day all-inclusive desert and stargazing experience.",
            450000.0,
        ),
        (
            "Patagonia Explorer",
            "7-day guided trekking and glacier tour.",
            780000.0,
        ),
        (
            "Mystic South",
            "4-day cultural and gastronomic island getaway.",
            320000.0,
        ),
        (
            "Polynesian Escape",
            "6-day archaeological and beach expedition.",
            950000.0,
        ),
    ]
    sql_packages = (
        f"INSERT INTO packages (name, description, price) VALUES ({ph}, {ph},"
        f" {ph});"
    )
    cursor.executemany(sql_packages, packages)

    # 5. Insert Package-Destination Assignments (Junction Table)
    # (package_id, destination_id, start_date, end_date)
    package_destinations = [
        (1, 1, "2026-12-01", "2026-12-03"),  # Northern Adventure -> Atacama
        (1, 3, "2026-12-04", "2026-12-05"),  # Northern Adventure -> Elqui
        (
            2,
            2,
            "2026-12-10",
            "2026-12-16",
        ),  # Patagonia Explorer -> Torres del Paine
        (3, 4, "2026-12-15", "2026-12-18"),  # Mystic South -> Chiloé
        (4, 5, "2026-12-20", "2026-12-25"),  # Polynesian Escape -> Rapa Nui
    ]
    sql_pkg_dest = (
        "INSERT INTO package_destinations "
        "(package_id, destination_id, start_date, end_date) "
        f"VALUES ({ph}, {ph}, {ph}, {ph});"
    )
    cursor.executemany(sql_pkg_dest, package_destinations)

    # 6. Insert Reservations
    # (user_id, package_id, reservation_date, status)
    reservations = [
        (3, 1, "2026-11-10", "confirmed"),
        (4, 2, "2026-11-12", "pending"),
        (5, 3, "2026-11-15", "confirmed"),
        (3, 4, "2026-11-20", "cancelled"),
    ]
    sql_reservations = (
        "INSERT INTO reservations "
        "(user_id, package_id, reservation_date, status) "
        f"VALUES ({ph}, {ph}, {ph}, {ph});"
    )
    cursor.executemany(sql_reservations, reservations)

    connection.commit()
    print("Data successfully seeded into the database.")

  finally:
    cursor.close()
    connection.close()