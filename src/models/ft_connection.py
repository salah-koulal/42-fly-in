from dataclasses import dataclass
from src.models.ft_zone import Zone


@dataclass
class Connection:
    zone1: Zone
    zone2: Zone
    max_link_capacity: int = 1