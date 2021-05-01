import importlib
from exporter import base


def save(data: dict) -> int:
    module = importlib.import_module('exporter.' + data['name'])
    class_ = getattr(module, data['name'].title())
    exporter = class_()
    success = False

    if isinstance(exporter, base.Export):
        exporter.execute(data=data)
        success = True

    return success
