from src.in_out.download import download_file

FILE_URL = "https://civitai.com/api/download/models/815353?type=Model&format=SafeTensor"
FILE_NAME = "atl2.safetensors"
FILE_TYPE = "lora"

def run():
    download_file(FILE_URL, FILE_NAME, FILE_TYPE)

if __name__ == "__main__":
    run()