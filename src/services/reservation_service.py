from dataclasses import dataclass
from datetime import date

from persistence.conexion import open_connection
from services.permissions import require_admin

VALID_STATUSES = ("pending", "confirmed", "cancelled")


def _session_user_id(session: dict) -> int:
    """Obtiene el ID del usuario desde la sesión ('id' o 'user_id')."""
    user_id = session.get("id", session.get("user_id"))
    if user_id is None:
        raise PermissionError("Invalid session: user ID not found.")
    return user_id


def create_reservation(session: dict, package_id: int) -> int:
    """Crea una reserva pendiente para el usuario de la sesión."""
    user_id = _session_user_id(session)

    connection = open_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM packages WHERE id = ?", (package_id,))
        if not cursor.fetchone():
            raise ValueError(f"Package {package_id} does not exist.")

        cursor.execute(
            """
            INSERT INTO reservations (user_id, package_id, reservation_date, status)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, package_id, date.today().isoformat(), "pending"),
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        connection.close()


def list_reservations_by_user(session: dict) -> list[Reservation]:
    """Devuelve las reservas del usuario de la sesión."""
    user_id = _session_user_id(session)

    connection = open_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id, user_id, package_id, reservation_date, status
            FROM reservations
            WHERE user_id = ?
            ORDER BY id
            """,
            (user_id,),
        )
        return [Reservation(*row) for row in cursor.fetchall()]
    finally:
        cursor.close()
        connection.close()


def cancel_my_reservation(session: dict, reservation_id: int) -> None:
    """Cancela una reserva propia que no esté ya cancelada."""
    user_id = _session_user_id(session)

    connection = open_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT status FROM reservations WHERE id = ? AND user_id = ?",
            (reservation_id, user_id),
        )
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Reservation {reservation_id} not found for your account.")
        if row[0] == "cancelled":
            raise ValueError("This reservation is already cancelled.")

        cursor.execute(
            "UPDATE reservations SET status = 'cancelled' WHERE id = ?",
            (reservation_id,),
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def list_all_reservations(session: dict) -> list[Reservation]:
    require_admin(session)

    connection = open_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id, user_id, package_id, reservation_date, status
            FROM reservations
            ORDER BY id
            """
        )
        return [Reservation(*row) for row in cursor.fetchall()]
    finally:
        cursor.close()
        connection.close()


def update_reservation_status(session: dict, reservation_id: int, status: str) -> None:
    require_admin(session)

    status = status.strip().lower()
    if status not in VALID_STATUSES:
        raise ValueError(f"Status must be one of: {', '.join(VALID_STATUSES)}.")

    connection = open_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE reservations SET status = ? WHERE id = ?",
            (status, reservation_id),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"Reservation {reservation_id} does not exist.")
        connection.commit()
    finally:
        cursor.close()
        connection.close()