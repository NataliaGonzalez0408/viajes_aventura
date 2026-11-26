from src.domain.destinations import Destination
from src.domain.packages import Package
from src.persistence.conexion import get_connection


class PackagesDAO:
    """Data Access Object for Package entities and package-destination links."""

    def _row_to_package(self, row) -> Package:
        return Package(
            id=row["id"],
            name=row["name"],
            start_date=row["start_date"],
            end_date=row["end_date"],
            total_price=row["total_price"],
            available_spots=row["available_spots"],
        )

    def create(self, package: Package, destination_ids: list[int]) -> Package:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO packages (name, start_date, end_date, total_price, available_spots)
                VALUES (?, ?, ?, ?, ?);
                """,
                package.to_tuple(),
            )
            package.id = cursor.lastrowid
            for dest_id in destination_ids:
                cursor.execute(
                    """
                    INSERT INTO package_destinations (package_id, destination_id)
                    VALUES (?, ?);
                    """,
                    (package.id, dest_id),
                )
            conn.commit()
        return package

    def get_all(self) -> list[Package]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM packages ORDER BY id;")
            rows = cursor.fetchall()
        return [self._row_to_package(row) for row in rows]

    def get_by_id(self, package_id: int) -> Package | None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM packages WHERE id = ?;", (package_id,))
            row = cursor.fetchone()
        return self._row_to_package(row) if row else None

    def get_destinations_for_package(self, package_id: int) -> list[Destination]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT d.*
                FROM destinations d
                INNER JOIN package_destinations pd ON pd.destination_id = d.id
                WHERE pd.package_id = ?
                ORDER BY pd.id;
                """,
                (package_id,),
            )
            rows = cursor.fetchall()
        return [
            Destination(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                base_cost=row["base_cost"],
            )
            for row in rows
        ]

    def update_spots(self, package_id: int, new_spots: int) -> None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE packages SET available_spots = ? WHERE id = ?;",
                (new_spots, package_id),
            )
            conn.commit()
