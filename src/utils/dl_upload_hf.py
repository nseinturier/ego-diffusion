from huggingface_hub import HfApi
from pathlib import Path
from src.config.core import config, ROOT
from src.in_out.download import download_file

# Change top variables to upload different files
REPO_NAME = "sid38/loras"
FILE_URL = "https://civitai.com/api/download/models/815353?type=Model&format=SafeTensor"
FILE_NAME = "ana-taylor-joy-lora.safetensors"

### Do not change below code

OUTPUT_FOLDER = ROOT / "tmp"
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
FILE_OUTPUT_PATH = OUTPUT_FOLDER / FILE_NAME

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

def run():
    download_file(FILE_URL, FILE_NAME, output_path=OUTPUT_FOLDER)
    upload_file_hf(FILE_OUTPUT_PATH, FILE_NAME, REPO_NAME)


if __name__ == "__main__":
    run()