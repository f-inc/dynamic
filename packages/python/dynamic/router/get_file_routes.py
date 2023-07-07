import importlib.util
import os
import inspect
import sys
import logging

from dynamic import dynamic
from dynamic.router import Route

MODULE_EXTENSIONS = '.py'
DEFAULT_ROUTES_DIRECTORY = "/routes"
DEFAULT_HANDLER_NAME = "handler"

class FileRoutesBuilder:
    def __init__(self, routes_dir: str = DEFAULT_ROUTES_DIRECTORY):
        self.routes = []
        self._dir_path = self._get_route_dir_path(routes_dir)

    def get_file_routes(self):
        packages = [_get_package_contents(package) for package in self._get_list_of_routes()]
        handlers = {
            _get_route_name(package.__file__): _get_valid_module_functions(package)
            for package in packages
        }
        routes = []

        for path, handle in handlers.items():
            if handle:
                route = Route(path=path, handle=handle, streaming=False)
                routes.append(route)

        logging.info(f"Grabbing {len(routes)} file-based routes...")

        return routes

    def has_file_based_routing(self):
        return os.path.exists(self._dir_path)

    def _get_route_dir_path(self, routes_dir):
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        path = os.path.normpath(path + routes_dir)

        return path
    
    def _get_list_of_routes(self):
        _, files = _run_fast_scandir(self._dir_path)

        files = [f for f in files if "__" not in f]

        return files

####################
# Helper Functions #
####################

def _get_valid_module_functions(package):
    module_members = inspect.getmembers(package, inspect.isfunction)
    
    for name, func in module_members:
        if hasattr(func, "__wrapped__"):
            logging.info(f"{name} - {func} is wrapped {func.methods}")
            # logging.info(dynamic == func.__wrapped__.__name__)
        if name == DEFAULT_HANDLER_NAME:
            return func
    
    file_path = package.__file__.split(DEFAULT_ROUTES_DIRECTORY)[1]
    logging.warn(f"The module at {file_path} does not have a handler function. Expected a function named '{DEFAULT_HANDLER_NAME}', did not find.")

    return None

def _get_package_contents(file_path):
    """Import functions and other modules within a file"""
    spec = importlib.util.spec_from_file_location(file_path, location=file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["module.name"] = module
    spec.loader.exec_module(module) 

    
    return module

def _get_route_name(file_path):
    """Given a file path, return a valid endpoint

    Example: routes/foo/bar.py --> foo/bar
    """
    path = file_path.split(MODULE_EXTENSIONS)[0]
    route_path = path.split(DEFAULT_ROUTES_DIRECTORY)[1]
    return route_path


def _run_fast_scandir(dir, ext=[MODULE_EXTENSIONS]):
    """Recurseively find all files in a directory, while also given desired file extension."""
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

