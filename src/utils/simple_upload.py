from src.utils.dl_upload_hf import upload_file_hf
from src.config.core import config, ROOT
from logzero import logger

# Change top variables to upload different files
MODEL_NAME = "my_model.safetensors"

HF_REPO_NAME = "sid38/fine_tuned_models"
TRAINED_MODEL_PATH = ROOT / "trained_model_files" / "model"

if __name__ == "__main__":
    file_path = TRAINED_MODEL_PATH / MODEL_NAME
    logger.info(f"uploading {file_path} to {HF_REPO_NAME} Hugginface repo")
    
    upload_file_hf(
        file_path=file_path,
        file_name=MODEL_NAME,
        repo_name=HF_REPO_NAME
    )