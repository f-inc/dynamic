import importlib.util
import os
import inspect
import sys
import logging

MODULE_EXTENSIONS = '.py'
DEFAULT_ROUTES_DIRECTORY = "/routes"
DEFAULT_HANDLER_NAME = "handler"

def get_file_routes():
    packages = [_get_package_contents(package) for package in _get_list_of_routes()]
    functions = {
        _get_route_name(package.__file__): _get_valid_module_functions(package)
        for package in packages
    }

    return functions

def has_file_based_routing():
    cwd = os.getcwd()
    path = os.path.abspath(cwd)
    path = os.path.normpath(path + DEFAULT_ROUTES_DIRECTORY)

    return os.path.exists(path)

####################
# Helper Functions #
####################

def _get_valid_module_functions(package):
    module_members = inspect.getmembers(package, inspect.isfunction)
    
    for name, func in module_members:
        if name == DEFAULT_HANDLER_NAME:
            return func
    
    file_path = package.__file__.split(DEFAULT_ROUTES_DIRECTORY)[1]
    logging.warn(f"The module at {file_path} does not have a handler function. Expected a function named '{DEFAULT_HANDLER_NAME}', did not find.")

    return None

def _get_package_contents(file_path):
    spec = importlib.util.spec_from_file_location(file_path, location=file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = module
    spec.loader.exec_module(module) 

    
    return module

def _get_route_name(file_path):
    path = file_path.split(MODULE_EXTENSIONS)[0]
    route_path = path.split(DEFAULT_ROUTES_DIRECTORY)[1]
    return route_path

def _get_list_of_routes():
    cwd = os.getcwd()
    path = os.path.abspath(cwd)
    path = os.path.normpath(path + DEFAULT_ROUTES_DIRECTORY)

    _, files = _run_fast_scandir(path, [".py"])

    files = [f for f in files if "__" not in f]

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