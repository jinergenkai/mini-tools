import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Configuration
BASE_URL = "https://dn710704.ca.archive.org/0/items/englishpod_all/englishpod_{:04d}pb.mp3"
START_NUM = 1
END_NUM = 365
MAX_WORKERS = 10  # Download 10 files at a time
DOWNLOAD_DIR = "downloads"

def download_file(file_num):
    """Download a single MP3 file"""
    url = BASE_URL.format(file_num)
    filename = f"englishpod_{file_num:04d}pb.mp3"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    # Skip if already downloaded
    if os.path.exists(filepath):
        return f"✓ Skipped {filename} (already exists)"

    try:
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()

        # Save file
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
        return f"✓ Downloaded {filename} ({file_size:.2f} MB)"

    except Exception as e:
        return f"✗ Failed {filename}: {str(e)}"

def main():
    # Create download directory
    Path(DOWNLOAD_DIR).mkdir(exist_ok=True)

    print(f"Starting download of {END_NUM - START_NUM + 1} files...")
    print(f"Downloading {MAX_WORKERS} files at a time")
    print(f"Saving to: {DOWNLOAD_DIR}/\n")

    # Download files concurrently
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(download_file, num): num for num in range(START_NUM, END_NUM + 1)}

        completed = 0
        total = len(futures)

        for future in as_completed(futures):
            result = future.result()
            completed += 1
            print(f"[{completed}/{total}] {result}")

    print(f"\n✓ Download complete! Files saved to '{DOWNLOAD_DIR}/' folder")

if __name__ == "__main__":
    main()
