from typing import List
from src.models.ft_drone import Drone
from src.ft_parser import ParsedMap
from src.algorithms.path_finder import PathFinder

class Simulator:
    def __init__(self, parsed_map: ParsedMap):
        self.map_data = parsed_map
        self.start_zone = parsed_map.start_hub
        self.end_zone = parsed_map.end_hub
        self.pf = PathFinder(parsed_map)
        
        self.drones: List[Drone] = []
        for i in range(parsed_map.nb_drones):
            self.drones.append(Drone(i + 1, self.map_data.zones[self.start_zone.name]))
         
        # just for debuggin    
        # for zone in self.map_data.zones:
        #     print(self.map_data.zones[zone].name, end="  ")
        
        self.turn_count = 0
        
    def _get_connection_name(self, zone1_name: str, zone2_name: str) -> str:
        z1, z2 = zone1_name.strip(), zone2_name.strip()
        for conn in self.map_data.connections:
            c1, c2 = conn.zone1.name.strip(), conn.zone2.name.strip()
            if (c1 == z1 and c2 == z2) or (c1 == z2 and c2 == z1):
                return f"{conn.zone1.name}-{conn.zone2.name}"
        return f"{zone1_name}-{zone2_name}"

    def _is_finished(self) -> bool:
        for drone in self.drones:
            if drone.current_zone.name.strip() != self.end_zone.name.strip() or drone.is_traveling:
                return False
        return True

    def run_turn(self) -> List[str]:
        turn_moves = []
        moved_this_turn = set()
        
        zone_occupancy = {name: 0 for name in self.map_data.zones.keys()}
        for drone in self.drones:
            if drone.is_traveling and drone.destination_zone:
                zone_occupancy[drone.destination_zone.name] += 1
            elif not drone.is_traveling:
                zone_occupancy[drone.current_zone.name] += 1

        link_occupancy = {self._get_connection_name(c.zone1.name, c.zone2.name): 0 for c in self.map_data.connections}

        for drone in self.drones:
            if drone.is_traveling:
                if drone.advance_turn():
                    turn_moves.append(f"D{drone.id}-{drone.current_zone.name}")
                    moved_this_turn.add(drone.id)
                else:
                    turn_moves.append(f"D{drone.id}-{drone.current_connection_name}")

        idle_drones = [d for d in self.drones if not d.is_traveling and d.current_zone.name.strip() != self.end_zone.name.strip() and d.id not in moved_this_turn]

        idle_drones.sort(key=lambda d: self.pf.get_distance(d.current_zone.name))
        
            
        for drone in idle_drones:
            current_name = drone.current_zone.name
            
            best_neighbors = list(drone.current_zone.neighbors.keys())
            best_neighbors.sort(key=lambda n: self.pf.get_distance(n))
            
            for next_name in best_neighbors:
                print("There are the best neighbors list",best_neighbors)
                next_zone = self.map_data.zones[next_name]
                
                # 🛡️ FILTER 1: U-Turn Check
                dist_next = self.pf.get_distance(next_name)
                dist_curr = self.pf.get_distance(current_name)
                if dist_next >= dist_curr:
                    continue
                
                # 🛡️ FILTER 2: Zone Capacity Check
                if next_name.strip() != self.end_zone.name.strip():
                    max_cap = getattr(next_zone, 'max_drones', 1)
                    if max_cap <= 0: 
                        max_cap = 1 
                    if zone_occupancy.get(next_name, 0) >= max_cap:
                        continue
                
                # 🛡️ FILTER 3: Link Capacity Check
                conn_name = self._get_connection_name(current_name, next_name)
                conn_obj = next((c for c in self.map_data.connections if self._get_connection_name(c.zone1.name, c.zone2.name) == conn_name), None)
                if conn_obj and hasattr(conn_obj, 'max_link_capacity'):
                    max_link = getattr(conn_obj, 'max_link_capacity')
                    if max_link is not None and max_link > 0:
                        if link_occupancy.get(conn_name, 0) >= max_link:
                            continue

                # ✅ KOLCHI NADI: 7erek D-Drone
                print(f"$$$$$$$$$$$$$$$$$$$$$ {zone_occupancy} ####################")
                
                zone_occupancy[current_name] -= 1
                zone_occupancy[next_name] = zone_occupancy.get(next_name, 0) + 1
                link_occupancy[conn_name] = link_occupancy.get(conn_name, 0) + 1
                
                is_restricted = False
                if hasattr(next_zone, 'zone_type'):
                    zt = str(getattr(next_zone, 'zone_type')).lower()
                    if 'restricted' in zt:
                        is_restricted = True

                move_cost = 2 if is_restricted else 1

                if move_cost == 1:
                    drone.current_zone = next_zone
                    turn_moves.append(f"D{drone.id}-{next_name}")
                else:
                    # 🌟 THE EUREKA FIX: (move_cost - 1)
                    # Haka L-Transit ghadi y-shed 2 Turns d-bsseh machi 3!
                    drone.move_to(next_zone, conn_name, move_cost - 1)
                    turn_moves.append(f"D{drone.id}-{conn_name}")
                break
        print(f"$$$$$$$$$$$$$$$$$$$$$ {zone_occupancy} ####################")
    
        return turn_moves

    def run_all(self):
        while not self._is_finished():
            self.turn_count += 1
            moves = self.run_turn()
            
            if moves:
                # print(f"# Turn {self.turn_count}")
                print(" ".join(moves))
            else:
                print(f"\n[!] Engine Stalled at Turn {self.turn_count}! Drones are blocked by traffic.")
                break
