from typing import List, Dict
from src.models import Zone
from pydantic import BaseModel
from pathlib import Path



class ParsedMap(BaseModel):
    """just for pydantic validate map data structure"""

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
        self.zones = {}
        self.connections = []
        self.seen_connections = set()
        self.nb_drones_parsed = False