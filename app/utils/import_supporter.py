import importlib.util
import logging
import os

from fastapi import FastAPI


class ImportSupporter:
    def __init__(self, app: FastAPI, logger_name: str = "app.utils.import_supporter"):
        self.app = app
        self.logger = logging.getLogger(logger_name)

    def load_routers(self, package: str, base_dir: str):
        package_path = os.path.join(base_dir, *package.split("."))
        files = [
            f for f in os.listdir(package_path)
            if f.endswith(".py") and not f.startswith("_")
        ]
        for file in files:
            self._include_router(package + "." + file[:-3])

    def _include_router(self, module_name: str):
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            self.logger.error(f"Module not found: {module_name}")
            return

        lib = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(lib)
        except Exception as e:
            self.logger.error(f"Failed to load {module_name}: {e}")
            return

        if not hasattr(lib, "router"):
            self.logger.warning(f"No 'router' attribute in {module_name}, skipping")
            return

        self.app.include_router(lib.router)
        self.logger.info(f"Loaded router from {module_name}")
