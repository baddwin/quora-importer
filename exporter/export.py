import importlib
from exporter import base


def save(name: str) -> int:
    module = importlib.import_module('exporter.' + name)
    class_ = getattr(module, name.title())
    exporter = class_()
    success = False

    if isinstance(exporter, base.Export):
        exporter.execute()
        success = True

    return success
