from src.config.core import config, DownloadConfig
from src.in_out.download import download_file
from logzero import logger


def run():
    """
    Download all the models defined in the to_download.yaml file
    """
    downloads_info = config.downloads_info.__dict__
    all_files = list_enabled_files(downloads_info)
    filtered_downloads_info = filter_enabled_config(downloads_info)

    logger.info(f"Preparing to download {all_files}...")

    for download_type in filtered_downloads_info:    
            logger.info(f"Downloading {download_type}...")
            output_dir = config.download_outputs_path[download_type]

            for file_name, file_download_info in filtered_downloads_info[download_type].items():
                file_path = output_dir / file_name

                if file_path.exists():
                    logger.info(f"File {file_name} already exists, skipping download...")
                    continue
                
                logger.info(f"Downloading {file_name}...")
                url = file_download_info.url
                download_file(url, file_name, download_type)


def filter_enabled_config(config: dict) -> dict[str, dict[str, dict[str, DownloadConfig]]]:
    filtered_dict = {
        category: {
            key: value for key, value in items.items()
            if value.enabled
        }
        for category, items in config.items()
    }
    return {k:v for k,v in filtered_dict.items() if len(v) > 0}


def list_enabled_files(config: dict) -> list[str]:
    return [
        filename
        for category, items in config.items()
        for filename, details in items.items()
        if details.enabled
    ]


if __name__ == "__main__":
    run()