from typing import List, Dict, Optional
# from src.models import Zone
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
            # elif line.startswith
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