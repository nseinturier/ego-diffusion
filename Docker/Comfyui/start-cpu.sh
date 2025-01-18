#!/bin/bash
set -x

echo "Starting code-server..."
code-server --bind-addr 0.0.0.0:8188 --auth none --user-data-dir /workspace/.vscode-server --extensions-dir /workspace/.vscode-server/extensions . &

echo "Contents of info.txt:"
cat $WORKSPACE/logs/info.txt

echo "Starting ComfyUI..."
touch $WORKSPACE/logs/comfyui.log
cd $WORKSPACE/ComfyUI && python3 main.py --cpu --listen --port 8080 > $WORKSPACE/logs/comfyui.log 2>&1 &

echo "Waiting for ComfyUI to start..."
sleep 5

echo "Tailing ComfyUI logs..."
tail -f "$WORKSPACE/logs/comfyui.log" &

echo "Downloading latest models list to download..."
curl -o "$WORKSPACE/src/config/models_config.yaml" https://raw.githubusercontent.com/nseinturier/ego-diffusion/main/src/config/models_config.yaml

echo "Starting downloading models..."
python3 $WORKSPACE/src/download_comfyui_models.py

# Keep the script running (for Docker)
tail -f /dev/null