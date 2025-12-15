import os
import tarfile
import zipfile

from domains.database import AutoSave


def zip_method(name: str = "students.dat"):
    base_dir = os.getcwd()
    real_base = os.path.realpath(base_dir)

    with zipfile.ZipFile(
        name, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as zipf:
        for path in AutoSave.list_paths():
            full_path = (
                os.path.join(base_dir, path) if not os.path.isabs(path) else path
            )

            if not os.path.isfile(full_path):
                continue

            real_file = os.path.realpath(full_path)

            if not real_file.startswith(real_base):
                continue

            arcname = os.path.relpath(real_file, real_base)
            zipf.write(real_file, arcname)


@staticmethod
def tar_gz_method(name: str = "students.dat"):
    base_dir = os.getcwd()
    real_base = os.path.realpath(base_dir)

    with tarfile.open(name, "w:gz", compresslevel=9) as tar:
        for path in AutoSave.list_paths():
            full_path = (
                os.path.join(base_dir, path) if not os.path.isabs(path) else path
            )

            if not os.path.isfile(full_path):
                continue

            real_file = os.path.realpath(full_path)

            if not real_file.startswith(real_base):
                continue

            arcname = os.path.relpath(real_file, real_base)
            tar.add(real_file, arcname=arcname)
