import platform
import subprocess
import traceback


def start_pipeline_sh():
    """
    Starts the data pipeline bash script.
    """
    subprocess.run(['bash', './env/scripts/sh/run-pipeline.sh'])

def start_pipeline_ps1():
    """
    Starts the data pipeline ps1 script.
    """
    subprocess.run(['powershell', "-ExecutionPolicy", "Bypass", '-File', './env/scripts/ps1/run-pipeline.ps1'])

def main():
    """
    Main program loop for running the pipeline.
    """
    if platform.system() == 'Windows':
        print("Running on Windows...")
        start_pipeline_ps1()
    else:
        print("Running on Linux/macOS/WSL...")
        start_pipeline_sh()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An exception occurred...")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")
        print(f"Arguments: {e.args}")
        print("Traceback:")
        traceback.print_exc()