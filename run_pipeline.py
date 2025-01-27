import os
import platform
import subprocess
import sys
import traceback

"""
This script is the entry point for all users who want to run the pipeline.
"""

def start_pipeline_sh():
    """
    Starts the data pipeline bash script.
    """
    os.execvp("bash", ["bash", "./src/sh/run_pipeline.sh"])

def start_pipeline_ps1():
    """
    Starts the data pipeline ps1 script.
    """
    os.execvp("powershell", ["powershell", "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "./src/ps1/run-pipeline.ps1"])

def main():
    """
    Main program loop for running the pipeline.
    """
    if platform.system() == "Windows":
        print("Running on Windows...")
        start_pipeline_ps1()
    else:
        print("Running on Linux/macOS...")
        start_pipeline_sh()

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print("An exception occurred...")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")
        print(f"Arguments: {e.args}")
        print("Traceback:")
        traceback.print_exc()
        sys.exit(1)