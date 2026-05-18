"""Automated testing script to verify error handling for invalid maps."""

import os
import glob
import subprocess


def main():
    """Runs tests against all invalid map configurations.

    Iterates over all .txt files in maps/error/, runs the simulator, and ensures
    that each invalid map is successfully rejected with a non-zero exit code.
    """
    error_maps = glob.glob("maps/error/*.txt")
    if not error_maps:
        print("No error maps found.")
        return

    passed_tests = 0
    failed_tests = []

    print(f"Testing {len(error_maps)} error maps against fly-in.py...")
    print("-" * 50)

    for file_path in sorted(error_maps):
        file_name = os.path.basename(file_path)

        # Run fly-in.py on the error map
        # We expect a non-zero exit code because it's an error map
        result = subprocess.run(
            ["./fly-in_venv/bin/python3", "fly-in.py", file_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            passed_tests += 1
            # Get the first line of stderr or stdout as the error message
            err_output = result.stderr.strip() or result.stdout.strip()
            err_msg = err_output.splitlines()
            err_line = err_msg[-1] if err_msg else "Unknown Error"
            print(f"✅ [PASS] {file_name} -> Rejected successfully: {err_line}")
        else:
            failed_tests.append(
                (file_name, "Parsed and executed successfully without error!")
            )
            print(f"❌ [FAIL] {file_name} -> Did not throw an error (Exit 0)!")

    print("-" * 50)
    print(f"Results: {passed_tests}/{len(error_maps)} tests passed.")

    if failed_tests:
        print("\nFailed Tests Details:")
        for name, reason in failed_tests:
            print(f" - {name}: {reason}")
    else:
        print("\nAll error edge cases correctly rejected by the program! 🎉")


if __name__ == "__main__":
    main()
