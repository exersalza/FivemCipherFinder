from cipherFinder.plugins import PluginInterface


class Init(PluginInterface):
    """This hook gets called when the program starts"""

    def __init__(self):
        pass

    def execute(self, *args, **kw):
        # This is a test hook
        # you can put in here theoretically everything you want.
        pass
