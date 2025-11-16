#!/bin/bash

# Check if the conda environment 'stepaudioedit' exists
if conda env list | grep -q "stepaudioedit"; then
    echo "Conda environment 'stepaudioedit' found."
    echo "Updating dependencies..."
    conda run -n stepaudioedit pip install -r requirements.txt --upgrade
    echo "Launching the application..."
    python launcher.py
else
    echo "Conda environment 'stepaudioedit' not found."
    echo "Running the installer..."
    python install.py

    # Check if the installation was successful before launching
    if conda env list | grep -q "stepaudioedit"; then
        echo "Installation complete. Launching the application..."
        python launcher.py
    else
        echo "Installation failed. Please check the logs."
    fi
fi
