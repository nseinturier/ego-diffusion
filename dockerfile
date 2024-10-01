# Use an NVIDIA CUDA base image with Ubuntu
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Prevents prompts from packages asking for user input during installation
ENV DEBIAN_FRONTEND=noninteractive

# Prefer binary wheels over source distributions for faster pip installations
ENV PIP_PREFER_BINARY=1

# Prevents Python from buffering output, ensuring that logs are flushed immediately
ENV PYTHONUNBUFFERED=1

ENV WORKSPACE=/workspace

RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    curl \
    git \
    wget

# Clean up to reduce image size
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* 

RUN mkdir -p /workspace $WORKSPACE/ComfyUI $WORKSPACE/logs
RUN git clone https://github.com/comfyanonymous/ComfyUI.git $WORKSPACE/ComfyUI
RUN git clone https://github.com/ltdrdata/ComfyUI-Manager.git $WORKSPACE/ComfyUI/custom_nodes/ComfyUI-Manager

WORKDIR /workspace

# Install requirements
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu124

RUN pip install -r $WORKSPACE/ComfyUI/requirements.txt
RUN curl -fL https://code-server.dev/install.sh | sh

EXPOSE 8188 8080

# Create an info.txt file (you can modify this content as needed)
RUN echo "ComfyUI is running. Check the logs for more information." > $WORKSPACE/logs/info.txt

# Copy ego-diffusion files into the image
COPY src/ $WORKSPACE/src/
COPY setup.py project_setup.sh requirements.txt download_models.sh $WORKSPACE/

RUN bash project_setup.sh

# Copy the start script into the image
COPY start.sh $WORKSPACE/start.sh
RUN chmod +x $WORKSPACE/start.sh

# Set the startup command
CMD ["/bin/bash", "/workspace/start.sh"]