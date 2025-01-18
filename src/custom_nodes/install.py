import subprocess
import sys
from src.custom_nodes.download_cn_resources import download_custom_nodes_resources
import json
from src.config.core import ROOT

COMFYUI_MANAGER_PATH = ROOT / "ComfyUI" / "custom_nodes" / "ComfyUI-Manager"
CM_CLI_PATH = COMFYUI_MANAGER_PATH / "cm-cli.py"
JSON_PATH = COMFYUI_MANAGER_PATH / "custom-node-list.json"

NODES_TO_INSTALL = [
    "https://github.com/ltdrdata/ComfyUI-Impact-Pack",
    "https://github.com/ltdrdata/ComfyUI-Impact-Subpack",
    "https://github.com/ltdrdata/ComfyUI-Inspire-Pack",
    "https://github.com/cubiq/ComfyUI_essentials",
    "https://github.com/chrisgoringe/cg-use-everywhere",
    "https://github.com/rgthree/rgthree-comfy",
    "https://github.com/cubiq/PuLID_ComfyUI",
    #"https://github.com/ZHO-ZHO-ZHO/ComfyUI-YoloWorld-EfficientSAM",
    "https://github.com/BadCafeCode/masquerade-nodes-comfyui",
    "https://github.com/Ryuukeisyou/comfyui_face_parsing",
    "https://github.com/logtd/ComfyUI-Fluxtapoz",
    "https://github.com/Jonseed/ComfyUI-Detail-Daemon",
    "https://github.com/kijai/ComfyUI-KJNodes",
    "https://github.com/storyicon/comfyui_segment_anything"
]

def load_node_description():
    with open(JSON_PATH, "r") as file:
        return json.load(file)
    
NODES_DESCRIPTION = load_node_description()

def install_custom_node(node_id: str):
    cmd = [sys.executable, str(CM_CLI_PATH), "install", node_id] 
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)


    for line in process.stdout:
        print(line, end='')

    process.wait()
    if process.returncode != 0:
        print(f"Error: Process exited with code {process.returncode}", file=sys.stderr)
        return

    node_data = next((node for node in NODES_DESCRIPTION['custom_nodes'] if node.get('reference') == node_id), None)
    
    if node_data and 'pip' in node_data:
        print(f"Installing pip dependencies for {node_id}")
        for pip_package in node_data['pip']:
            subprocess.run([sys.executable, "-m", "pip", "install", pip_package], check=True)

def run():
    for custom_node in NODES_TO_INSTALL:
        install_custom_node(custom_node)

    download_custom_nodes_resources()

if __name__ == "__main__":
    run()