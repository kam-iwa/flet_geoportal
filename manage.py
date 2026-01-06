import argparse
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("parameter", nargs='?', help=" - Available parameters: `up`, `build`, `restart`, `down`. Description of parameters is available in readme file.")
args = parser.parse_args()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Missing parameter. Program will exit now.\n{'=' * 25}")
        parser.print_help()
        sys.exit(-1)

    if sys.argv[1].lower() == "up":
        print(f"Run API. \n{'=' * 25}")
        subprocess.run(["docker", "compose", "up"])
    elif sys.argv[1].lower() == "build":
        print(f"Build API.\n{'=' * 25}")
        subprocess.run(["docker", "compose", "build"])
    elif sys.argv[1].lower() == "restart":
        print(f"Restart API.\n{'=' * 25}")
        subprocess.run(["docker", "compose", "restart"])
    elif sys.argv[1].lower() == "down":
        print(f"Exit API.\n{'=' * 25}")
        subprocess.run(["docker", "compose", "down"])
    else:
        print(f"Invalid parameter. Program will exit now.\n{'=' * 25}")
        parser.print_help()
        sys.exit(-1)