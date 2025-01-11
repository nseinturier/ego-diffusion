import os
from zipfile import ZipFile
from tqdm import tqdm
from src.config.core import config, ROOT
from src.utils.dl_upload_hf import upload_file_hf
from logzero import logger

OUTPUT_NAME = "flux_tiers_3_24gb_seed_0_files"
DIR_TO_ZIP = ROOT / "trained_model_files" / "model"
hf_repo_name = "sid38/images"

if __name__ == "__main__":
    output_path = ROOT / f"{OUTPUT_NAME}.zip"
    
    # Calculate total size
    total_size = sum(os.path.getsize(os.path.join(dirpath, filename))
        for dirpath, _, filenames in os.walk(DIR_TO_ZIP)
        for filename in filenames)

    with ZipFile(output_path, 'w') as zipf:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc="Creating zip") as pbar:
            for root, _, files in os.walk(DIR_TO_ZIP):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, DIR_TO_ZIP)
                    zipf.write(file_path, arcname=arcname)
                    pbar.update(os.path.getsize(file_path))

    logger.info(f"Uploading {DIR_TO_ZIP} to {hf_repo_name}")
    upload_file_hf(
        file_path=output_path,
        file_name=f"{OUTPUT_NAME}.zip",
        repo_name=hf_repo_name
    )