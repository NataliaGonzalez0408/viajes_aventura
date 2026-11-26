from src.domain.destinations import Destination
from src.persistence.destinations_dao import DestinationsDAO
from src.services.permissions import require_admin


def list_destinations() -> list[Destination]:
    """Returns all registered destinations ordered by ID."""
    dao = DestinationsDAO()
    return dao.get_all()


def get_destination_by_id(dest_id: int) -> Destination:
    """Returns a destination by ID or raises ValueError if not found."""
    if not isinstance(dest_id, int) or dest_id <= 0:
        raise ValueError("Destination ID must be a positive integer.")

    dao = DestinationsDAO()
    destination = dao.get_by_id(dest_id)
    if destination is None:
        raise ValueError(f"Destination with ID {dest_id} does not exist.")
    return destination


def create_destination(
    session: dict | None,
    name: str,
    description: str,
    base_cost: float = 0.0,
    active: bool = True,
) -> int:
    """Creates a new destination after validating admin permissions and input data."""
    require_admin(session)

    if base_cost < 0:
        raise ValueError("Base cost cannot be negative.")

    dao = DestinationsDAO()
    clean_name = name.strip() if name else ""
    if clean_name and any(
        d.name.strip().lower() == clean_name.lower() for d in dao.get_all()
    ):
        raise ValueError(f"A destination named '{clean_name}' already exists.")

    destination = Destination(
        id=None,
        name=name,
        description=description,
        base_cost=float(base_cost),
        active=bool(active),
    )
    created = dao.create(destination)
    return created.id


def update_destination(
    session: dict | None,
    dest_id: int,
    name: str,
    description: str,
    base_cost: float,
) -> Destination:
    """Updates an existing destination using Destination.update_info."""
    require_admin(session)
    destination = get_destination_by_id(dest_id)

    dao = DestinationsDAO()
    clean_name = name.strip() if name else ""
    if clean_name and any(
        d.id != dest_id and d.name.strip().lower() == clean_name.lower()
        for d in dao.get_all()
    ):
        raise ValueError(f"Another destination named '{clean_name}' already exists.")

    destination.update_info(name=name, description=description, base_cost=float(base_cost))
    return dao.update(destination)


def deactivate_destination(session: dict | None, dest_id: int) -> Destination:
    """Marks a destination as inactive and warns if it is used in packages."""
    require_admin(session)
    destination = get_destination_by_id(dest_id)
    destination.deactivate()
    if is_destination_in_use(dest_id):
        raise ValueError(
            "Cannot deactivate destination because it is already assigned to one or more packages."
        )
    return dao_update_active_or_state(destination)


def activate_destination(session: dict | None, dest_id: int) -> Destination:
    """Marks a destination as active."""
    require_admin(session)
    destination = get_destination_by_id(dest_id)
    destination.activate()
    return destination


def dao_update_active_or_state(destination: Destination) -> Destination:
    """Persists destination state when table does not store an active column."""
    dao = DestinationsDAO()
    return dao.update(destination)


def is_destination_in_use(dest_id: int) -> bool:
    """Checks whether a destination is currently linked to any package."""
    get_destination_by_id(dest_id)
    dao = DestinationsDAO()
    return dao.is_used_in_packages(dest_id)