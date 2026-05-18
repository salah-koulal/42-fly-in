"""Provides path finding algorithms for routing drones."""

import heapq
from typing import Dict
from src.models.ft_zone import ZoneType
from src.ft_parser import ParsedMap


class PathFinder:
    """Calculates shortest paths from all zones to the end zone.

    Attributes:
        map (ParsedMap): The parsed map data.
        end_name (str): The name of the destination zone.
        distances (Dict[str, float]): A dictionary mapping zone names to their
            computed distance to the end zone.
    """

    def __init__(self, parsed_map: ParsedMap):
        """Initializes the PathFinder and computes initial distances.

        Args:
            parsed_map (ParsedMap): The parsed map data.
        """
        self.map = parsed_map
        self.end_name = parsed_map.end_hub.name

        self.distances: Dict[str, float] = self._compute_reverse_distances()

    def _compute_reverse_distances(self) -> Dict[str, float]:
        """Computes shortest path distances from the destination to all zones.

        Uses Dijkstra's algorithm to calculate the distance from the end zone
        to every other zone in the map.

        Returns:
            Dict[str, float]: Dictionary mapping zone names to distances.
        """
        distances = {name: float("inf") for name in self.map.zones}
        distances[self.end_name] = 0.0

        pq = [(0.0, self.end_name)]

        while pq:
            current_cost, current_name = heapq.heappop(pq)
            if current_cost > distances[current_name]:
                continue

            current_zone = self.map.zones[current_name]

            for neighbor_name in current_zone.neighbors:
                neighbor_zone = self.map.zones[neighbor_name]
                if neighbor_zone.zone_type == ZoneType.BLOCKED:
                    continue

                move_cost = (
                    2.0
                    if current_zone.zone_type == ZoneType.RESTRICTED
                    else 1.0
                )

                if current_zone.zone_type == ZoneType.PRIORITY:
                    move_cost -= 0.05
                new_cost = current_cost + move_cost

                if new_cost < distances[neighbor_name]:
                    distances[neighbor_name] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor_name))

        return distances

    def get_distance(self, zone_name: str) -> float:
        """Returns the precomputed shortest distance from the given zone.

        Args:
            zone_name (str): The name of the zone to check.

        Returns:
            float: The distance to the end zone, or infinity if unreachable.
        """
        return self.distances.get(zone_name, float("inf"))
