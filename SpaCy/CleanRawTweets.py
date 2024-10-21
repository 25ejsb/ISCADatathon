import spacy
from TweetData import Tweet, CleanTweet

nlp = spacy.load('en_core_web_lg')

with open("E:\GithubRepos\Clicker Game\ISCADatathon\src\GoldStandard2024_Participants.csv", 'r', encoding='utf-8', errors='ignore') as file:
    raw_tweets:list[str] = file.readlines()
    
raw_tweets.pop(0)
    
CleanedTweets:list[Tweet] = [CleanTweet(i, nlp) for i in raw_tweets]