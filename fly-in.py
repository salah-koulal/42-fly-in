import argparse
import sys
from src.ft_parser import MapParser
from src.algorithms.path_finder import PathFinder
from src.ft_engine import Simulator
from src.ft_2D_renderer import Renderer2D


def main():
    """Main entry point for the fly-in drone simulator.

    Parses command-line arguments, validates the input map, initializes the
    simulation engine, runs the simulation, and optionally visualizes it.
    """
    parser_args = argparse.ArgumentParser(
        description="Fly-in: Drone Routing & Simulator"
    )
    parser_args.add_argument(
        "map_file", help="Path to the map .txt file (e.g., maps/test.txt)"
    )
    parser_args.add_argument(
        "--viz", action="store_true", help="Enable Pygame visualization"
    )
    parser_args.add_argument("--capacity_info", action="store_true")

    args = parser_args.parse_args()

    try:

        parser = MapParser()
        parsed_map = parser.file_parsing(args.map_file)

        pf = PathFinder(parsed_map)
        print(pf.distances)
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
        i = 0
        if args.capacity_info:
            for name in parsed_map.zones:
                if i >= len(parsed_map.connections):
                    break
                print(
                    f"zone {parsed_map.zones[name].name} : "
                    f"{parsed_map.zones[name].max_drones} "
                    f" | connection {parsed_map.connections[i].zone1.name}-"
                    f"{parsed_map.connections[i].zone2.name} "
                    f" | capacity used: "
                    f"{parsed_map.connections[i].max_link_capacity}"
                )
                i += 1

    except BaseException as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
