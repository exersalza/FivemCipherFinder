import os
import tempfile
from cipherFinder.plugins import load_plugs


def test_load_plugs():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a dummy plugin file
        plugin_file = os.path.join(tmpdir, "dummy_plugin.py")
        with open(plugin_file, "w") as f:
            f.write(
                """
                from cipherFinder.plugins import PluginInterface

                class DummyPlugin(PluginInterface):
                    def execute(self, *args, **kw):
                        return "dummy result"
                """
            )

        # Load the plugins from the temporary directory
        plugins = load_plugs(tmpdir)

        # Check that the DummyPlugin was loaded and returns the expected result
        assert "DummyPlugin" in plugins
        assert plugins["DummyPlugin"].execute() == "dummy result"