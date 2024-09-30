import subprocess
import sys

def install(package):
    """Install the given package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Lies alle Pakete aus der requirements.txt
with open("requirements.txt") as f:
    packages = f.read().splitlines()

# Installiere alle Pakete
for package in packages:
    try:
        __import__(package.split('==')[0])  # Versucht, das Paket zu importieren
    except ImportError:
        print(f"{package} nicht installiert. Installiere...")
        install(package)
