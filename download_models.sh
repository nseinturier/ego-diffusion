#!/bin/sh

# Hardcoded paths to the Python scripts
MODEL_SCRIPT="src/download_models.py"  
CUSTOM_NODES_SCRIPT="src/custom_nodes/download_cn_resources.py"

# Initialize flags
RUN_MODEL=true
RUN_CUSTOM_NODES=true

# Parse command-line options
if [ "$1" == "--custom_nodes" ]; then
    RUN_MODEL=false
elif [ "$1" == "--models" ]; then
    RUN_CUSTOM_NODES=false
fi

# Run dataset script if flag is true
if $RUN_CUSTOM_NODES; then
    echo "Running custom nodes script..."
    python3 "$CUSTOM_NODES_SCRIPT"
fi

# Run model script if flag is true
if $RUN_MODEL; then
    echo "Running model script..."
    python3 "$MODEL_SCRIPT"
fi