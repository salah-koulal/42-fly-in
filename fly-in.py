import argparse
import sys
from src.ft_parser import MapParser
from src.algorithms.path_finder import PathFinder
from src.ft_engine import Simulator
from src.ft_2D_renderer import Renderer2D


def main():
    """Main entry point for the fly-in drone simulator."""
    parser_args = argparse.ArgumentParser(
        description="Fly-in: Drone Routing & Simulator"
    )
    parser_args.add_argument(
        "map_file", help="Path to the map .txt file (e.g., maps/test.txt)"
    )
    parser_args.add_argument(
        "--viz", action="store_true", help="Enable Pygame visualization"
    )
    args = parser_args.parse_args()

    try:
        parser = MapParser()
        parsed_map = parser.file_parsing(args.map_file)

        pf = PathFinder(parsed_map)
        start_name = parsed_map.start_hub.name
        sim = Simulator(parsed_map)
        sim.run_all()
        engine_history = sim.history
        if pf.get_distance(start_name) == float("inf"):
            print("No path found! Drones are stuck.!")
            sys.exit(1)
        if args.viz:
            renderer = Renderer2D(parsed_map, engine_history)
            renderer.run()
        else:
            sim.run_all()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
