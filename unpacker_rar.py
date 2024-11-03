import os
from typing import List
from concurrent.futures import ProcessPoolExecutor
import logging

# dirname = os.path.dirname(__file__)
# os.environ.setdefault('UNRAR_LIB_PATH', os.path.join(dirname, "unrar"))
# logger = logging.getLogger(__file__)
from unrar import rarfile

def unzip_files(archive, filenames, path):
    with rarfile.RarFile(archive, 'r') as handle:
        handle.extractall(path=path, members=filenames)


def extract(archive: str, out_path: str, n_worker: int = 8):
    with rarfile.RarFile(archive, "r") as handle:
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
    dirname = os.path.dirname(__file__)
    if not os.path.exists("abcd"):
        os.mkdir("abcd")
    extract("bcd.rar", "abcd")