from typing import List, Dict, Optional
from src.models.ft_zone import Zone, ZoneType
from src.models.ft_connection import Connection
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ParsedMap:
    """Dataclass to hold the validated map data"""

    nb_drones: int
    start_hub: Zone
    end_hub: Zone
    zones: Dict[str, Zone]
    connections: List[Connection]


class MapParser:
    """Parser for input files."""
    def __init__(self) -> None:
        """Initialize the parser."""
        self.zones: Dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.seen_connections: set[tuple[str, str]] = set()
        self.nb_drones_parsed = False

    def _parse_metadata(
        self, metadata_str: Optional[str], n_line: int
    ) -> dict:
        """Parses metadata string and returns a dictionary of attributes."""
        required_metadata = [
            "max_drones",
            "color",
            "zone",
            "max_link_capacity",
        ]
        if not metadata_str:
            return {}
        metadata_str = metadata_str.strip()
        if not (metadata_str.startswith("[") and metadata_str.endswith("]")):
            raise ValueError(
                f"Line {n_line}: Metadata must be between [...] -> '{metadata_str}'"
            )

        content = metadata_str[1:-1].strip()
        if not content:
            return {}

        parsed_data = {}
        items = content.split()

        for item in items:
            if "=" not in item:
                raise ValueError(
                    f"Line {n_line}: Metadata syntax error in '{item}', must be key=value"
                )

            key, value = item.split("=", 1)
            if key not in required_metadata:
                raise ValueError(
                    f"Line {n_line}: Not found in required metadata <max_drones, color, zone, max_link_capacity>"
                )
            if key in parsed_data:
                raise ValueError(
                    f"Line {n_line}: Key '{key}' is duplicated in metadata"
                )

            parsed_data[key] = value

        return parsed_data

    def file_parsing(self, filepath) -> ParsedMap:
        """Parses the input map file and returns a ParsedMap object."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Map file not found: {filepath}")
        try:
            with open(path, "r") as f:
                lines = f.readlines()
        except IOError as exec:
            raise ValueError((f"Failed to read file: {exec}"))

        nb_drones = 0
        start_hub: Optional[Zone] = None
        end_hub: Optional[Zone] = None
        self.zones = {}
        self.connections = []
        self.seen_connections = set()
        self.nb_drones_parsed = False

        for n_line, line in enumerate(lines, 1):
            line = line.split("#")[0].strip()
            if not line:
                continue

            if not self.nb_drones_parsed:
                if line.startswith("nb_drones:"):
                    drones_str = line.split(":")[1].strip()
                    try:
                        nb_drones = int(drones_str)
                    except ValueError:
                        raise ValueError(
                            f"Line {n_line}: nb_drones must be a valid integer!"
                        )

                    if nb_drones <= 0:
                        raise ValueError(
                            f"Line {n_line}: nb_drones must be > 0"
                        )
                    self.nb_drones_parsed = True
                    continue
                else:
                    raise ValueError(
                        f"Line {n_line}: the first line must be nb_drones 'nb_drones: <valid_integer>'"
                    )

            elif line.startswith("start_hub:"):
                if start_hub is not None:
                    raise ValueError(
                        f"Line {n_line}: It must be just one start hub per map"
                    )
                content = line.replace("start_hub:", "").strip()
                parts = content.split()
                if len(parts) < 3:
                    raise ValueError(
                        f"Line {n_line}: start_hub needs <name> <x> <y>"
                    )

                name = parts[0]
                if "-" in name:
                    raise ValueError(
                        f"Line {n_line}: zone names cannot contain hyphens ('-'), got '{name}'"
                    )
                if name.endswith("-") or name.startswith("-"):
                    raise ValueError(
                        f"Line {n_line}: zone names cannot start or end with hyphens ('-'), got '{name}'"
                    )
                if name in self.zones:
                    raise ValueError(
                        f"Line {n_line}: zone '{name}' is duplicated"
                    )

                try:
                    x = int(parts[1])
                    y = int(parts[2])
                except ValueError:
                    raise ValueError(
                        f"Line {n_line}: x and y must be valid integers"
                    )

                metadata_str = " ".join(parts[3:]) if len(parts) > 3 else None
                meta_dict = self._parse_metadata(metadata_str, n_line)

                color = meta_dict.get("color", None)
                z_type_str = meta_dict.get("zone", "normal")
                try:
                    zone_type = ZoneType(z_type_str)
                except ValueError:
                    raise ValueError(
                        f"Line {n_line}: The zone type is unknown <'{z_type_str}'> "
                    )
                max_drones_str = meta_dict.get("max_drones", "1")
                try:
                    max_drones = int(max_drones_str)
                    if max_drones <= 0:
                        raise ValueError()
                except ValueError:
                    raise ValueError(f"Line {n_line}: max_drones must >= 0")
                start_hub = Zone(name, x, y, zone_type=zone_type, color=color)
                self.zones[name] = start_hub
                continue

            elif line.startswith("end_hub:"):
                if end_hub is not None:
                    raise ValueError(
                        f"Line {n_line}: It must be just one end hub per map"
                    )
                content = line.replace("end_hub:", "").strip()
                parts = content.split()
                if len(parts) < 3:
                    raise ValueError(
                        f"Line {n_line}: end_hub needs <name> <x> <y>"
                    )

                name = parts[0]
                if "-" in name:
                    raise ValueError(
                        f"Line {n_line}: zone names cannot contain hyphens ('-'), got '{name}'"
                    )
                if name.endswith("-") or name.startswith("-"):
                    raise ValueError(
                        f"Line {n_line}: zone names cannot start or end with hyphens ('-'), got '{name}'"
                    )
                if name in self.zones:
                    raise ValueError(
                        f"Line {n_line}: zone '{name}' is duplicated"
                    )

                try:
                    x = int(parts[1])
                    y = int(parts[2])
                except ValueError:
                    raise ValueError(
                        f"Line {n_line}: x and y must be valid integers"
                    )

                metadata_str = " ".join(parts[3:]) if len(parts) > 3 else None
                meta_dict = self._parse_metadata(metadata_str, n_line)

                max_drones_str = meta_dict.get("max_drones", "1")
                try:
                    max_drones = int(max_drones_str)
                    if max_drones <= 0:
                        raise ValueError()
                except ValueError:
                    raise ValueError(f"Line {n_line}: max_drones must >= 0")
                color = meta_dict.get("color", None)
                z_type_str = meta_dict.get("zone", "normal")

                try:
                    zone_type = ZoneType(z_type_str)
                except ValueError:
                    raise ValueError(
                        f"Line {n_line}: The zone type is unknown <'{z_type_str}'> "
                    )
                end_hub = Zone(name, x, y, zone_type=zone_type, color=color)
                self.zones[name] = end_hub
                continue

            # 4. parsing other hubs
            elif line.startswith("hub:"):
                content = line.replace("hub:", "").strip()
                parts = content.split()
                if len(parts) < 3:
                    raise ValueError(
                        f"Line {n_line}: every hub must have <name> <x> <y>"
                    )

                name = parts[0]
                if "-" in name:
                    raise ValueError(
                        f"Line {n_line}: zone names cannot contain hyphens ('-'), got '{name}'"
                    )
                if name.endswith("-") or name.startswith("-"):
                    raise ValueError(
                        f"Line {n_line}: zone names cannot start or end with hyphens ('-'), got '{name}'"
                    )
                if name in self.zones:
                    raise ValueError(
                        f"Line {n_line}: zone '{name}' is duplicated"
                    )

                try:
                    x = int(parts[1])
                    y = int(parts[2])
                except ValueError:
                    raise ValueError(
                        f"Line {n_line}: x and y must be valid integers"
                    )

                metadata_str = " ".join(parts[3:]) if len(parts) > 3 else None
                meta_dict = self._parse_metadata(metadata_str, n_line)

                z_type_str = meta_dict.get("zone", "normal")
                try:
                    zone_type = ZoneType(z_type_str)
                except ValueError:
                    raise ValueError(
                        f"Line {n_line}: The zone type is unknown <'{z_type_str}'> "
                    )

                max_drones_str = meta_dict.get("max_drones", "1")
                try:
                    max_drones = int(max_drones_str)
                    if max_drones <= 0:
                        raise ValueError()
                except ValueError:
                    raise ValueError(f"Line {n_line}: max_drones must >= 0")

                color = meta_dict.get("color", None)

                hub_zone = Zone(
                    name,
                    x,
                    y,
                    zone_type=zone_type,
                    max_drones=max_drones,
                    color=color,
                )
                self.zones[name] = hub_zone
                continue

            elif line.startswith("connection:"):
                content = line.replace("connection:", "").strip()
                parts = content.split()

                zones_str = parts[0]
                if "-" not in zones_str:
                    raise ValueError(
                        f"Line {n_line}: The connection must be linked by (-) <a-b>"
                    )

                zone1_name, zone2_name = zones_str.split("-", 1)
                if zone1_name not in self.zones:
                    raise ValueError(
                        f"Line {n_line}: the zone '{zone1_name}' is unknown"
                    )
                if zone2_name not in self.zones:
                    raise ValueError(
                        f"Line {n_line}: the zone '{zone2_name}' is unknown"
                    )

                normalized_conn = (
                    min(zone1_name, zone2_name),
                    max(zone1_name, zone2_name),
                )
                if normalized_conn in self.seen_connections:
                    raise ValueError(
                        f"Line {n_line}: The connection {zones_str} already seen"
                    )

                metadata_str = " ".join(parts[1:]) if len(parts) > 1 else None
                meta_dict = self._parse_metadata(metadata_str, n_line)

                max_cap_str = meta_dict.get("max_link_capacity", "1")
                try:
                    max_capacity = int(max_cap_str)
                    if max_capacity <= 0:
                        raise ValueError()
                except ValueError:
                    raise ValueError(
                        f"Line {n_line}: max_link_capacity must be >= 0"
                    )

                z1 = self.zones[zone1_name]
                z2 = self.zones[zone2_name]

                conn = Connection(z1, z2, max_capacity)
                self.connections.append(conn)
                self.seen_connections.add(normalized_conn)

                z1.neighbors[zone2_name] = conn
                z2.neighbors[zone1_name] = conn

                continue

            else:
                raise ValueError(
                    f"Line {n_line}: unknown parameter or syntax -> '{line}'"
                )

        if not self.nb_drones_parsed:
            raise ValueError("There is no (nb_drones) in the file")
        if start_hub is None:
            raise ValueError("There is no start_hub in the file")
        if end_hub is None:
            raise ValueError("There is no end_hub in the file")
        if start_hub.x == end_hub.x and start_hub.y == end_hub.y:
            raise ValueError(
                "The start_hub should be different than the end_hub"
            )

        seen_cords: Dict[tuple[int, int], str] = {}

        for name, zone in self.zones.items():
            coords = (zone.x, zone.y)
            if coords in seen_cords:
                other_name = seen_cords[coords]
                raise ValueError(
                    f"Duplicate Coordinates! the zone {zone.name} and"
                    f" {other_name} are in the same (x, y) <{zone.x}, {zone.y}>"
                )

            seen_cords[coords] = name

        return ParsedMap(
            nb_drones=nb_drones,
            start_hub=start_hub,
            end_hub=end_hub,
            zones=self.zones,
            connections=self.connections,
        )
