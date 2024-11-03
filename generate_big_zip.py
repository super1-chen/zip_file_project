from random import random
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED

def generate_lines():
    return ",".join([str(random()) for _ in range(10)])

def generate_file_data():
    lines = [generate_lines() for _ in range(10)]
    return "\n".join(lines)

def main(filename_zip: str, num_files = 1000):
    with ZipFile(filename_zip, "w", compression=ZIP_DEFLATED) as handle:
        for i in range(num_files):
            data = generate_file_data()
            filename = f"data-{i:04d}.csv"
            handle.writestr(filename, data)
            print(f".add {filename}")
    print("done")

if __name__ == "__main__":
    main("abc.zip", 20)