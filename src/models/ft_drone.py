from typing import Optional
from src.models.ft_zone import Zone

class Drone:
    def __init__(self, drone_id: int, start_zone: Zone):
        self.id: int = drone_id
        self.current_zone: Zone = start_zone

        # Variables dyal Transit (Restricted)
        self.is_traveling = False
        self.destination_zone: Zone = None
        self.current_connection_name = ""
        self.turns_until_arrival = 0
    
    def move_to(self, next_zone, connection_name: str, move_cost: int):
        """Kat-sifet d-drone l T-triq"""
        self.is_traveling = True
        self.destination_zone = next_zone
        self.current_connection_name = connection_name
        self.turns_until_arrival = move_cost
        # Mss7na L-Error d remove mn hna!
    
    def advance_turn(self):
        """Kat-n9ess L-weqt dyal T-triq koul turn"""
        if self.is_traveling:
            self.turns_until_arrival -= 1
            if self.turns_until_arrival <= 0:
                # Wsel L-blassa!
                self.is_traveling = False
                self.current_zone = self.destination_zone
                self.destination_zone = None
                self.current_connection_name = ""
                return True
        return False