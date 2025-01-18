from huggingface_hub import HfApi
from pathlib import Path
from src.config.core import config, ROOT

def upload_file_hf(
        file_path: Path, 
        file_name: str, 
        repo_name: str
)-> None:
    api = HfApi()

    api.upload_file(
        path_or_fileobj = file_path,
        path_in_repo = file_name,
        repo_id = repo_name,
        token = config.hf_token,
        repo_type = "model"
    )