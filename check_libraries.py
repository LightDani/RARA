import subprocess


def check_install(package):
    try:
        __import__(package)
    except ImportError:
        print(f"{package} is not installed. Installing...")
        subprocess.check_call(["pip", "install", package])
        print(f"{package} has been successfully installed.")
