from src.domain.destinations import Destination


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
        if not name or not name.strip():
            raise ValueError("Package name cannot be empty.")
        if end_date < start_date:
            raise ValueError("End date cannot be earlier than start date.")
        if total_price < 0:
            raise ValueError("Total price cannot be negative.")
        if available_spots < 0:
            raise ValueError("Available spots cannot be negative.")

        self.id = id
        self.name = name.strip()
        self.start_date = start_date
        self.end_date = end_date
        self.total_price = total_price
        self.available_spots = available_spots

    def calculate_total_price(self, destinations: list[Destination]) -> float:
        """Calculates and updates the package total price based on its destinations."""
        self.total_price = sum(dest.base_cost for dest in destinations)
        return self.total_price

    def validate_itinerary(self, destinations: list[Destination]) -> None:
        """Validates that the package has at least 2 destinations."""
        if len(destinations) < 2:
            raise ValueError("A package must include at least 2 destinations.")

    def has_available_spots(self, quantity: int = 1) -> bool:
        """Checks if there are enough spots available in the package."""
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        return self.available_spots >= quantity

    def reserve_spot(self, quantity: int = 1) -> None:
        """Decrements available spots by quantity if enough spots are available."""
        if not self.has_available_spots(quantity):
            raise ValueError("Not enough spots available for this package.")
        self.available_spots -= quantity

    def release_spots(self, quantity: int = 1) -> None:
        """Increments available spots by quantity (e.g., when a reservation is cancelled)."""
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        self.available_spots += quantity

    def to_tuple(self) -> tuple:
        """Returns package attributes as a tuple for database insertion."""
        return (
            self.name,
            self.start_date,
            self.end_date,
            self.total_price,
            self.available_spots,
        )