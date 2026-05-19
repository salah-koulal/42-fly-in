import os
import subprocess

BENCHMARKS = {
    "maps/easy/01_linear_path.txt": 6,
    "maps/easy/02_simple_fork.txt": 6,
    "maps/easy/03_basic_capacity.txt": 8,
    "maps/medium/01_dead_end_trap.txt": 15,
    "maps/medium/02_circular_loop.txt": 20,
    "maps/medium/03_priority_puzzle.txt": 12,
    "maps/hard/01_maze_nightmare.txt": 45,
    "maps/hard/02_capacity_hell.txt": 60,
    "maps/hard/03_ultimate_challenge.txt": 35,
}

def main():
    print("Testing Benchmarks...")
    print("-" * 50)
    passed = 0
    
    for map_path, target_turns in BENCHMARKS.items():
        if not os.path.exists(map_path):
            print(f"⚠️  [SKIP] Map not found: {map_path}")
            continue
            
        file_name = os.path.basename(map_path)
        
        # Run the simulator on the map
        result = subprocess.run(
            ["./fly-in_venv/bin/python3", "fly-in.py", map_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ [ERROR] {file_name} failed to execute.")
            continue
            
        # Count turns by counting lines of output (each line is a turn)
        output_lines = result.stdout.strip().splitlines()
        # Filter out random print statements if any (like distances)
        turns = 0
        for line in output_lines:
            if line.startswith("D"):  # Valid movement lines start with D
                turns += 1
                
        if turns <= target_turns:
            passed += 1
            print(f"✅ [PASS] {file_name} -> Solved in {turns} turns (Target: ≤ {target_turns})")
        else:
            print(f"❌ [FAIL] {file_name} -> Solved in {turns} turns (Target: ≤ {target_turns})")

    print("-" * 50)
    print(f"Results: {passed}/{len(BENCHMARKS)} benchmarks passed.")

if __name__ == "__main__":
    main()
