import subprocess
import os

def run_command(command, shell_type=True):
    """Run command and print output and errors."""
    result = subprocess.run(command, shell=shell_type, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("Error:", result.stderr)

# Checking NVIDIA GPU status
run_command("nvidia-smi")

# Path for the Miniconda installer in Windows
miniconda_installer_path = r"C:\temp\miniconda.sh"
os.makedirs(r"C:\temp", exist_ok=True)  # Ensure temp directory exists

# Download Miniconda for Linux in WSL using PowerShell
run_command(f"powershell wget https://repo.anaconda.com/miniconda/Miniconda3-py310_24.3.0-0-Linux-x86_64.sh -OutFile {miniconda_installer_path}")

# Convert Windows path to WSL path
wsl_miniconda_installer_path = miniconda_installer_path.replace('C:\\', '/mnt/c/').replace('\\', '/')

# Installing Miniconda in WSL with sudo to avoid permission issues
run_command(f"wsl sudo bash {wsl_miniconda_installer_path} -b -p /opt/conda")

# Remove the installer script in Windows after installation
os.remove(miniconda_installer_path)

# Initialize Conda in WSL
run_command("wsl sudo /opt/conda/bin/conda init")

print("Setup completed successfully.")
