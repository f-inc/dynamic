import importlib.util
import os
import inspect

MODULE_EXTENSIONS = '.py'

def get_file_routes():
    packages = [package_contents(package) for package in _get_list_of_routes()]

    return  inspect.getmembers(packages[0].__name__)

def package_contents(file_path):
    spec = importlib.util.spec_from_file_location(file_path, location=file_path)


    return importlib.util.module_from_spec(spec)

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

    # print("Current working directory:", files)

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