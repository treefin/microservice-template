"""Design patterns"""
from typing import Any
from typing import Dict


class Singleton(type):
    """Usage - inherit to make a singleton,
    see
    https://realpython.com/python-metaclasses/
    https://blog.ionelmc.ro/2015/02/09/understanding-python-metaclasses/
    https://stackoverflow.com/a/6966909/9600207
    https://stackoverflow.com/a/22404034/9600207
    https://stackoverflow.com/a/6798042/9600207
    """

    _instances: Dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):  # noqa
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
