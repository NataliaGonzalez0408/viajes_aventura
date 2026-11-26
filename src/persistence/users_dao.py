from src.domain.users import User
from src.persistence.conexion import get_connection 


class UsersDAO:
    """Data Access Object for User entities."""

    def _row_to_entity(self, row) -> User:
        return User(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            password_hash=row["password_hash"],
            role=row["role"],
        )

    def create(self, user: User) -> User:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (name, email, password_hash, role)
                VALUES (?, ?, ?, ?);
                """,
                (user.name, user.email.strip().lower(), user.password_hash, user.role),
            )
            user.id = cursor.lastrowid
            conn.commit()
        return user

    def get_by_email(self, email: str) -> User | None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE email = ?;",
                (email.strip().lower(),),
            )
            row = cursor.fetchone()
        return self._row_to_entity(row) if row else None

    def get_by_id(self, user_id: int) -> User | None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
            row = cursor.fetchone()
        return self._row_to_entity(row) if row else None

    def get_all(self) -> list[User]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users ORDER BY id;")
            rows = cursor.fetchall()
        return [self._row_to_entity(row) for row in rows]