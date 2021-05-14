import os
import time

def remove_old_files(dir_path, days, extension="*"):
    all_files = os.listdir(dir_path)
    now = time.time()
    n_days = days * 86400
    for f in all_files:
        if (extension == "*" or f.endswith(".{0}".format(extension))):
            file_path = os.path.join(dir_path, f)
            if not os.path.isfile(file_path):
                continue
            if os.stat(file_path).st_mtime < now - n_days:
                os.remove(file_path)
                print("Deleted ", f)