#!/bin/bash
set -x

echo "Starting code-server..."
code-server --bind-addr 0.0.0.0:8188 --auth none --user-data-dir /workspace/.vscode-server --extensions-dir /workspace/.vscode-server/extensions . &

echo "Contents of info.txt:"
cat $WORKSPACE/logs/info.txt

echo "Starting ComfyUI..."
touch $WORKSPACE/logs/comfyui.log
cd $WORKSPACE/ComfyUI && python main.py --listen --port 8080 --cpu > $WORKSPACE/logs/comfyui.log 2>&1 &

echo "Waiting for ComfyUI to start..."
sleep 5

echo "Tailing ComfyUI logs..."
tail -f $WORKSPACE/logs/comfyui.log