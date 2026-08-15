"""Load the frozen digit-prefixed pipeline scripts as modules.

`import 03_analyze` is not legal Python, and the scripts themselves must not
be renamed (they are the documented, frozen reproduction surface for the
paper's numbers), so they are loaded by file path exactly once here.
"""
import importlib.util
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent


def load_script(module_name: str, filename: str):
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, _ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
