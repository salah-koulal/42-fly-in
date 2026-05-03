from typing import Optional, List
from models.ft_zone import Zone

class Drone:
    def __init__(self, drone_id: int, current_zone: Zone):
        self.id: int = drone_id
        self.current_zone: Zone = self.current_zone
        self.is_traveling: bool = False
        
    @property
    def current_zone(self) -> str:
        return self.path[self.path_index]
    
    @property
    def is_finished(self) -> bool:
        return self.path_index >= len(self.path) - 1