import src
from pathlib import Path
import yaml
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Literal
import warnings

# Constants
PACKAGE_ROOT = Path(src.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
ENV_YAML = PACKAGE_ROOT / 'env.yaml'
TO_DOWNLOAD_YAML = PACKAGE_ROOT / 'to_download.yaml'
FILES_DOWNLOAD_PATH = PACKAGE_ROOT / 'config' / 'download_paths.yaml'

# Define the path structure for different environments
PATH_CONFIG = {
    "comfyUI": {
        "checkpoints": ROOT / "ComfyUI" / "models" / "checkpoints",
        "vae": ROOT / "ComfyUI" / "models" / "vae",
        "lora": ROOT / "ComfyUI" / "models" / "lora",
    },
    "kohya_ss": {
        "checkpoints": ROOT / "kohya_ss" / "models",
        "vae": ROOT / "kohya_ss" / "models" / "vae",
        # Note: 'lora' is not defined for kohya_ss
    },
}

def find_env_config_file() -> Path:
    """Locate the configuration file."""
    if ENV_YAML.is_file():
        return ENV_YAML
    raise FileNotFoundError(f"Environment config not found at {ENV_YAML!r}")

def load_yaml_config(file_path: Path = None) -> Dict[str, Any]:
    """Load YAML configuration file."""
    file_path = file_path or find_env_config_file()
    with file_path.open("r") as file:
        return yaml.safe_load(file)

ENV_CONFIG = load_yaml_config()
TO_DOWNLOAD_CONFIG = load_yaml_config(TO_DOWNLOAD_YAML)

def get_files_paths_to_download(
        download_type: Literal['checkpoints', 'loras']
)-> dict[str, str]:
    if TO_DOWNLOAD_CONFIG[download_type] is None:
        return {}
    download_paths = load_yaml_config(FILES_DOWNLOAD_PATH)
    return {k: v for k, v in download_paths[download_type].items() if k in TO_DOWNLOAD_CONFIG[download_type]}


class Config(BaseModel):
    mod_env: str = ENV_CONFIG["MOD_ENV"]
    hf_token: str = ENV_CONFIG["HF_TOKEN"]
    checkpoints_download_paths: dict[str, str] = get_files_paths_to_download("checkpoints")
    loras_download_paths: dict[str, str] = get_files_paths_to_download("loras")
    vae_download_paths: dict[str, str] = get_files_paths_to_download("vae")
    controlnet_download_paths: dict[str, str] = get_files_paths_to_download("controlnet")

    def get_path(self, path_type: str) -> Optional[Path]:
        """
        Dynamically get the path based on the storage mode and path type.
        
        :param path_type: Type of path to retrieve (e.g., 'checkpoints', 'vae', 'lora')
        :return: Path object for the requested path type, or None if not defined
        """
        try:
            path = PATH_CONFIG[self.mod_env].get(path_type)
            if path is None:
                warnings.warn(f"Warning: No {path_type} path associated with {self.mod_env}")
            return path
        except KeyError:
            warnings.warn(f"Warning: Undefined environment: {self.mod_env}")
            return None

    @property
    def checkpoints_path(self) -> Optional[Path]:
        return self.get_path('checkpoints')

    @property
    def vae_path(self) -> Optional[Path]:
        return self.get_path('vae')

    @property
    def lora_path(self) -> Optional[Path]:
        return self.get_path('lora')

    @property
    def controlnet_path(self) -> Optional[Path]:
        return self.get_path('controlnet')

config = Config()


