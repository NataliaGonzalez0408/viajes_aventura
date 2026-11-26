from src.domain.destinations import Destination
from src.persistence.conexion import get_connection


class DestinationsDAO:
    """Data Access Object for Destination entities."""

    def _row_to_entity(self, row) -> Destination:
        return Destination(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            base_cost=row["base_cost"],
        )

    def create(self, destination: Destination) -> Destination:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO destinations (name, description, base_cost)
                VALUES (?, ?, ?);
                """,
                (destination.name, destination.description, destination.base_cost),
            )
            destination.id = cursor.lastrowid
            conn.commit()
        return destination

    def get_all(self) -> list[Destination]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM destinations ORDER BY id;")
            rows = cursor.fetchall()
        return [self._row_to_entity(row) for row in rows]

    def get_by_id(self, dest_id: int) -> Destination | None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM destinations WHERE id = ?;", (dest_id,))
            row = cursor.fetchone()
        return self._row_to_entity(row) if row else None

    def update(self, destination: Destination) -> Destination:
        if destination.id is None:
            raise ValueError("Destination ID is required to update.")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE destinations
                SET name = ?, description = ?, base_cost = ?
                WHERE id = ?;
                """,
                (
                    destination.name,
                    destination.description,
                    destination.base_cost,
                    destination.id,
                ),
            )
            conn.commit()
        return destination

    def is_used_in_packages(self, dest_id: int) -> bool:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM package_destinations WHERE destination_id = ?;",
                (dest_id,),
            )
            count = cursor.fetchone()[0]
        return count > 0