import os
import sys
import importlib


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

    def execute(self, *args, **kw):
        raise NotImplementedError("Plugins must implement an 'execute' method")


class _PluginDummy(PluginInterface):
    """PluginDummy, this class is for the case that you dont have hooks
    implemented or you wrote a hook wrong.

    You can just copy paste it and write your code into the execute function
    """

    def execute(self, *args, **kw):
        # Enter code here, I mean not here here, but should you copy it
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
    
    # add the Plugins path so we can import it
    sys.path.append(os.path.abspath(plug_dir))

    _hooks = {}

    for f in os.listdir(plug_dir):
        if not f.endswith(".py"):
            continue

        module = importlib.import_module(f[:-3], package=plug_dir)
        for item_name in dir(module):
            item = getattr(module, item_name)

            # Make sure we dont add the PluginInterface to the hook list
            if getattr(module, item_name) == PluginInterface:
                continue
            
            # Check if the Hook is inhereting the PluginInterface class
            if isinstance(item, type) and issubclass(item, PluginInterface):
                _hooks[item.__name__] = item()

    return _hooks
