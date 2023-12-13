from cipherFinder.plugins import PluginInterface


class Init(PluginInterface):
    def execute(self, *args, **kw):
        return "dummy result"
