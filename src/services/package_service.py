from dataclasses import dataclass
from datetime import datetime

from src.persistence.conexion import open_connection
from src.services.permissions import require_admin


@dataclass
class Package:
    id: int
    name: str
    description: str
    price: float


def _validate_date(value: str, label: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"{label} must have the format YYYY-MM-DD.")
    return value


def create_package(session: dict, name: str, description: str, price: float) -> int:
    require_admin(session)

    name = name.strip()
    description = description.strip()
    if not name:
        raise ValueError("Package name cannot be empty.")
    if price <= 0:
        raise ValueError("Price must be greater than zero.")

    connection = open_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO packages (name, description, price) VALUES (?, ?, ?)",
            (name, description, price),
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        connection.close()


def list_packages() -> list[Package]:
    """Devuelve todos los paquetes disponibles."""
    connection = open_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT id, name, description, price FROM packages ORDER BY id"
        )
        return [Package(*row) for row in cursor.fetchall()]
    finally:
        cursor.close()
        connection.close()


def assign_destination_to_package(
    session: dict,
    package_id: int,
    destination_id: int,
    start_date: str,
    end_date: str,
) -> int:
    """Asigna un destino a un paquete con sus fechas. Solo administradores."""
    require_admin(session)

    start_date = _validate_date(start_date, "Start date")
    end_date = _validate_date(end_date, "End date")
    if end_date < start_date:
        raise ValueError("End date cannot be before start date.")

    connection = open_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM packages WHERE id = ?", (package_id,))
        if not cursor.fetchone():
            raise ValueError(f"Package {package_id} does not exist.")

        cursor.execute("SELECT id FROM destinations WHERE id = ?", (destination_id,))
        if not cursor.fetchone():
            raise ValueError(f"Destination {destination_id} does not exist.")

        cursor.execute(
            """
            INSERT INTO package_destinations
                (package_id, destination_id, start_date, end_date)
            VALUES (?, ?, ?, ?)
            """,
            (package_id, destination_id, start_date, end_date),
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        connection.close()


def get_package_details(package_id: int) -> dict:
    """Devuelve un paquete con sus destinos y fechas."""
    connection = open_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT id, name, description, price FROM packages WHERE id = ?",
            (package_id,),
        )
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Package {package_id} does not exist.")

        cursor.execute(
            """
            SELECT d.name, pd.start_date, pd.end_date
            FROM package_destinations pd
            JOIN destinations d ON d.id = pd.destination_id
            WHERE pd.package_id = ?
            ORDER BY pd.start_date
            """,
            (package_id,),
        )
        destinations = [
            {
                "destination_name": name,
                "start_date": start_date,
                "end_date": end_date,
            }
            for name, start_date, end_date in cursor.fetchall()
        ]

        return {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": row[3],
            "destinations": destinations,
        }
    finally:
        cursor.close()
        connection.close()