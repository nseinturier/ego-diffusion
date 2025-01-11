from zipfile import ZipFile
from src.config.core import config, ROOT
from src.utils.dl_upload_hf import upload_file_hf
from logzero import logger

# change the following to upload
zip_name = "test.zip"

sample_images_folder = ROOT / "trained_model_files" / "model/sample"
hf_repo_name = "sid38/images"

png_files = list(sample_images_folder.glob('*.png'))
output_dir = ROOT / "sample_images"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / zip_name

with ZipFile(output_path, 'w') as zip_obj:
    # Add each PNG file to the zip
    for png_file in png_files:
        # Add file with its basename (filename without path)
        zip_obj.write(png_file, png_file.name)

logger.info(f"Uploading {output_path} to {hf_repo_name}")
upload_file_hf(
    file_path=output_path,
    file_name=zip_name,
    repo_name=hf_repo_name
)