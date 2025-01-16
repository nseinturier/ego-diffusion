from src.in_out.download import download_file
from src.config.core import config
from logzero import logger

MODELS_TO_DOWNLOAD = [
    "flux1-dev.safetensors",
    "t5xxl_fp16.safetensors",
    "clip_l.safetensors",
    "ae.safetensors"
]

def main():
    download_info = {
        **config.downloads_info.checkpoint,
        **config.downloads_info.clip,
        **config.downloads_info.vae,
        **config.downloads_info.unet
    }
    downloads_dict = {k: v for k,v in download_info.items() if k in MODELS_TO_DOWNLOAD}
    output_path = config.download_outputs_path["checkpoint"]

    for file_name, dl_config in downloads_dict.items():
        file_path = output_path / file_name

        if file_path.exists():
            logger.info(f"File {file_name} already exists, skipping download...")
            continue
        
        logger.info(f"Downloading {file_name}...")
        download_file(
            url = dl_config.url, 
            file_name = file_name,
            output_path = output_path
        )

if __name__ == "__main__":
    main()