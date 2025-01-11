# Base image with CUDA 12.2
FROM nvidia/cuda:12.4.1-base-ubuntu22.04

# Prevents prompts from packages asking for user input during installation
ENV DEBIAN_FRONTEND=noninteractive

# Prefer binary wheels over source distributions for faster pip installations
ENV PIP_PREFER_BINARY=1

# Prevents Python from buffering output, ensuring that logs are flushed immediately
ENV PYTHONUNBUFFERED=1

ENV MOD_ENV="kohya"

# Set workspace environment variable
ENV WORKSPACE=/workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    git \
    wget \
    python3-pip \
    python3-venv \
    python3-tk \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Make python terminal command points toward python3.10
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Clean up to reduce image size
RUN apt-get autoremove -y \
&& apt-get clean -y \
&& rm -rf /var/lib/apt/lists/*

# Create workspace directories
WORKDIR ${WORKSPACE}
RUN mkdir -p ${WORKSPACE}/logs && \
    mkdir -p training_images && \
    mkdir -p trained_model_files

# Set CUDA environment variables
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

######### KOHYA #########

# Clone the repository and set the specific branch
RUN git clone --recursive -b sd3-flux.1 https://github.com/bmaltais/kohya_ss.git

COPY Docker/kohya/custom_requirements.txt ${WORKSPACE}/kohya_ss/custom_requirements.txt

# Install requirements
RUN cd kohya_ss && \
    pip install --upgrade pip && \
    pip install -r custom_requirements.txt && \
    pip cache purge


EXPOSE 7860

####### CODE SERVER ########

# Install code-server
RUN curl -fL https://code-server.dev/install.sh | sh

# Copy start script
COPY Docker/kohya/start.sh ${WORKSPACE}/start.sh
RUN chmod +x ${WORKSPACE}/start.sh

EXPOSE 8188

####### Src files ########
COPY src/ $WORKSPACE/src/
COPY setup.py project_setup.sh requirements.txt $WORKSPACE/

RUN bash project_setup.sh

# Create info file
RUN echo "Kohya is running. Check the logs for more information." > ${WORKSPACE}/logs/info.txt

CMD ["/bin/bash", "/workspace/start.sh"]