from typing import List, Dict, Optional
import math
from src.models.ft_zone import Zone, ZoneType
from src.ft_parser import ParsedMap

class PathFinder:
    def __init__(self, parsed_map: ParsedMap):
        """It takes just the parsed map"""
        self.map_data = parsed_map
        self.zones = parsed_map.zones
    
    
    def dijkstra(self, start_name: str, end_name: str) -> Optional[List[str]]:
        """To be added later """
        distances: Dict[str, float] = {}
        previous_nodes: Dict[str, Optional[str]] = {}
        unvisited: List[str] = []
        
        #initialization of zones
        for zone_name in self.zones:
            distances[zone_name] = float('inf')
            previous_nodes[zone_name] = None
            unvisited.append(zone_name)
        
        distances[start_name] = float(0)
        
        # main loop of the algorithm (Dijkstra Loop)
        while unvisited:
            print(f"########## unvisited, so far! : {unvisited} ########### ")
            current = min(unvisited, key=lambda node: distances[node])
            if distances[current] == math.inf:
                break
            
            if current == end_name:
                break
            
            current_zone = self.zones[current]
            
            for neighbor_name in current_zone.neighbors:
                if neighbor_name not in unvisited:
                    continue
                
                neighbor_zone = self.zones[neighbor_name]
                
                cost = 2 if neighbor_zone.zone_type == ZoneType.RESTRICTED else 1
                new_distance = distances[current] + cost

                
                # Update distances & previous)
                if new_distance < distances[neighbor_name]:
                    distances[neighbor_name] = new_distance
                    previous_nodes[neighbor_name] = current
                
            unvisited.remove(current)
            
        # backtracking
        current_step = end_name
        path: List[str] = []
        while current_step is not None:
            path.append(current_step)
            current_step = previous_nodes[current_step]

        path.reverse()
        print(path)
        if path and path[0] == start_name:
            print(f"Total Cost (Turns): {distances[end_name]}") 
            return path
        return None                    