from src.ft_parser import MapParser
from src.algorithms.path_finder import PathFinder

if __name__ == "__main__":
    from src.algorithms.path_finder import PathFinder
    print("Here! we're just parsing that sh**t")
    parser = MapParser()

    try:
        parsed_map = parser.file_parsing("./test.txt")
        
        print(f"\n🗺️ L-GPS (Pathfinder) is looking for the dest ! '{parsed_map.start_hub.name}' l '{parsed_map.end_hub.name}'...")
        pf = PathFinder(parsed_map)
        shortest_path = pf.dijkstra(parsed_map.start_hub.name, parsed_map.end_hub.name)
        
        if shortest_path:
            print(f"\n✅ we found it ! A lM3llem: {' -> '.join(shortest_path)}")
        else:
            print("\n❌ Malqina 7ta triq! d-drones ghadi tbqa wa7la.")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
