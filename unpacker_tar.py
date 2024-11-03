import os
import tarfile
from tarfile import TarFile
from concurrent.futures import ProcessPoolExecutor

def unpack(archive, filenames, path, mode):
    # open the zip file
    tar = tarfile.open(archive, mode)
    tar.extractall(path=path, members=filenames)
    tar.close()

def extract(archive: str, out_path: str, n_worker: int = 8):
    mode = "r:gz" if archive.endswith("tar.gz") else "r"
    tar = tarfile.open(archive, mode)
    member_list = tar.getmembers()
    tar.close()
    n = len(member_list)
    if not n:
        return;
    chunk_size = round(n / n_worker)
    with ProcessPoolExecutor(n_worker) as exec:
        for i in range(0, n, chunk_size):
            filenames = member_list[i: i+chunk_size]
            _ = exec.submit(unpack, archive, filenames, out_path)
        
if __name__ == "__main__":
    ouput_dir = "abcd"
    if not os.path.exists(ouput_dir):
        os.mkdir(ouput_dir)
    extract("bcd.tar", ouput_dir, 8)
    extract("bcd.tar.gz", ouput_dir, 8)