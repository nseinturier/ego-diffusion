from src.config.core import config, DownloadConfig
from pathlib import Path
from logzero import logger

def get_output_path(
        file_name: str,
        download_type: str
)-> str:
    return (config.download_outputs_path[download_type] / file_name).__str__()


def get_headers(
        url: str
)-> dict[str, str]:
    headers = {}
    if "huggingface" in url:
        headers["Authorization"] = f"Bearer {config.hf_token}"
    elif "civitai" in url:
        headers["Authorization"] = f"Bearer {config.civitai_token}"
    return headers


def list_files_to_download(download_list: list[dict]) -> list[str]:
    return [Path(dl_dict["output_path"]).name for dl_dict in download_list]


def prepare_download_list(download_info_filtered: dict[str, dict])->list[dict]:
    download_list = []

    for download_type, models_configs in download_info_filtered.items():
        download_list_for_dl_type = []

        for file_name, download_config in models_configs.items():
            model_config = {
                "url": download_config.url,
                "headers": get_headers(download_config.url),
                "output_path": get_output_path(file_name, download_type)
            }
            download_list_for_dl_type.append(model_config)
        download_list += download_list_for_dl_type
        
    download_list = filter_existing_files(download_list)
    return download_list


def filter_existing_files(
        download_list: dict[str, dict]
)-> dict[str, dict]:
    """remove downloads where files are already existings"""
    download_list_filtered = []

    for file in download_list:
        if Path(file["output_path"]).exists():
            logger.info(f"File {Path(file['url']).name} already exists, skipping download...")
        else:
            download_list_filtered.append(file)
    return download_list_filtered