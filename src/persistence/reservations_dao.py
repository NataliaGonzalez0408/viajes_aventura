from src.domain.reservations import Reservation
from src.persistence.conexion import get_connection


class ReservationsDAO:
    """Data Access Object for Reservation entities."""

    def _row_to_entity(self, row) -> Reservation:
        return Reservation(
            id=row["id"],
            user_id=row["user_id"],
            package_id=row["package_id"],
            reservation_date=row["reservation_date"],
            status=row["status"],
            passenger_count=row["passenger_count"],
            travel_stage=row["travel_stage"],
        )

    def create(self, reservation: Reservation) -> Reservation:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO reservations (
                    user_id, package_id, reservation_date, status, passenger_count, travel_stage
                )
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                reservation.to_tuple(),
            )
            reservation.id = cursor.lastrowid
            conn.commit()
        return reservation

    def get_by_user(self, user_id: int) -> list[Reservation]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM reservations WHERE user_id = ? ORDER BY id DESC;",
                (user_id,),
            )
            rows = cursor.fetchall()
        return [self._row_to_entity(row) for row in rows]

    def get_all(self) -> list[Reservation]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reservations ORDER BY id DESC;")
            rows = cursor.fetchall()
        return [self._row_to_entity(row) for row in rows]

    def get_by_id(self, res_id: int) -> Reservation | None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reservations WHERE id = ?;", (res_id,))
            row = cursor.fetchone()
        return self._row_to_entity(row) if row else None

    def update_status(self, res_id: int, status: str) -> None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE reservations SET status = ? WHERE id = ?;",
                (status, res_id),
            )
            conn.commit()

    def update_stage(self, res_id: int, stage: str) -> None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE reservations SET travel_stage = ? WHERE id = ?;",
                (stage, res_id),
            )
            conn.commit()