from src.config.core import config
from src.in_out.download import download_file
from logzero import logger


def main():
    """
    Download all the models defined in the to_download.yaml file
    """
    all_files = [file_name for file_type in config.download_urls.keys() for file_name in config.download_urls[file_type].keys()]
    logger.info(f"Preparing to download {all_files}...")

    for download_type in config.download_urls:    
        if len(config.download_urls[download_type]) > 0:
            logger.info(f"Downloading {download_type}...")

            for file_name in config.download_urls[download_type]:
                logger.info(f"Downloading {file_name}...")
                url = config.download_urls[download_type][file_name]
                download_file(url, file_name, download_type)

if __name__ == "__main__":
    main()