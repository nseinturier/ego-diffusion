from src.config.core import ROOT
from src.transfer.download import download_list_of_files
from src.transfer.download_utils import filter_existing_files, list_files_to_download, get_headers

from logzero import logger
from pathlib import Path
import asyncio

CUSTOM_NODE_FOLDER = ROOT / "ComfyUI" / "custom_nodes"

CN_DIR_FILES_URL = {
    ROOT / "ComfyUI" / "models" / "ultralytics" / "bbox": [
        "https://huggingface.co/sid38/custom_nodes/resolve/main/Eyes.pt",
        "https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8m.pt"
    ],
    ROOT / "ComfyUI" / "models" / "ultralytics" / "segm": [
        "https://github.com/hben35096/assets/releases/download/yolo8/face_yolov8m-seg_60.pt",
        "https://huggingface.co/Bingsu/adetailer/resolve/main/person_yolov8m-seg.pt",
        "https://github.com/hben35096/assets/releases/download/yolo8/skin_yolov8m-seg_400.pt"
    ],
    CUSTOM_NODE_FOLDER / "ComfyUI_essentials" / "luts": [
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Basin.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Boulder.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Butte.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Everest.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Hopkins.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_LochNess.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Oaxaca.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Oslo.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Phoenix.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Pocatello.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Prague.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Reykjavik.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_SantaFe.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Seattle.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Stillwater.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Tahoe.CUBE",
        "https://huggingface.co/sid38/custom_nodes/resolve/main/luts/PB_Thames.CUBE"
    ],
    CUSTOM_NODE_FOLDER / "ComfyUI-YoloWorld-EfficientSAM": [
        "https://huggingface.co/camenduru/YoloWorld-EfficientSAM/resolve/main/efficient_sam_s_gpu.jit"
    ]
}

def prepare_download_list_custom_nodes(
        custom_nodes_files_url: dict[Path, list]
)->list[dict[str, str]]:
    download_list = []

    for output_dir, urls in custom_nodes_files_url.items():
        if not output_dir.exists():
            if "ultralytics" in output_dir.__str__():
                output_dir.mkdir(parents=True, exist_ok=True)
            else:
                continue

        download_sublist = []

        for url in urls:
            output_path = output_dir / Path(url).name
            download_dict = {
                "url": url,
                "output_path": output_path.__str__(),
                "headers": get_headers(url)
            }        
            download_sublist.append(download_dict)

        download_list += download_sublist
        
    download_list = filter_existing_files(download_list)
    return download_list

def download_custom_nodes_resources():
    download_list = prepare_download_list_custom_nodes(CN_DIR_FILES_URL)
    all_files = list_files_to_download(download_list)

    logger.info(f"Preparing to download {all_files}...")
    asyncio.run(download_list_of_files(download_list))


if __name__ == "__main__":
    download_custom_nodes_resources()
