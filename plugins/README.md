# How to do Plugins

It's fairly simple, you can copy the contents of ./sendWebhook.py and yeet everything except the basic class structure
or you copy the following lines to trigger something when the cipherfinder starts
```py
from cipherFinder.plugins import PluginInterface

# Keep in mind to name the class like the hook you want to get
# should you have a typo or something, it wont trigger.
class Init(PluginInterface):
    # you can add every method you want, but this one should
    # be implemented, otherwise you'll get an 'NotImplementedError'
    def execute(self, *args, **kwargs) -> int:
        print("WEE WOO")
        return 0
```
or when you feel fancy, you can also name the class whatever you want and add an class variable named '__name__' and give it the 
hook name


## Hooks

So basically there are currently these hooks you can implement

```py
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
```
