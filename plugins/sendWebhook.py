import json
import requests

from cipherFinder.plugins import PluginInterface


# The file gets completely inserted, so dont overwrite glabals
# global variabls in the finder.py file
WEBHOOL_URL = ""  # Enter webhook here
ALERT_ROLE_ID = ""  # Enter member to ping, Optional
WEBHOOK_HEADERS = {"Content-Type": "application/json"}


def prepare_webhook_content(count: int, failed: int) -> dict:
    content = None

    if ALERT_ROLE_ID:
        content = f"<@&{ALERT_ROLE_ID}>"

    webhook_content = {
        "content": content,
        "embeds": [
            {
                "title": "Cipherfinder results",
                "color": 5814783,
                "image": {
                    "url": "https://media.giphy.com/media/"
                    "3oKIPlLZEbEbacWqOc/giphy.gif"
                },
                "fields": [
                    {
                        "name": "Detectet Ciphers (False positivs ... maybe)",
                        "value": count,
                    },
                    {
                        "name": "Files that could not be scanned",
                        "value": failed,
                    },
                ],
            }
        ],
        "attachments": [],
    }

    return webhook_content


class Init(PluginInterface):
    def execute(self, *args, **kw):
        pass


# You might ask yourself now, where tf does this name come from?
# good question, the name of classes are used to create the hooks
# that means, when you name your class Init, it will be called
# when the programs inits itself, or when you start it.
# Also when you're creating your own plugins, keep in mind
# to inherit the 'PluginInterface' class, otherwise it wont start.
class FetchMeTheirSouls(PluginInterface):
    # Create an attribute like this, to change the hook name
    # it will always default to the classes name, so you don't have
    # to define this.
    hook_name = "GetRawFileContents"

    # The following function is REQUIRED, it will be run by the
    # hook trigger
    def execute(self, *args, **kw):
        if not WEBHOOL_URL:
            print(
                f"PLEASE ENTER A WEBHOOK URL INTO YOUR PLUGIN "
                f"{self.__class__.__name__:!r}"
            )

        values = args[0]  # just isolate the values from the args
        failed = kw.pop("failed")  # failed files to open
        webhook_content = prepare_webhook_content(values[0]["count"], failed)

        requests.post(
            WEBHOOL_URL,
            data=json.dumps(webhook_content),
            headers=WEBHOOK_HEADERS,
            timeout=30,
        )
