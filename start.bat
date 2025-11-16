@echo off

REM Check if the conda environment 'stepaudioedit' exists
conda env list | findstr "stepaudioedit" > nul
if %errorlevel% == 0 (
    echo Conda environment 'stepaudioedit' found.
    echo Updating dependencies...
    conda run -n stepaudioedit pip install -r requirements.txt --upgrade
    echo Launching the application...
    python launcher.py
) else (
    echo Conda environment 'stepaudioedit' not found.
    echo Running the installer...
    python install.py

    REM Check if the installation was successful before launching
    conda env list | findstr "stepaudioedit" > nul
    if %errorlevel% == 0 (
        echo Installation complete. Launching the application...
        python launcher.py
    ) else (
        echo Installation failed. Please check the logs.
    )
)
