import json
import requests

from cipherFinder.plugins import PluginInterface


# The file gets completely executed, so be aware to not overwrite
# global variabls in the finder.py file
ALERT_ROLE_ID = ""  # Enter member to ping, can be left empty
WEBHOOK_HEADERS = {"Content-Type": "application/json"}
WEBHOOL_URL = ""  # Enter webhook here


def prepare_webhook_content(count: int, failed: int) -> dict:
    content = None

    if role_id := ALERT_ROLE_ID:
        content = f"<@&{role_id}>"

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


# You might ask yourself now, where tf does this name come from?
# good question, the name of classes are used to create the hooks
# that means, when you name your class Init, it will be called
# when the programs inits self, or when you start it.
# Also when you're creating your own plugins, keep in mind
# to inherit the 'PluginInterface' class, otherwise it wont start.
class GetRawFileContents(PluginInterface):
    # The following function is REQUIRED, it will be run by the
    # hook trigger
    def execute(self, *args, **kw):
        values = args[0]  # just isolate the values from the args
        failed = kw.pop("failed")  # failed files to open
        webhook_content = prepare_webhook_content(values[0]["count"], failed)

        requests.post(
            WEBHOOL_URL,
            data=json.dumps(webhook_content),
            headers=WEBHOOK_HEADERS,
            timeout=30,
        )
