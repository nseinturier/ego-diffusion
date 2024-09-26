import src
from pathlib import Path
import yaml
from pydantic import BaseModel, Field
from typing import Dict, Any, Literal
import os


# Constants
PACKAGE_ROOT = Path(src.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
TO_DOWNLOAD_YAML = PACKAGE_ROOT / 'to_download.yaml'
DOWNLOAD_URLS = PACKAGE_ROOT / 'config' / 'download_urls.yaml'

# Define the path structure for different environments
PATH_CONFIG = {
    "comfyUI": {
        "checkpoint": ROOT / "ComfyUI" / "models" / "checkpoints",
        "vae": ROOT / "ComfyUI" / "models" / "vae",
        "lora": ROOT / "ComfyUI" / "models" / "loras",
        "clip": ROOT / "ComfyUI" / "models" / "clip",
        "controlnet": ROOT / "ComfyUI" / "models" / "controlnet",
        "unet": ROOT / "ComfyUI" / "models" / "unet",
    },
    "kohya_ss": {
        "checkpoint": ROOT / "kohya_ss" / "models",
        "vae": ROOT / "kohya_ss" / "models" / "vae",
        # Note: 'lora' is not defined for kohya_ss
    },
}

def load_yaml_config(file_path: Path = None) -> Dict[str, Any]:
    """Load YAML configuration file."""
    file_path = file_path or find_env_config_file()
    with file_path.open("r") as file:
        return yaml.safe_load(file)

TO_DOWNLOAD_CONFIG = load_yaml_config(TO_DOWNLOAD_YAML)

def get_urls(
        download_type: Literal['checkpoint', 'lora', "vae", "controlnet"]
)-> dict[str, str]:
    if TO_DOWNLOAD_CONFIG[download_type] is None:
        return {}
    download_urls = load_yaml_config(DOWNLOAD_URLS)
    return {k: v for k, v in download_urls[download_type].items() if k in TO_DOWNLOAD_CONFIG[download_type]}

def get_all_files_urls()-> dict[str, str]:
    return {download_type: get_urls(download_type) for download_type in TO_DOWNLOAD_CONFIG.keys()}


class Config(BaseModel):
    mod_env: str = os.environ["MOD_ENV"]
    hf_token: str = os.environ["HF_TOKEN"]
    civitai_token: str = os.environ["CIVITAI_TOKEN"]
    custom_nodes_folder: Path = ROOT / "ComfyUI" / "custom_nodes"
    download_outputs_path: dict[str, Path] = PATH_CONFIG[mod_env]
    download_urls: dict[str, dict[str, str]] = get_all_files_urls()


config = Config()