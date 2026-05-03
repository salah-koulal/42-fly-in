from typing import List,Dict
from src.models.ft_drone import Drone
from src.models.ft_zone import ZoneType
from src.ft_parser import ParsedMap

class Simulator:
    def __init__(self, parsed_map: ParsedMap, base_path: List[str], total_drones: int):
        self.map_data = parsed_map
        self.turn_count = 0
        self.drones: List[Drone] = []
        
        for i in range(total_drones):
            new_drone = Drone(i + 1, base_path)
            self.drones.append(new_drone)
        
        
    def run_all(self):
        while not self._all_drones_finished():
            self.turn_count += 1
            self.run_turn()
    
    
    def run_turn(self):
        moves_this_turn: List[str] = []
        # 1. an7seb ch7al mn drone kayn f koul zone dba (bach nmanagi lcapacity)
        zone_occupancy: Dict[str, int] = {zone_name: 0 for zone_name in self.map_data.zones}
        link_occupancy = {}
        
        for drone in self.drones:
            if not drone.is_finished and not drone.in_transit:
                zone_occupancy[drone.current_zone] += 1
                
    
        for drone in self.drones:
            if drone.is_finished:
                            continue
            
            current_node = drone.current_zone
            next_node = drone.path[drone.path_index + 1]
            next_zone_obj = self.map_data.zones[next_node]

            if drone.in_transit:
                drone.in_transit = False
                drone.path_index += 1
                moves_this_turn.append(f"D{drone.id}-{next_node}")
                zone_occupancy[next_node] += 1
                continue
            
            
            has_capacity = False
            if zone_occupancy[next_node] < next_zone_obj.max_drones or next_node == self.map_data.end_hub.name:
                has_capacity = True
                
            if has_capacity:
                if next_zone_obj.zone_type == ZoneType.RESTRICTED:
                    drone.in_transit = True
                    zone_occupancy[current_node] -= 1
                    moves_this_turn.append(f"D{drone.id}-{current_node}-{next_node}")
                else:
                    drone.path_index += 1
                    zone_occupancy[current_node] -= 1
                    zone_occupancy[next_node] += 1
                    moves_this_turn.append(f"D{drone.id}-{next_node}")
            else:
                pass
        if moves_this_turn:
            print(" ".join(moves_this_turn))
                    
                    
        
    def _all_drones_finished(self) -> bool:
        """Katreje3 True ila ga3 d-drones wslou l end_hub"""
        # TBC: return True ila ga3 self.drones 3ndhom drone.is_finished == True
        for drone in self.drones:
            if not drone.is_finished:
                return False
        return True
            