1. **List available Linux distributions for WSL and install a specific version**:
   ```bash
   wsl --list
   wsl --install -d Ubuntu-20.04
   ```

2. **Check NVIDIA GPU status**:
   ```bash
   nvidia-smi
   ```

3. **Update package lists and install wget**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y wget
   ```

4. **Download and install Miniconda**:
   ```bash
   wget https://repo.anaconda.com/miniconda/Miniconda3-py310_24.3.0-0-Linux-x86_64.sh -O /tmp/miniconda.sh
   sudo chmod +x /tmp/miniconda.sh
   /tmp/miniconda.sh -b -p /opt/conda
   sudo rm /tmp/miniconda.sh
   ```

5. **Initialize Conda to configure your shell**:
   ```bash
   sudo /opt/conda/bin/conda init
   ```

6. **Create a symbolic link for the Conda script to ensure it is loaded automatically**:
   ```bash
   sudo ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh
   ```

7. **Add Conda to the PATH in your `.bashrc` file and source it to reflect changes**:
   ```bash
   echo 'export PATH="/opt/conda/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

8. **Install a specific version of Python using Conda**:
   ```bash
   sudo conda install -y python=3.10
   ```

9. **Create a new Conda environment**:
   ```bash
   conda create --name llmtuning_env python=3.10
   ```

# Missed a few commands
- There are a few commands that are missing from the list above.


```bash
conda activate llmtuning_env
```
conda install pytorch=12.1 pytorch cudatoolkit xformers -c pytorch -c nvidia -c

pip install --no-deps trl peft accelerate bitsandbytes

pip install llm-toolkit

```bash
conda install numpy pandas scikit-learn
pip install tensorflow
```



'''
wsl --list
wsl --install -d Ubuntu-20.04

nvidia-smi

sudo apt-get update
sudo apt-get install -y wget

wget https://repo.anaconda.com/miniconda/Miniconda3-py310_24.3.0-0-Linux-x86_64.sh -O /tmp/miniconda.sh
sudo chmod +x /tmp/miniconda.sh
/tmp/miniconda.sh -b -p /opt/conda
sudo rm /tmp/miniconda.sh

sudo /opt/conda/bin/conda init

sudo ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh

echo 'export PATH="/opt/conda/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

sudo conda install -y python=3.10

conda create --name llmtuning_env python=3.10

conda activate llmtuning_env
conda install -c pytorch -c nvidia pytorch=1.12 cudatoolkit xformers

pip install --no-deps trl peft accelerate bitsandbytes

pip install llm-toolkit
'''

ls
nano input.json
sudo git clone https://github.com/georgian-io/LLM-Finetuning-Toolkit

config.yml - This is the main file that contains all of the information that needs to be set. Some related to hardware, and others related to the fine tuning job.

