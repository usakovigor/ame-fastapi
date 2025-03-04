FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu20.04
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends git curl software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt install -y python3.10 python3.10-distutils && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10


RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 2 && \
    update-alternatives --auto python3

RUN export CUDA_HOME=/usr/local/cuda/

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . .

# Make port 8500 available to the world outside this container
EXPOSE 8500

# Define environment variable
ENV NAME World

# Run app.py when the container launches using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8500"]
