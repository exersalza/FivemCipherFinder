import os
import sys
import importlib
import inspect
import requests


REMOTE_PLUGINS = [
    "https://raw.githubusercontent.com/exersalza/"
    "FivemCipherFinder/main/plugins/sendWebhook.py",
]

VALID_HOOKS = [
    "Init",
    "GetValidatedLines",
    "GetGibberishCheckMatches",
    "GetLoggingValues",
    "GetFileContents",
    "GetRawFileContents",
    "GetLogFilename",
]


def is_valid_hook(item_name: str) -> bool:
    """Returns if item_name is in VALID_HOOKS"""
    return item_name in VALID_HOOKS


class PluginInterface:
    """Use this class to create plugins
    You have to Implment the execute method to catch stuff.

    Here comes a list of all hooks you can implement:

    # Gets called when the program starts
    Init
    # Get the lines that got validated by a file
    GetValidatedLines(list[tuple])
    # Same as above just with the Gibberishchecker
    GetGibberishCheckMatches(list[tuple[str, int, str]])
    # Get the values used for creating the log file. Gets triggered
    # for each entry in the logfile
    GetLoggingValues(
        {dir: str, ln: int, file: str,
        line: int, count: int, decoded: str, path: str}
    )
    # gets the contents printed later into a logfile
    GetFileContents(log: list)
    # the same as the one above, just not formatted
    GetRawFileContents(log: list)
    # get the name of the logfile
    GetLogFilename(filename: str)

    """

    hook_name = ""

    def __init__(self) -> None:
        if not self.hook_name:
            self.hook_name = self.__class__.__name__

    def execute(self, *args, **kw):
        raise NotImplementedError("Plugins must implement an 'execute' method")


class _PluginDummy(PluginInterface):
    """PluginDummy, this class is for the case that you dont have hooks
    implemented or you wrote a hook wrong.

    You can just copy paste it and write your code into the execute function
    """

    def execute(self, *args, **kw):
        # Enter code here, I mean not here here, but should you copy
        # it and add it to your own plugin :D
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

    if not os.path.exists(plug_dir) and not os.path.isdir(plug_dir):
        print("Given path is not a Directory or does not exist.")
        return {"error": 1}

    sys.path.append(os.path.abspath(plug_dir))

    _hooks = {}

    for f in os.listdir(plug_dir):
        if not f.endswith(".py"):
            continue

        module = importlib.import_module(f[:-3], package=plug_dir)
        for item_name in dir(module):
            item = getattr(module, item_name)

            if item_name == PluginInterface.__name__ or not inspect.isclass(
                item
            ):
                continue

            hook_name = item.hook_name if item.hook_name else item.__name__

            if isinstance(item, type) and is_valid_hook(hook_name):
                _hooks[hook_name] = item()

    return _hooks


def get_remote_plugins() -> int:
    """Get the prebuild plugins from github so the user just has
    to configure them

    Returns
    -------
    int :
        Status code

    """
    DIR = "./_plugins"

    if not os.path.exists(DIR):
        os.mkdir(DIR)

    for plug in REMOTE_PLUGINS:
        plug_name = plug[plug.rfind("/"):]

        with open(f"{DIR}{plug_name}", "wb") as _file:
            for chunk in requests.get(
                plug, stream=True, timeout=5
            ).iter_content(chunk_size=8192):
                if not chunk:
                    continue

                _file.write(chunk)

    print(
        "Configure your new gained Plugins inside the files itself.\n"
        "After you configured your plugins, run them with "
        f"`find-cipher --plug-dir `{DIR}`"
    )
    return 0


if __name__ == "__main__":
    print(load_plugs("../plugins"))
