from dataclasses import dataclass, field
from typing import Dict, Optional, TYPE_CHECKING
from enum import Enum


if TYPE_CHECKING:
    from src.models.ft_connection import Connection

class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


@dataclass
class Zone:
    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    max_drones: int = 1
    color: Optional[str] = None
    neighbors: Dict[str, 'Connection'] = field(default_factory=dict)
    
