*This project has been created as part of the 42 curriculum by skoulal.*

# 🚁 Fly-In: Drone Routing & Simulator

## 📌 Description
Fly-In is an advanced, object-oriented drone logistics simulator built in Python. The core goal of this project is to intelligently route a fleet of drones from a starting hub to a destination hub across a custom-built graph network, minimizing the total number of turns required.

The simulation strictly enforces complex mechanical constraints, including:
- **Zone Capacities:** Maximum number of drones allowed in a hub (`max_drones`).
- **Link Capacities:** Maximum drones traversing a connection simultaneously (`max_link_capacity`).
- **Zone Movement Costs:** Different rules for `normal` (1 turn), `priority` (preferred algorithmically), `restricted` (takes 2 turns), and `blocked` (inaccessible) zones.

This project focuses heavily on algorithmic efficiency, concurrency (deadlock prevention), and robust input parsing, with the ultimate goal of solving the complex "Challenger" maps in record turns.

---

## ⚙️ Instructions

### Prerequisites
- Python 3.10 or higher.
- `pygame` (required for the visualizer).

### Compilation & Installation
The project uses a Makefile to set up a clean virtual environment, ensuring execution without system-wide dependency conflicts.
```bash
# Clone the repository
cd fly-in

# Create the virtual environment and install dependencies
make install

# for the interactive mode
make menu
```

### Execution

To run the standard terminal simulation (calculates turns and prints movements to stdout):

```bash
# Activate the virtual environment
source fly_in_venv/bin/activate

# Run the simulation on a specific map
python3 fly_in.py maps/01_linear_path.txt

```

To launch the interactive Pygame 2D renderer:

```bash
python3 fly_in.py maps/01_linear_path.txt --viz
```


---

## 🧠 Algorithm Explanation & Implementation Strategy

### 1. Custom Graph Implementation

The map is parsed into a custom Object-Oriented Graph without using any forbidden external libraries (like `networkx`). The codebase is entirely type-safe (`mypy` verified) with strict encapsulation to separate parsing, logic, and rendering.

### 2. Pathfinding: Reverse Dijkstra (Flow Field)

Instead of running a pathfinding algorithm for each drone individually (which is highly inefficient and causes recalculation loops), the engine uses a **Reverse Dijkstra** approach:

* The algorithm starts at the `end_hub` (Goal) and works backward, calculating the shortest distance to every other node in the graph.
* This creates a "Flow Field" (or heatmap). Drones simply "flow downhill" towards the goal by picking the neighboring node with the lowest distance cost.
* **Priority Zones** are mathematically favored by artificially lowering their edge weights during the calculation, while **Blocked Zones** are assigned infinite costs.

### 3. Concurrency & Conflict Resolution (Pipelining)

To prevent deadlocks and manage capacity limits, the engine uses a turn-based **Pipelining** system:

* In each turn, drones are evaluated sequentially based on their proximity to the goal.
* A drone can only move if its target zone has available `max_drones` capacity AND the connection has available `max_link_capacity`.
* If a path is temporarily bottlenecked, the drone gracefully waits in its current zone. Restricted zones correctly track a "dwell time" (2 turns) before allowing exit, ensuring no collisions or capacity breaches occur.

---

## 🎮 Visual Representation Features

The project includes a highly polished Pygame Visualizer (`ft_2D_renderer.py`) designed to enhance user experience and provide clear debugging feedback for massive maps.

* **Free Mode Camera (Pan & Zoom):** Instead of rigid, static rendering, the visualizer features a virtual camera system. Users can **Click & Drag** to pan around massive environments and use the **Mouse Wheel** to zoom in and out smoothly.
* **LERP Animation (Smooth Interpolation):** Drones do not teleport between nodes. Their movements are calculated using Linear Interpolation (LERP) based on the frame rate, providing smooth, realistic flight paths between hubs.
* **Dynamic Styling & Legend:** The renderer dynamically extracts colors from the parsed map (e.g., `[color=red]`). Zone types are mathematically drawn using custom geometry (e.g., a red slash for `blocked`, a yellow center for `priority`) and are documented in a real-time, transparent UI Legend.
* **Interactive Controls:** Users can play/pause the simulation using `[SPACE]`, and step through the simulation turn-by-turn using the `[LEFT]` and `[RIGHT]` arrow keys, allowing for granular inspection of traffic flow and bottleneck resolution.

---

## 📚 Resources

### Classic References

* [Dijkstra's Shortest Path Algorithm (Computerphile)](https://www.youtube.com/watch?v=GazC3A4OQTE)
* https://www.geeksforgeeks.org/dsa/introduction-to-graphs-data-structure-and-algorithm-tutorials/
* [Pygame Official Documentation](https://www.pygame.org/docs/)
* Flow Field Pathfinding concepts for crowd simulation.

### AI Usage

Artificial Intelligence (LLMs) was utilized strictly as an educational tutor and debugging assistant during the development of this project:

* **Architectural Brainstorming:** Used AI to discuss the theoretical differences between A* and Dijkstra, leading to the decision to use a Reverse Dijkstra (Flow Field) approach for multi-agent routing.
* **Math Visualization (LERP):** Consulted AI to understand the mathematical formula behind Linear Interpolation ($P(t) = A + (B - A) \times t$) to implement smooth drone animations in Pygame without using external animation libraries.
* **Environment Debugging:** Used AI to diagnose specific Python virtual environment vs. global system path issues when integrating Pygame with macOS.



