import asyncio
import aiohttp
from logzero import logger
from tqdm.asyncio import tqdm
from src.config.core import config


async def download_list_of_files(
        download_list: list[dict[str, str]]
)->None:
    timeout = aiohttp.ClientTimeout(total=3600) # 1 hour timeout
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Create overall progress bar
        total_progress = tqdm(
            total=0,  # Will be updated as we download
            unit='B',
            unit_scale=True,
            desc="Total Progress",
            position=0,
            leave=True
        )

        # Run downloads concurrently
        await asyncio.gather(*[
            download_file(item['url'], item['output_path'], session, item["headers"], total_progress) 
            for item in download_list
        ])
        
        total_progress.close()

async def download_file(
        url: str, 
        output_path: str, 
        session: aiohttp.ClientSession,
        headers: dict[str, str],
        total_progress: tqdm
) -> None:
    async with session.get(url, headers=headers) as response:
        file_size = int(response.headers.get('content-length', 0))
        desc = f"Downloading {output_path}"
        
        with open(output_path, 'wb') as f:
            with tqdm(total=file_size, unit='B', unit_scale=True, 
                     desc=desc, leave=True) as file_progress:
                while True:
                    chunk = await response.content.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    chunk_size = len(chunk)
                    file_progress.update(chunk_size)
                    total_progress.update(chunk_size)