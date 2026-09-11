import shutil
import os


def move_file(file_path, destination_folder):

    os.makedirs(destination_folder, exist_ok=True)

    file_name = os.path.basename(file_path)

    destination_path = os.path.join(
        destination_folder,
        file_name
    )

    shutil.move(
        file_path,
        destination_path
    )

    return destination_path