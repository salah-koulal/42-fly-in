from src.ft_parser import MapParser
from src.algorithms.path_finder import PathFinder

if __name__ == "__main__":
    from src.algorithms.path_finder import PathFinder
    print("Here! we're just parsing that sh**t")
    parser = MapParser()

    try:
        parsed_map = parser.file_parsing("./maps/easy/01_linear_path.txt")
        
        print(f"\n🗺️ L-GPS (Pathfinder) is looking for the dest ! '{parsed_map.start_hub.name}' l '{parsed_map.end_hub.name}'...")
        pf = PathFinder(parsed_map)
        # shortest_path = pf.dijkstra(parsed_map.start_hub.name, parsed_map.end_hub.name)
        distances = pf.distances
        
        if distances:
            print(f"\n✅ we found all distances that are faraway from goal:  {distances}")
        else:
            print("\n❌ no distances there is a problem in reverse dijkastra")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
