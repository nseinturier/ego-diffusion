from src.config.core import ROOT
from src.in_out.download import download_file
from logzero import logger
from pathlib import Path

CUSTOM_NODE_FOLDER = ROOT / "ComfyUI" / "custom_nodes"

CN_DIR_FILES_URL = {
    ## Impact pack
    ROOT / "ComfyUI" / "models" / "ultralytics" / "bbox": {
        "Eyes.pt" : "https://huggingface.co/sid38/custom_nodes/resolve/main/Eyes.pt"
    },

    ## Comfy Essentials
    CUSTOM_NODE_FOLDER / "ComfyUI_essentials" / "luts": {
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
    },

    ## Yoloworld
    CUSTOM_NODE_FOLDER / "ComfyUI-YoloWorld-EfficientSAM": {
        "efficient_sam_s_gpu.jit": "https://huggingface.co/camenduru/YoloWorld-EfficientSAM/resolve/main/efficient_sam_s_gpu.jit"
    }
}

def run():
    for custom_node_path, files_urls in CN_DIR_FILES_URL.items():
        files_downloader(files_urls, custom_node_path)

def files_downloader(
        files_urls: dict[str, str],
        custom_node_directory: Path
)-> None:
    """
    Given a dict of file names and download urls, download all the files in the given repository, only if the output path exists and the file is not already downloaded 
    """
    for file_name, url in files_urls.items():
        file_full_path = custom_node_directory / file_name

        if custom_node_directory.exists() and not file_full_path.exists():
            logger.info(f"Downloading {file_name}")
            download_file(url, file_name, output_path = custom_node_directory)
        else:
            logger.info(f"Skipping {file_name} download: custom node not installed or file already downloaded")

if __name__ == "__main__":
    run()
