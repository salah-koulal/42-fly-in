from dataclasses import dataclass, field
from typing import Dict, Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from src.models.ft_connection import Connection


class ZoneType(Enum):
    """Enumeration for the different types of zones a drone can traverse.

    Attributes:
        NORMAL: Standard zone with 1 turn movement cost.
        BLOCKED: Inaccessible zone. Drones must not enter.
        RESTRICTED: Sensitive zone. Movement costs 2 turns.
        PRIORITY: Preferred zone. Movement costs 1 turn but is prioritized.
    """

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


@dataclass
class Zone:
    """Represents a map zone (hub) with properties like capacity and neighbors.

    Attributes:
        name (str): The unique name of the zone.
        x (int): The X coordinate of the zone.
        y (int): The Y coordinate of the zone.
        zone_type (ZoneType): The type of the zone, determining movement rules.
        max_drones (int): Max drones that can occupy the zone simultaneously.
        color (Optional[str]): Optional color for visual representation.
        neighbors (Dict[str, "Connection"]): Maps neighbor names to connections.
    """

    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    max_drones: int = 1
    color: Optional[str] = None
    neighbors: Dict[str, "Connection"] = field(default_factory=dict)
