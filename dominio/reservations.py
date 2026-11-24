class Reservation:
    """Represents a user's package reservation and manages its status."""

    def __init__(
        self,
        id: int | None,
        user_id: int,
        package_id: int,
        reservation_date: str,
        status: str = "confirmed",
    ):
        self.id = id
        self.user_id = user_id
        self.package_id = package_id
        self.reservation_date = reservation_date
        self.status = status  # 'confirmed' or 'cancelled'

    def confirm(self) -> None:
        """Sets the reservation status to confirmed."""
        if self.status == "confirmed":
            raise ValueError("The reservation is already confirmed.")
        self.status = "confirmed"

    def cancel(self) -> None:
        """Cancels the reservation if it is not already cancelled."""
        if self.status == "cancelled":
            raise ValueError("The reservation is already cancelled.")
        self.status = "cancelled"

    def is_active(self) -> bool:
        """Checks if the reservation is currently confirmed."""
        return self.status == "confirmed"

    def to_tuple(self) -> tuple:
        """Returns reservation attributes as a tuple for database insertion."""
        return (self.user_id, self.package_id, self.reservation_date, self.status)