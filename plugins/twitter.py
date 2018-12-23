import tweepy
import utils
from prettytable import PrettyTable
from mango_plugin import mango_plugin
from MessageListener import MessageListener

def instance():
    return Twitter()


class Twitter(mango_plugin):
    def __init__(self):
        #print('[TWTTR]')
        twitterConfigData = utils.loadJSON(utils.getConfigFile('twitter.json'))
        consKey = twitterConfigData["consumer_key"]
        consSecret = twitterConfigData["consumer_secret"]
        accessToken = twitterConfigData["access_token"]
        accessTokenSecret = twitterConfigData["access_token_secret"]

        auth = tweepy.OAuthHandler(consKey, consSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        self.api = tweepy.API(auth)
        self.table = PrettyTable(['Twitter trends'])

    def go(self, args: list, message_listener: MessageListener = MessageListener()):
        if not utils.internet_reachable():
            message_listener.printMessage("Twitter : offline")
            return -1

        # public_tweets = api.home_timeline()
        # for tweet in public_tweets:
        #	print(tweet.text)

        # user = api.get_user('roc5cor')
        # print(user.screen_name)
        # print(user.followers_count)
        # for friend in user.friends():
        #    print(friend.screen_name)

        # self.api.update_status("Mango Application is on twitter !!!")
        # closestIDAvailable = self.api.trends_closest(44.933393,4.892360)[0]['woeid']
        # print(closestIDAvailable)

        # trends = self.api.trends_place(closestIDAvailable)[0]['trends']
        # print(trends)
        # for trend in trends:
        #    print(trend['name'])

        trends = self.api.trends_place(1)[0]['trends']
        # print(trends)
        for trend in trends[:10]:
            self.table.add_row([trend['name']])
        message_listener.printMessage(self.table.get_string())


        # print(str(self.api.rate_limit_status()) + ' api calls left')
