import shutil
import os

def cleanup_dir(directory) -> None:
    if os.path.exists(directory) and os.path.isdir(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        print(f"All contents of the directory '{directory}' have been removed.")
    else:
        print(f"Directory '{directory}' does not exist or is not a directory.")
