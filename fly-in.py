import argparse
import sys
from src.ft_parser import MapParser
# (T2ked mn smiyt L-fichier dyal PathFinder 3ndk)
from src.algorithms.path_finder import PathFinder
from src.models import ZoneType
from src.ft_engine import Simulator

def main():
    parser_args = argparse.ArgumentParser(description="Fly-in: Drone Routing & Simulator")
    parser_args.add_argument("map_file", help="Path to the map .txt file (e.g., maps/test.txt)")
    parser_args.add_argument("--viz", action="store_true", help="Enable Pygame visualization")
    args = parser_args.parse_args()

    try:
        parser = MapParser()
        parsed_map = parser.file_parsing(args.map_file)
        
        # print(parsed_map.connections)
        pf = PathFinder(parsed_map)
        start_name = parsed_map.start_hub.name
        if pf.get_distance(start_name) == float('inf'):
            print("No path found! Drones are stuck.!")
            sys.exit(1)
        
        print(pf.distances)
        print("PathFinder: Routes Calculated Successfully!\n\n")

        if args.viz:
            print("🎨 Visualization Mode: ON (Coming soon...)")
            pass
        else:
            print(f"running fly in with the map:{args.map_file}")
            sim = Simulator(parsed_map)
            sim.run_all()
            print(f"\n# Total turns: {sim.turn_count}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()