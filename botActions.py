import twitter
import json

class MainActions:
    def __init__(self, configFile: str):
        botInfo = json.loads(open(configFile, 'r').read())
        self.api = twitter.Api(
            consumer_key=botInfo["consumer_key"],
            consumer_secret=botInfo["consumer_secret"],
            access_token_key=botInfo["access_tooken"],
            access_token_secret=botInfo["access_tooken_secret"],
        )