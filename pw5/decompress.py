import os
import tarfile
import zipfile


def extract_all(filename, output_dir=None):
    if output_dir is None:
        output_dir = os.getcwd()

    os.makedirs(output_dir, exist_ok=True)

    if zipfile.is_zipfile(filename):
        with zipfile.ZipFile(filename, "r") as zipf:
            zipf.extractall(output_dir)
    elif tarfile.is_tarfile(filename):
        with tarfile.open(filename, "r:*") as tar:
            tar.extractall(output_dir)
    else:
        raise ValueError(f"Unknown compressed file format: {filename}")
