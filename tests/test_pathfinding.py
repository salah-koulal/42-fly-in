from src.ft_parser import MapParser
from src.algorithms.path_finder import PathFinder

if __name__ == "__main__":
    from src.algorithms.path_finder import PathFinder
    print("Here! we're just parsing that sh**t")
    parser = MapParser()

    try:
        parsed_map = parser.file_parsing("./maps/easy/01_linear_path.txt")
        
        print(f"\nL-GPS (Pathfinder) is starting from the goal and spread over all zones ! '{parsed_map.start_hub.name}' l '{parsed_map.end_hub.name}'...")
        pf = PathFinder(parsed_map)
        distances = pf.distances
        
        if distances:
            print(f"we found all distances that are faraway from goal:  {distances}")
        else:
            print("\nno distances there is a problem in reverse dijkastra")
            
    except Exception as e:
        print(f"ERROR: {e}")
