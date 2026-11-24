class Destination:
    """Represents a travel destination with its base cost and details."""

    def __init__(self, id: int | None, name: str, description: str, base_cost: float):
        if base_cost < 0:
            raise ValueError("Base cost cannot be negative.")
        self.id = id
        self.name = name
        self.description = description
        self.base_cost = base_cost

    def update_info(self, name: str, description: str, base_cost: float) -> None:
        """Updates the destination's name, description, and base cost."""
        if base_cost < 0:
            raise ValueError("Base cost cannot be negative.")
        self.name = name
        self.description = description
        self.base_cost = base_cost

    def to_tuple(self) -> tuple:
        """Returns destination attributes as a tuple for database insertion."""
        return (self.name, self.description, self.base_cost)