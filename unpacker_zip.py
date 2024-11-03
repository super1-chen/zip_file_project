import os
from typing import List
from zipfile import ZipFile
from concurrent.futures import ProcessPoolExecutor
import logging

logger = logging.getLogger(__file__)

def unzip_files(archive, filenames, path):
    # open the zip file
    with ZipFile(archive, 'r') as handle:
        # unzip a batch of files
        handle.extractall(path=path, members=filenames)


def extract(archive: str, out_path: str, n_worker: int = 8):
    with ZipFile(archive, "r") as handle:
        namelist = handle.namelist()
    n = len(namelist)
    if not n:
        return
    chunk_size = round(n / n_worker)
    with ProcessPoolExecutor(n_worker) as exec:
        for i in range(0, n, chunk_size):
            filenames = namelist[i: i+chunk_size]
            _ = exec.submit(unzip_files, archive, filenames, out_path)
        
if __name__ == "__main__":
    if not os.path.exists("abc"):
        os.mkdir("abc")
    extract("abc.zip", "bcd", 8)