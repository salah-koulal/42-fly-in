import argparse
import sys
from src.ft_parser import MapParser
from src.algorithms.path_finder import PathFinder

def main():
    # 1. Twajad dyal l-Arguments
    parser_args = argparse.ArgumentParser(description="Fly-in: Drone Routing & Simulator")
    
    # Argument asasi (Darouri): l-chemin dyal fichier map
    parser_args.add_argument("map_file", help="Path to the map .txt file (e.g., maps/test.txt)")
    
    # Argument ikhtiyari (Optional) dyal visualization: --viz
    parser_args.add_argument("--viz", action="store_true", help="Enable Pygame visualization")

    # Qra l-arguments li dkhl l-user f terminal
    args = parser_args.parse_args()

    print(f"🚀 Starting Fly-in Simulation with map: {args.map_file}")
    if args.viz:
        print("🎨 Visualization Mode: ON")
    else:
        print("🖥️ Terminal Mode: ON")

    # 2. Bda l-Khedma d- بصح (Parsing & Pathfinding)
    try:
        parser = MapParser()
        parsed_map = parser.file_parsing(args.map_file)
        
        pf = PathFinder(parsed_map)
        shortest_path = pf.dijkstra(parsed_map.start_hub.name, parsed_map.end_hub.name)
        
        if not shortest_path:
            print("❌ No path found!")
            sys.exit(1)
            
        print(f"✅ Found Base Path: {' -> '.join(shortest_path)}")
        
        # 3. L-Engine (Simulator) - TBC
        if args.viz:
            # Hna ghadi t3yet l-Simulator li fih Pygame (mn b3d)
            pass
        else:
            # Hna ghadi t3yet l-Simulator dyal T-terminal (Turn by turn f Console)
            pass

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()