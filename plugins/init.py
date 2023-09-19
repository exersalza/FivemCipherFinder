from cipherFinder.plugins import PluginInterface

class Init(PluginInterface):
    def __init__(self):
        pass

    def execute(self):
        print(__name__)
