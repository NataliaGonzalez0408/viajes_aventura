class Destination:
    """Represents a travel destination with its base cost, details, and active status."""

    def __init__(
        self,
        id: int | None,
        name: str,
        description: str,
        base_cost: float,
        active: bool = True,
    ):
        if not name or not name.strip():
            raise ValueError("Destination name cannot be empty.")
        if base_cost < 0:
            raise ValueError("Base cost cannot be negative.")

        self.id = id
        self.name = name.strip()
        self.description = description.strip() if description else ""
        self.base_cost = base_cost
        self.active = bool(active)

    def update_info(self, name: str, description: str, base_cost: float) -> None:
        """Updates the destination's name, description, and base cost."""
        if not name or not name.strip():
            raise ValueError("Destination name cannot be empty.")
        if base_cost < 0:
            raise ValueError("Base cost cannot be negative.")

        self.name = name.strip()
        self.description = description.strip() if description else ""
        self.base_cost = base_cost

    def deactivate(self) -> None:
        """Marks the destination as inactive so it cannot be added to new packages."""
        if not self.active:
            raise ValueError("The destination is already inactive.")
        self.active = False

    def activate(self) -> None:
        """Marks the destination as active."""
        if self.active:
            raise ValueError("The destination is already active.")
        self.active = True

    def to_tuple(self) -> tuple:
        """Returns destination attributes as a tuple for database insertion."""
        return (self.name, self.description, self.base_cost, int(self.active))