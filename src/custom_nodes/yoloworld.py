from src.config.core import config
from src.in_out.download import download_file
from logzero import logger

CUSTOM_NODE_FOLDER_NAME = config.custom_nodes_folder / "ComfyUI-YoloWorld-EfficientSAM"
FILE_NAME = "efficient_sam_s_gpu.jit"
URL = "https://huggingface.co/camenduru/YoloWorld-EfficientSAM/resolve/main/efficient_sam_s_gpu.jit"


def run()-> None:
    """
    Install efficient_sam_s_gpu.jit only if the custom node is installed
    """
    full_path = CUSTOM_NODE_FOLDER_NAME / FILE_NAME

    if CUSTOM_NODE_FOLDER_NAME.exists() and not full_path.exists():
        logger.info("Downloading efficient_sam_s_gpu.jit")
        download_file(URL, FILE_NAME, output_path = CUSTOM_NODE_FOLDER_NAME)
    else:
        logger.info("Skipping efficient_sam_s_gpu download: custom node not installed or file already downloaded")

if __name__ == "__main__":
    run()