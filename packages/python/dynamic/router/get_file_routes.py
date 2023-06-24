import os

def get_file_routes():
    pass

def is_file_based_routing():
    cwd = os.getcwd()
    path = os.path.abspath(cwd)
    path = os.path.normpath(path + '/routes')

    return os.path.exists(path)

def _get_list_of_routes():
    cwd = os.getcwd()
    path = os.path.abspath(cwd)
    path = os.path.normpath(path + '/routes')

    _, files = _run_fast_scandir(path, [".py"])

    print("Current working directory:", files)

    return files

def _run_fast_scandir(dir, ext):    # dir: str, ext: list
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)


    for dir in list(subfolders):
        sf, f = _run_fast_scandir(dir, ext)
        subfolders.extend(sf)
        files.extend(f)
    return subfolders, files