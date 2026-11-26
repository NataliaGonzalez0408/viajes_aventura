from src.persistence.conexion import get_engine, open_connection
from src.services.authentication import create_hash


def seed_data():
    connection = open_connection()
    cursor = connection.cursor()

    try:
        # 1. Check if the database already has data (Idempotency)
        cursor.execute("SELECT COUNT(*) FROM users;")
        if cursor.fetchone()[0] > 0:
            print("The database already contains records. Seeding skipped.")
            return

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
        cursor.executemany(
            f"INSERT INTO users (name, email, password_hash, role) VALUES ({ph}, {ph}, {ph}, {ph});",
            users,
        )

        # 3. Insert Destinations (name, description, base_cost)
        destinations = [
            (
                "San Pedro de Atacama",
                "Desert landscapes, salt flats, and geysers in northern Chile.",
                120000.0,
            ),
            (
                "Torres del Paine",
                "Granite peaks, glaciers, and trekking routes in Patagonia.",
                210000.0,
            ),
            (
                "Valle del Elqui",
                "Stargazing tours, pisco distilleries, and scenic valleys.",
                95000.0,
            ),
            (
                "Chiloé Island",
                "Wooden churches, palafitos, and coastal culture.",
                110000.0,
            ),
            (
                "Rapa Nui",
                "Moai statues, volcanic craters, and Polynesian heritage.",
                280000.0,
            ),
        ]
        cursor.executemany(
            f"INSERT INTO destinations (name, description, base_cost) VALUES ({ph}, {ph}, {ph});",
            destinations,
        )

        # 4. Insert Packages (name, start_date, end_date, total_price, available_spots)
        packages = [
            (
                "Northern Adventure",
                "2026-12-01",
                "2026-12-05",
                450000.0,
                15,
            ),
            (
                "Patagonia Explorer",
                "2026-12-10",
                "2026-12-16",
                780000.0,
                10,
            ),
            (
                "Mystic South",
                "2026-12-15",
                "2026-12-18",
                320000.0,
                12,
            ),
            (
                "Polynesian Escape",
                "2026-12-20",
                "2026-12-25",
                950000.0,
                8,
            ),
        ]
        cursor.executemany(
            f"INSERT INTO packages (name, start_date, end_date, total_price, available_spots) VALUES ({ph}, {ph}, {ph}, {ph}, {ph});",
            packages,
        )

        # 5. Insert Package-Destination Assignments (package_id, destination_id)
        package_destinations = [
            (1, 1),  # Northern Adventure -> Atacama
            (1, 3),  # Northern Adventure -> Elqui
            (2, 2),  # Patagonia Explorer -> Torres del Paine
            (3, 4),  # Mystic South -> Chiloé
            (4, 5),  # Polynesian Escape -> Rapa Nui
        ]
        cursor.executemany(
            f"INSERT INTO package_destinations (package_id, destination_id) VALUES ({ph}, {ph});",
            package_destinations,
        )

        # 6. Insert Reservations (user_id, package_id, reservation_date, status, passenger_count, travel_stage)
        reservations = [
            (3, 1, "2026-11-10", "confirmed", 2, "pending"),
            (4, 2, "2026-11-12", "confirmed", 1, "pending"),
            (5, 3, "2026-11-15", "confirmed", 3, "pending"),
            (3, 4, "2026-11-20", "cancelled", 1, "pending"),
        ]
        cursor.executemany(
            f"INSERT INTO reservations (user_id, package_id, reservation_date, status, passenger_count, travel_stage) VALUES ({ph}, {ph}, {ph}, {ph}, {ph}, {ph});",
            reservations,
        )

        connection.commit()
        print("Data successfully seeded into the database.")

    finally:
        cursor.close()
        connection.close()