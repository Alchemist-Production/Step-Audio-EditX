import os
import subprocess
import sys

def main():
    """
    Launches the Step-Audio-EditX application.
    """
    # Activate the conda environment and run the app.py script
    command = [
        "conda",
        "run",
        "-n",
        "stepaudioedit",
        "python",
        "app.py",
        "--model-path",
        ".",
        "--model-source",
        "local",
    ]

    print(f"Running command: {' '.join(command)}")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while launching the application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
