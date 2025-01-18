from src.config.core import config, DownloadConfig
from src.transfer.download import download_list_of_files
from src.transfer.download_utils import list_files_to_download, prepare_download_list, filter_existing_files

from logzero import logger
import asyncio

def run():
    downloads_info = config.downloads_info.__dict__
    download_info_filtered = filter_enabled_config(downloads_info)
    download_list = prepare_download_list(download_info_filtered)
    all_files = list_files_to_download(download_list)

    logger.info(f"Preparing to download {all_files}...")
    asyncio.run(download_list_of_files(download_list))


#### UTILS ####

def filter_enabled_config(downloads_info: dict) -> dict[str, dict[str, dict[str, DownloadConfig]]]:
    """filter the config to keep files with enabled=True"""
    filtered_dict = {
        category: {
            key: value for key, value in items.items()
            if value.enabled
        }
        for category, items in downloads_info.items()
    }
    return {k:v for k,v in filtered_dict.items() if len(v) > 0}

if __name__ == "__main__":
    run()