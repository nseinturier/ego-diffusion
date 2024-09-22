from src.config.core import config
from src.in_out.download import download_file
from logzero import logger

LUTS_FILES = {
    "PB_Basin.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Basin.CUBE",
    "PB_Boulder.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Boulder.CUBE",
    "PB_Butte.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Butte.CUBE",
    "PB_Everest.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Everest.CUBE",
    "PB_Hopkins.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Hopkins.CUBE",
    "PB_LochNess.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_LochNess.CUBE",
    "PB_Oaxaca.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Oaxaca.CUBE",
    "PB_Oslo.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Oslo.CUBE",
    "PB_Phoenix.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Phoenix.CUBE",
    "PB_Pocatello.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Pocatello.CUBE",
    "PB_Prague.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Prague.CUBE",
    "PB_Reykjavik.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Reykjavik.CUBE",
    "PB_SantaFe.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_SantaFe.CUBE",
    "PB_Seattle.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Seattle.CUBE",
    "PB_Stillwater.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Stillwater.CUBE",
    "PB_Tahoe.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Tahoe.CUBE",
    "PB_Thames.CUBE": "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Thames.CUBE"
}

CUSTOM_NODE_FOLDER_NAME = config.custom_nodes_folder / "ComfyUI_essentials" / "luts"


def run():
    for file_name, file_url in LUTS_FILES.items():
        download_lut_file(file_name, file_url)

def download_lut_file(
        file_name: str,
        file_url: str
)-> None:
    """
    Install efficient_sam_s_gpu.jit only if the custom node is installed
    """
    full_path = CUSTOM_NODE_FOLDER_NAME / file_name

    if CUSTOM_NODE_FOLDER_NAME.exists() and not full_path.exists():
        logger.info(f"Downloading {file_name}.jit")
        download_file(file_url, file_name, output_path = CUSTOM_NODE_FOLDER_NAME)

if __name__ == "__main__":
    run()