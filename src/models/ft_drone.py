from typing import Optional
from src.models.ft_zone import Zone


class Drone:
    """Represents a drone in the simulation.

    Attributes:
        id (int): The unique identifier of the drone.
        current_zone (Zone): The zone where the drone is currently located.
        is_traveling (bool): Indicates if the drone is in transit.
        destination_zone (Optional[Zone]): The zone the drone is traveling to.
        current_connection_name (str): Connection the drone is traversing.
        turns_until_arrival (int): Turns remaining until the destination is met.
    """

    def __init__(self, drone_id: int, start_zone: Zone):
        """Initializes the drone with an ID and a starting zone.

        Args:
            drone_id (int): The unique identifier for this drone.
            start_zone (Zone): The starting zone where the drone spawns.
        """
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
        """Dispatches the drone to transit through a connection.

        Args:
            next_zone (Zone): The destination zone the drone will travel to.
            connection_name (str): The name of the connection being used.
            move_cost (int): Number of turns required to complete the movement.
        """
        self.is_traveling = True
        self.destination_zone = next_zone
        self.current_connection_name = connection_name
        self.turns_until_arrival = move_cost

    def advance_turn(self):
        """Decrements travel time each turn and completes move if time is up.

        Returns:
            bool: True if destination is reached this turn, False otherwise.
        """
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
