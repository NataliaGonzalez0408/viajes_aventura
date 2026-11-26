class Reservation:
    """Represents a user's package reservation, passenger count, and travel stage."""

    VALID_STAGES = ("pending", "in_progress", "completed")

    def __init__(
        self,
        id: int | None,
        user_id: int,
        package_id: int,
        reservation_date: str,
        status: str = "confirmed",
        passenger_count: int = 1,
        travel_stage: str = "pending",
    ):
        if passenger_count < 1:
            raise ValueError("La reserva debe incluir al menos 1 pasajero.")
        if status not in ("confirmed", "cancelled"):
            raise ValueError("El estado debe ser 'confirmed' o 'cancelled'.")
        if travel_stage not in self.VALID_STAGES:
            raise ValueError(f"Etapa de viaje inválida: {travel_stage}")

        self.id = id
        self.user_id = user_id
        self.package_id = package_id
        self.reservation_date = reservation_date
        self.status = status
        self.passenger_count = passenger_count
        self.travel_stage = travel_stage

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

    def update_stage(self, new_stage: str) -> None:
        """Updates the travel stage of an active reservation."""
        if self.status != "confirmed":
            raise ValueError("No se puede actualizar la etapa de una reserva cancelada.")
        if new_stage not in self.VALID_STAGES:
            raise ValueError(f"Etapa de viaje inválida: {new_stage}")
        self.travel_stage = new_stage

    def is_active(self) -> bool:
        """Checks if the reservation is currently confirmed."""
        return self.status == "confirmed"

    def to_tuple(self) -> tuple:
        """Returns reservation attributes as a tuple for database insertion."""
        return (
            self.user_id,
            self.package_id,
            self.reservation_date,
            self.status,
            self.passenger_count,
            self.travel_stage,
        )