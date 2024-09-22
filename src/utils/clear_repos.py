import os
import shutil
import sys
from logzero import logger
from pathlib import Path
from src.config.core import config


def run():
    for folder_name, folder_path in config.download_outputs_path.items():
        logger.warning(f"Deleting contents of {folder_name}")
        delete_folder_contents(folder_path)


def delete_folder_contents(folder_path: Path):
    for item in folder_path.rglob('*'):
        if item.is_file():
            item.unlink()

        elif item.is_dir():
            shutil.rmtree(item)

        logger.warning(f"Deleted {item}")

if __name__ == "__main__":
    run()

