from typing import List, Dict, Optional
from src.models import Zone
from pydantic import BaseModel
from pathlib import Path
import sys



class ParsedMap(BaseModel):
    """just for pydantic validate map data structure"""
    pass
class MapParser:
    """Parser for input files."""
    def __init__(self) -> None:
        """Initialize the parser."""
        self.zones: Dict[str, Zone] = {}
        self.connections: list[tuple[str, str, int]] = []
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
                    raise ValueError(f"FAAAAAAAAAH! Line {n_line}: the first line must be nb_drones \
                                    'nb_drones: <valid_integer>' ")
            # start_hub parsing here!
            elif line.startswith("start_hub:"):
                if start_hub is not None:
                    raise ValueError(f"FAAAAAAAAAAH! Line {n_line}: It must be just one start hub per map")
                content = line.replace("start_hub: ","").strip()
                parts = content.split()
                if len(parts) < 3:
                    raise ValueError(f"Line {n_line}: start_hub needs <name, (x,y)>")
                name = parts[0]
                try:
                    x = int(parts[1])
                    y = int(parts[2])
                except ValueError:
                    raise ValueError(f"FAAAH ! Line {n_line}: x and y must be valid integers")
                
                zone_metadata = " ".join(parts[3:]) if len(parts) > 3 else None
                start_hub = Zone(name, x, y)
                self.zones[name] = start_hub
                
                print(f"-> Start Hub found it : {name} in ({x}, {y})")
                continue
            
            
            # end_hub parsing heree! same thing as start_hub
            elif line.startswith("end_hub: "):
                if end_hub is not None:
                    raise ValueError(f"Line {n_line}: It must be just one end hub per map")
                content = line.replace("end_hub: ", "").strip()
                print(f"<<<<<<<< {content} >>>>>>>>>")
                parts = content.split()
                if len(parts) < 3:
                        raise ValueError(f"Line {n_line}: end_hub needs <name, (x, y)>")
                name  = parts[0]
                try:
                    x = int(parts[1])
                    y = int(parts[2])
                except ValueError:
                    raise ValueError(f"Line {n_line}: x and y must be valid integers")
                
                print(parts[3:])
                zone_metadata = " ".join(parts[3:]) if len(parts) > 3 else None
                end_hub = Zone(name, x, y)
                self.zones[name] = end_hub
                print(f"-> End Hub found it : {name} in ({x}, {y})")
                continue
            
            # TBC AJMI ...

        return ParsedMap()




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
if __name__ == "__main__":
    main()