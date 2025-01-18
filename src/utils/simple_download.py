from src.transfer.download import download_list_of_files
from src.transfer.download_utils import get_headers
from src.config.core import ROOT

import asyncio

FILE_URL = "https://huggingface.co/lkeab/hq-sam/resolve/main/sam_hq_vit_h.pth"
OUTPUT_PATH = ROOT / "ComfyUI" / "models/sam" / "sam_hq_vit_h.pth"

def run():
    download_list = [{
        "url": FILE_URL,
        "output_path": OUTPUT_PATH.__str__(),
        "header": get_headers(FILE_URL)
    }]
    asyncio.run(download_list_of_files(download_list))

if __name__ == "__main__":
    run()