#!/bin/bash
set -ex  # Exit on error and print commands

# Start code-server
echo "Starting code-server..."
code-server --bind-addr 0.0.0.0:8188 --auth none \
    --user-data-dir ${WORKSPACE}/.vscode-server \
    --extensions-dir ${WORKSPACE}/.vscode-server/extensions . &

# Display info
echo "Contents of info.txt:"
cat ${WORKSPACE}/logs/info.txt

# Start Kohya UI with logging
echo "Starting Kohya UI..."
touch ${WORKSPACE}/logs/kohya.log
cd ${WORKSPACE}/kohya_ss && python kohya_gui.py --listen 0.0.0.0 --headless --noverify > ${WORKSPACE}/logs/kohya.log 2>&1 &

echo "Tailing Kohya logs..."
tail -f "${WORKSPACE}/logs/kohya.log" &

echo "Starting downloading models..."
python3 $WORKSPACE/src/download_kohya.py

# Keep container running
tail -f /dev/null