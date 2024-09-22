# Use an NVIDIA CUDA base image with Ubuntu
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and Python
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Clone ComfyUI repository
RUN git clone https://github.com/comfyanonymous/ComfyUI.git /ComfyUI

# Set working directory
WORKDIR /ComfyUI

# Install PyTorch with CUDA support and other dependencies
RUN pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124 \
    && pip3 install -r requirements.txt

# Expose the ComfyUI port
EXPOSE 8188

# Set the startup command
CMD ["python3", "main.py", "--listen"]