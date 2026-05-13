from typing import Optional
from src.models.ft_zone import Zone


class Drone:
    """Represents a drone in the simulation."""

    def __init__(self, drone_id: int, start_zone: Zone):
        """Initializes the drone with an ID and a starting zone."""
        self.id: int = drone_id
        self.current_zone: Zone = start_zone

        # Transit Variables (Restricted)
        self.is_traveling = False
        self.destination_zone: Optional[Zone] = None
        self.current_connection_name = ""
        self.turns_until_arrival = 0

    def move_to_connection(
        self, next_zone, connection_name: str, move_cost: int
    ):
        """Dispatches the drone to transit through a connection."""
        self.is_traveling = True
        self.destination_zone = next_zone
        self.current_connection_name = connection_name
        self.turns_until_arrival = move_cost

    def advance_turn(self):
        """Decrements the travel time each turn and completes
    the move if time is up."""
        if self.is_traveling:
            self.turns_until_arrival -= 1
            if self.turns_until_arrival <= 0:
                # Reached destination zone!
                self.is_traveling = False
                self.current_zone = self.destination_zone
                self.destination_zone = None
                self.current_connection_name = ""
                return True
        return False
