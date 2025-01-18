import src
from pathlib import Path
import yaml
from pydantic import BaseModel
from typing import Any
import os


# Constants
PACKAGE_ROOT = Path(src.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
MODELS_DOWNLOAD_CONFIG = PACKAGE_ROOT / 'config' / 'models_config.yaml'

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
    "kohya": {
        download_type: ROOT / "kohya_ss" / "models"
        for download_type in ["checkpoint", "vae", "lora", "clip", "controlnet", "unet"]
    },
}

def load_yaml_config(file_path: Path) -> dict[str, Any]:
    """Load YAML configuration file."""
    with file_path.open("r") as file:
        return yaml.safe_load(file)

class DownloadConfig(BaseModel):
    enabled: bool
    url: str

class ModelConfig(BaseModel):
    checkpoint: dict[str, DownloadConfig]
    lora: dict[str, DownloadConfig]
    vae: dict[str, DownloadConfig]
    controlnet: dict[str, DownloadConfig]
    clip: dict[str, DownloadConfig]
    unet: dict[str, DownloadConfig]


class Config(BaseModel):
    mod_env: str = os.environ["MOD_ENV"]
    hf_token: str = os.environ.get("HF_TOKEN")
    civitai_token: str = os.environ.get("CIVITAI_TOKEN")
    custom_nodes_folder: Path = ROOT / "ComfyUI" / "custom_nodes"
    download_outputs_path: dict[str, Path] = PATH_CONFIG[mod_env]
    downloads_info: ModelConfig


config = Config(
    downloads_info=ModelConfig(**load_yaml_config(MODELS_DOWNLOAD_CONFIG))
)