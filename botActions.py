import twitter
import json
import accessDB

class MainActions:
    api = None
    db = None
    def __init__(self, configFile: str):
        botInfo = json.loads(open(configFile, 'r').read())
        self.api = twitter.Api(
            consumer_key=botInfo["consumer_key"],
            consumer_secret=botInfo["consumer_secret"],
            access_token_key=botInfo["access_tooken"],
            access_token_secret=botInfo["access_tooken_secret"],
        )
        self.db = accessDB.Database(configFile=configFile)
    
    def random_from_db(self):
        self.api.PostUpdate(self.db.read_random_data_from_table())

    def send_tweet(self):
        self.api.PostUpdate(input("enter your tweet "))


a = input('1. send tweet, 2. send random tweet from database ')
m = MainActions('./config.json')
if a == '1':
    m.send_tweet()
else: 
    m.random_from_db()
