import argparse
import sys
from src.ft_parser import MapParser
from src.algorithms.path_finder import PathFinder
from src.ft_engine import Simulator

def main():
    # 1. Twajad dyal l-Arguments
    parser_args = argparse.ArgumentParser(description="Fly-in: Drone Routing & Simulator")
    
    # Argument asasi (Darouri): l-chemin dyal fichier map
    parser_args.add_argument("map_file", help="Path to the map .txt file (e.g., maps/test.txt)")
    
    # Argument ikhtiyari (Optional) dyal visualization: --viz
    parser_args.add_argument("--viz", action="store_true", help="Enable Pygame visualization")

    # Qra l-arguments li dkhl l-user f terminal
    args = parser_args.parse_args()

    # print(f"Starting Fly-in Simulation with map: {args.map_file}")
    # if args.viz:
    #     print("🎨 Visualization Mode: ON")
    # else:
    #     print("🖥️ Terminal Mode: ON")

    # 2. Bda l-Khedma d- بصح (Parsing & Pathfinding)
    try:
        parser = MapParser()
        parsed_map = parser.file_parsing(args.map_file)
        
        pf = PathFinder(parsed_map)
        start_name = parsed_map.start_hub.name
        end_name = parsed_map.end_hub.name
        
        shortest_path = pf.dijkstra(start_name, end_name)
        
        if not shortest_path:
            print("No path found! Drones are stuck.!")
            sys.exit(1)
            
        print(f"✅ Found Base Path: {' -> '.join(shortest_path)}")
        total_drones = parsed_map.nb_drones
        # 3. L-Engine (Simulator) - TBC
        if args.viz:
            print("🎨 Visualization Mode: ON (Coming soon...)")
            pass
        else:
            sim = Simulator(parsed_map, shortest_path, total_drones)
            sim.run_all()
            print(f"# Total turns: {sim.turn_count}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()