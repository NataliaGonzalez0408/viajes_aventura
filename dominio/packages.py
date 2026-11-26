from dominio.destinations import Destination


class Package:
    """Represents a travel package with dates, pricing, and spot availability."""

    def __init__(
        self,
        id: int | None,
        name: str,
        start_date: str,
        end_date: str,
        total_price: float = 0.0,
        available_spots: int = 0,
    ):
        if total_price < 0:
            raise ValueError("Total price cannot be negative.")
        if available_spots < 0:
            raise ValueError("Available spots cannot be negative.")

        self.id = id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.total_price = total_price
        self.available_spots = available_spots

    def calculate_total_price(self, destinations: list[Destination]) -> float:
        """Calculates and updates the package total price based on its destinations."""
        self.total_price = sum(dest.base_cost for dest in destinations)
        return self.total_price

    def has_available_spots(self) -> bool:
        """Checks if there is at least one spot available in the package."""
        return self.available_spots > 0

    def reserve_spot(self) -> None:
        """Decrements available spots by one if spots are available."""
        if not self.has_available_spots():
            raise ValueError("No spots available for this package.")
        self.available_spots -= 1

    def release_spot(self) -> None:
        """Increments available spots by one (e.g., when a reservation is cancelled)."""
        self.available_spots += 1

    def to_tuple(self) -> tuple:
        """Returns package attributes as a tuple for database insertion."""
        return (
            self.name,
            self.start_date,
            self.end_date,
            self.total_price,
            self.available_spots,
        )