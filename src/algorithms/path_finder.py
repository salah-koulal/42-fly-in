import heapq
from typing import Dict, List, Optional
from src.models.ft_zone import ZoneType
from src.ft_parser import ParsedMap

class PathFinder:
    def __init__(self, parsed_map: ParsedMap):
        self.map = parsed_map
        self.end_name = parsed_map.end_hub.name
        
        self.distances: Dict[str, float] = self._compute_reverse_distances()
    
    
    def _compute_reverse_distances(self) -> Dict[str, float]:
        distances = {name: float('inf') for name in self.map.zones}
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
                
                move_cost = 2.0 if current_zone.zone_type == ZoneType.RESTRICTED else 1.0
                
                if current_zone.zone_type == ZoneType.PRIORITY:
                    move_cost -= 0.05
                new_cost = current_cost + move_cost
                
                if new_cost < distances[neighbor_name]:
                    distances[neighbor_name] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor_name))
                    
        return distances
    
    
    def get_distance(self, zone_name: str) -> float:
        return self.distances.get(zone_name, float('inf'))
    
    def get_best_next_zones(self, current_name: str) -> List[str]:
        current_zone = self.map.zones[current_name]
        ranked_neighbors = []

        for neighbor_name in current_zone.neighbors:
            neighbor_zone = self.map.zones[neighbor_name]
            
            dist = self.get_distance(neighbor_name)
            if dist == float('inf') and neighbor_name != self.end_name:
                continue
            move_cost = 2.0 if neighbor_zone.zone_type == ZoneType.RESTRICTED else 1.0
            bias = -0.05 if neighbor_zone.zone_type == ZoneType.PRIORITY else 0.0
            
            projected_cost = dist + move_cost + bias
            
            ranked_neighbors.append((projected_cost, move_cost, neighbor_name))
            ranked_neighbors.sort(key=lambda x: (x[0], x[1], x[2]))
            return [item[2] for item in ranked_neighbors]
