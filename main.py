import importlib.util
import os
import logging

from fastapi import FastAPI
from utils.directory import directory


def get_error_log(error):
    exc_arg_list = [str(x) for x in error.args]
    if not exc_arg_list:
        error_log = error.__class__.__name__
    else:
        error_log = error.__class__.__name__ + ": " + ", ".join(exc_arg_list)
    return error_log


app = FastAPI()
log = logging.getLogger(__name__)


views = [
    "routers." + file[:-3] for file in os.listdir(
        os.path.join(directory, "routers")
    ) if file.endswith(".py")
]
for view in views:
    spec = importlib.util.find_spec(view)
    if spec is None:
        log.error("Extension Not Found: {0}".format(view))
        continue

    lib = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(lib)  # type: ignore
    except Exception as e:
        error_log = get_error_log(e)
        log.error("Extension Failed: {0} ({1})".format(view, error_log))
        continue

    try:
        setup = getattr(lib, 'setup')
    except AttributeError:
        log.error("No Entry Point Error: {0}".format(view))
        continue

    try:
        setup(app)
    except Exception as e:
        error_log = get_error_log(e)
        log.error("Extension Failed: {0} ({1})".format(view, error_log))
        raise e
