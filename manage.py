import argparse
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("parameter", nargs='?', help=" - Available parameters: `up`, `build`, `restart`, `down`. Description of parameters is available in readme file.")
parser.add_argument("-e", "--env-file", type=str, help="Path to alternative .env file (e.g., .env.production, .env.development)")
args = parser.parse_args()

COMMANDS = {
    "up": "Run APP",
    "build": "Build APP",
    "restart": "Restart APP",
    "down": "Exit APP"
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Missing parameter. Program will exit now.\n{'=' * 25}")
        parser.print_help()
        sys.exit(-1)

    command = sys.argv[1].lower()
    
    if command in COMMANDS:
        print(f"{COMMANDS[command]}.\n{'=' * 25}")
        
        docker_command = ["docker", "compose"]
        
        if args.env_file:
            docker_command.extend(["--env-file", args.env_file])
        
        docker_command.append(command)
        
        subprocess.run(docker_command)
    else:
        print(f"Invalid parameter. Program will exit now.\n{'=' * 25}")
        parser.print_help()
        sys.exit(-1)