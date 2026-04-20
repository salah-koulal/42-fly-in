from typing import List, Dict, Optional
from src.models.ft_zone import Zone
from src.models.ft_connection import Connection
# from pydantic import BaseModel
from dataclasses import dataclass
from pathlib import Path
import sys


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
    
    
    def file_parsing(self, filepath) -> ParsedMap:
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
            # print(f"{line}")
            if not line:
                continue           
                
            # parsing the line of nb_drones must be the 1st line
            if not self.nb_drones_parsed:
                if line.startswith("nb_drones:"):
                    drones_str = line.split(":")[1].strip()
                    try:
                        nb_drones = int(drones_str)
                    except ValueError:
                        raise ValueError(f"Line {n_line}: nb_drones must be a valid integer dude!")

                    if nb_drones <= 0:
                        raise ValueError(f"Line {n_line}: nb_drones must be > 0")
                    self.nb_drones_parsed = True
                    continue
                else:
                    raise ValueError(f"Line {n_line}: the first line must be nb_drones \
                                    'nb_drones: <valid_integer>' ")
            # start_hub parsing here!
            elif line.startswith("start_hub:"):
                if start_hub is not None:
                    raise ValueError(f"Line {n_line}: It must be just one start hub per map")
                content = line.replace("start_hub:","").strip()
                parts = content.split()
                if len(parts) < 3:
                    raise ValueError(f"Line {n_line}: start_hub needs <name, (x,y)>")
                name = parts[0]
                try:
                    x = int(parts[1])
                    y = int(parts[2])
                except ValueError:
                    raise ValueError(f"Line {n_line}: x and y must be valid integers")
                
                zone_metadata = " ".join(parts[3:]) if len(parts) > 3 else None
                start_hub = Zone(name, x, y)
                self.zones[name] = start_hub
                
                print(f"-> Start Hub found it : {name} in ({x}, {y})")
                continue
            
            
            # end_hub parsing heree! same thing as start_hub
            elif line.startswith("end_hub:"):
                if end_hub is not None:
                    raise ValueError(f"Line {n_line}: It must be just one end hub per map")
                content = line.replace("end_hub:", "").strip()
                parts = content.split()
                if len(parts) < 3:
                        raise ValueError(f"Line {n_line}: end_hub needs <name, (x, y)>")
                name  = parts[0]
                try:
                    x = int(parts[1])
                    y = int(parts[2])
                except ValueError:
                    raise ValueError(f"Line {n_line}: x and y must be valid integers")
                
                zone_metadata = " ".join(parts[3:]) if len(parts) > 3 else None
                end_hub = Zone(name, x, y)
                self.zones[name] = end_hub
                print(f"-> End Hub found it : {name} in ({x}, {y})")
                continue
            # parsing other hubs
            elif line.startswith("hub:"):
                content = line.replace("hub:", "").strip()
                parts = content.split()
                if len(parts) < 3:
                    raise ValueError(f"Line {n_line}: every hub must have <name, (x, y)>")
                name = parts[0]
                try:
                    x = int(parts[1])
                    y = int(parts[2])
                except ValueError:
                    raise ValueError(f"Line {n_line}: x and y must be valid integers")
                
                zone_metadata = " ".join(parts[3:]) if len(parts) > 3 else None
                hub_zone = Zone(name, x, y)
                self.zones[name] = hub_zone
                print(f"-> Hub (3adi) m9ad: {name} f ({x}, {y})")
                continue
            
            # parsing connections
            elif line.startswith("connection:"):
                content = line.replace("connection:", "").strip()
                # print(f"@@@@@@@@@{content}@@@@@@@@@@@")
                parts = content.split()
                
                zones_str = parts[0]
                # print(f"<<<<<{zones_str}>>>>>>>>>>>>")
                if "-" not in zones_str:
                    raise ValueError(f"Line: {line}: The connection must be linked by (-) <a-b>")
                
                zone1_name, zone2_name = zones_str.split("-", 1)
                if zone1_name not in self.zones:
                    raise ValueError(f"Line {n_line}: the zone is unknown")
                if zone2_name not in self.zones:
                    raise ValueError(f"Line {n_line}: the zone is unknown")
                normalized_conn = tuple(sorted([zone1_name, zone2_name]))
                if normalized_conn in self.seen_connections:
                    raise ValueError(f"Line {n_line}: The connection {zones_str} already seen")
                
                z1 = self.zones[zone1_name]
                z2 = self.zones[zone2_name]
                
                conn = Connection(z1, z2)
                self.connections.append(conn)
                self.seen_connections.add(normalized_conn)
                
                z1.neighbors[zone2_name] = conn
                z2.neighbors[zone1_name] = conn
                
                print(f"-> Triq m9ada: {zone1_name} <-> {zone2_name}")
                continue
            else:
                raise ValueError(f"Line {n_line}: there is no parameters like '{line}'") 
                
                
        if not self.nb_drones_parsed:
            raise ValueError("There is no (nb_drones) in the file")
        if start_hub is None:
            raise ValueError("There is no start_hub in the file")
        if end_hub is None:
            raise ValueError("There is no end_hub in the file")
        return ParsedMap(
                nb_drones=nb_drones,
                start_hub=start_hub,
                end_hub=end_hub,
                zones=self.zones,
                connections=self.connections
            )



def main():
    parser = MapParser() 
    try:
        parsed_map = parser.file_parsing("./test.txt")
        print("Map parsed successfully!")
    except ValueError as e:
        print(f"Parsing Error: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"File Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
