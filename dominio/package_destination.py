class PackageDestination:
    """Represents the many-to-many relationship between a travel package and a destination."""

    def __init__(self, id: int | None, package_id: int, destination_id: int):
        self.id = id
        self.package_id = package_id
        self.destination_id = destination_id

    def to_tuple(self) -> tuple:
        """Returns the foreign keys as a tuple for database insertion."""
        return (self.package_id, self.destination_id)