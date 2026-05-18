"""Module containing the Connection model for linking zones."""

from dataclasses import dataclass
from src.models.ft_zone import Zone


@dataclass
class Connection:
    """Represents a direct pathway between two zones with a specified capacity.

    Attributes:
        zone1 (Zone): The first zone in the connection.
        zone2 (Zone): The second zone in the connection.
        max_link_capacity (int): Max drones that can traverse simultaneously.
    """

    zone1: Zone
    zone2: Zone
    max_link_capacity: int = 1
