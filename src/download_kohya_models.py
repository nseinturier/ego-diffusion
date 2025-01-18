from src.config.core import config, DownloadConfig
from src.transfer.download import download_list_of_files
from src.transfer.download_utils import list_files_to_download, prepare_download_list, filter_existing_files

from logzero import logger
import asyncio

MODELS_TO_DOWNLOAD = [
    "flux1-dev.safetensors",
    "t5xxl_fp16.safetensors",
    "clip_l.safetensors",
    "ae.safetensors"
]

def run():
    downloads_info = config.downloads_info.__dict__
    download_info_filtered = filter_config_by_name(downloads_info, MODELS_TO_DOWNLOAD)
    download_list = prepare_download_list(download_info_filtered)
    all_files = list_files_to_download(download_list)
    
    logger.info(f"Preparing to download {all_files}...")
    asyncio.run(download_list_of_files(download_list))

def filter_config_by_name(
        downloads_info: dict,
        model_names: list[str]
) -> dict[str, dict[str, dict[str, DownloadConfig]]]:
    filtered_config = {
        outer_key: {k: v for k, v in inner_dict.items() if k in model_names}
        for outer_key, inner_dict in downloads_info.items()
    }
    return filtered_config

if __name__ == "__main__":
    run()