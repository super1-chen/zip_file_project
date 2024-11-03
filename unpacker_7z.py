import os
from concurrent.futures import ProcessPoolExecutor
from py7zr import SevenZipFile

def unpack(archive, filenames, path):
    # open the zip file
    with SevenZipFile(archive, "r") as handler:
        handler.extract(path=path, targets=filenames)

def extract(archive: str, out_path: str, n_worker: int = 8):
    with SevenZipFile(archive, "r") as handler:
        member_list = handler.getnames()
    n = len(member_list)
    if not n:
        return
    chunk_size = round(n / n_worker)
    with ProcessPoolExecutor(n_worker) as exec:
        for i in range(0, n, chunk_size):
            filenames = member_list[i: i+chunk_size]
            _ = exec.submit(unpack, archive, filenames, out_path)
        
if __name__ == "__main__":
    ouput_dir = "abcd_7z"
    if not os.path.exists(ouput_dir):
        os.mkdir(ouput_dir)
    extract("abcd.7z", ouput_dir, 8)