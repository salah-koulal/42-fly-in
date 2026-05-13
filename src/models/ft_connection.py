from dataclasses import dataclass
from src.models.ft_zone import Zone


@dataclass
class Connection:
    """Represents a direct pathway between two zones with a
    specified capacity."""

    zone1: Zone
    zone2: Zone
    max_link_capacity: int = 1
