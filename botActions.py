import twitter
import json
import accessDB
from time import sleep
import random

class MainActions:
    __api = None
    __db = None
    __delays = None
    __numberOfTweets = None
    mode = None
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
        self.mode = int(botInfo["mode"])
    
    def random_from_db(self, id = None) -> None:
        tweet = str(self.__db.pop_random_data_from_table(id))
        print(tweet)
        self.__api.PostUpdate(tweet)

    def send_tweet(self, tweet:str = None) -> None:
        if tweet == None:
            tweet = input('enter your tweet: ')
        self.__api.PostUpdate(tweet)

    def send_tweet_in_timespans(self) -> None:
        for i in range(self.__db.get_table_rows()):
            try:
                randomList = random.sample(range(1, self.__db.get_table_rows() + 1), self.__db.get_table_rows())
                self.random_from_db(randomList.pop())
                print("tweet {} sent".format(i+1))
            except:
                print("failed to send tweet")
            sleep(self.__delays)



m = MainActions('./config.json')
if m.mode == 1:
    m.send_tweet()
elif m.mode == 2:
    m.random_from_db()
elif m.mode == 3:
    m.send_tweet_in_timespans()
