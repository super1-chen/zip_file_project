import sys
import os
import argparse
import multiprocessing
import time

import unpacker_7z
import unpacker_rar
import unpacker_zip
import unpacker_tar

FUNC_MAPS = {
    ".7z": unpacker_7z,
    ".rar": unpacker_rar,
    ".tar.gz": unpacker_tar,
    ".tar": unpacker_tar,
    ".zip": unpacker_zip
}

def main(opt_args):
    filename = opt_args.filename
    output = opt_args.output or os.path.join(os.getcwd(), "output")
    workers = opt_args.workers or multiprocessing.cpu_count()
    _, ext = os.path.splitext(filename)
    start_time = time.time()
    print(f"开始解压文件: {filename}")
    FUNC_MAPS[ext].extract(filename, output, workers)
    print(f"--- 共消耗时间：{time.time() - start_time:0.3f} seconds ---")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog=sys.argv[0],
                    description='高性能解压工具',
                    epilog='解压工具，支持7z, tar, zip, rar 四种格式的压缩包')
    parser.add_argument('filename', help="需要解压的文件")           # positional argument
    parser.add_argument('-w', '--workers', required=False, type=int, help="进程数")      # option that takes a value
    parser.add_argument('-o', '--output', required=False, help="输出文件夹")  # on/off flag
    opt_args = parser.parse_args()
    main(opt_args)