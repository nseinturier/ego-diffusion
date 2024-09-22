from pathlib import Path
import requests
from tqdm import tqdm
from src.config.core import config

def download_file(
        url: str,
        file_name: str,
        file_type: str = None,
        output_path: Path = None
)-> None:
    if output_path is None:
        output_path = config.download_outputs_path[file_type]
    output_path = (output_path / file_name).__str__()

    headers = {}
    if get_url_source(url) == "huggingface":
        headers["Authorization"] = f"Bearer {config.hf_token}"
    elif get_url_source(url) == "civitai":
        headers["Authorization"] = f"Bearer {config.civitai_token}"

    response = requests.get(url, headers=headers, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(output_path, 'wb') as file, tqdm(
        desc=output_path,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)


#### UTILS ####

def get_url_source(url: str) -> str:
    if "huggingface" in url:
        return "huggingface"
    elif "civitai" in url:
        return "civitai"
    else:
        raise ValueError(f"Invalid URL source: {url}")
    
def get_file_name(url: str) -> str:
    return Path(url).name
    
