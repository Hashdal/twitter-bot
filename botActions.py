from logging import raiseExceptions
import twitter
import json
import accessDB
from time import sleep

class MainActions:
    __api = None
    __db = None
    __delays = None
    __numberOfTweets = None
    def __init__(self, configFile: str) -> None:
        botInfo = json.loads(open(configFile, 'r').read())
        self.__api = twitter.Api(
            consumer_key=botInfo["consumer_key"],
            consumer_secret=botInfo["consumer_secret"],
            access_token_key=botInfo["access_tooken"],
            access_token_secret=botInfo["access_tooken_secret"],
        )
        self.__db = accessDB.Database(configFile=configFile)
        self.__delays = int(botInfo["delay_seconds"])
        self.__numberOfTweets = int(botInfo["number_of_tweets"])
    
    def random_from_db(self) -> None:
        self.__api.PostUpdate(self.__db.read_random_data_from_table())

    def send_tweet(self, tweet:str = None) -> None:
        if tweet == None:
            tweet = input('enter your tweet: ')
        self.__api.PostUpdate(tweet)

    def send_tweet_in_timespans(self) -> None:
        for i in range(self.__numberOfTweets):
            try:
                self.random_from_db()
                print("tweet {} sent".format(i+1))
            except:
                print("failed to send tweet")
            sleep(self.__delays)



a = input('1. send tweet, 2. send random tweet from database, 3. send random tweets in timespans: ')
m = MainActions('./config.json')
if a == '1':
    m.send_tweet()
elif a == '2':
    m.random_from_db()
else:
    m.send_tweet_in_timespans()
