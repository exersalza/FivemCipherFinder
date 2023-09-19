import os
import sys
import importlib


class PluginInterface:
    """Use this class to create plugins
    You have to Implment the execute method to catch stuff.

    Here comes a list of all hooks you can implement:

    Init
    GetValidatedLines(list[tuple])
    GetGibberishCheckMatches(list[tuple[str, int, str]])
    GetLoggingValues(
        {dir: str, ln: int, file: str, count: int, decoded: str}
    )
    GetLogFilename(filename: str)

    """

    def execute(self, *args, **kw):
        raise NotImplementedError("Plugins must implement an 'execute' method")


class _PluginDummy(PluginInterface):
    def execute(self, *args, **kw):
        # Enter code here
        ...


def load_plugs(plug_dir: str = ".") -> dict:
    """Load plugs (plugins) from a folder to create
    some hooks or get data

    Parameters
    ----------
    plug_dir : str : default "."
        Define the pluging directory.

    Returns
    -------
    list :
        The list of loaded plugins
    """

    sys.path.append(os.path.abspath(plug_dir))

    _hooks = {}

    for f in os.listdir(plug_dir):
        if not f.endswith(".py"):
            continue

        module = importlib.import_module(f[:-3], package=plug_dir)
        for item_name in dir(module):
            item = getattr(module, item_name)

            if (item := getattr(module, item_name)) == PluginInterface:
                continue

            if isinstance(item, type) and issubclass(item, PluginInterface):
                _hooks[item.__name__] = item()

    return _hooks
