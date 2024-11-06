import spacy
from spacy.tokens import Doc
from tweet import Tweet
import pandas

# from GetAccuracy.py
nlp = spacy.load("./train.spacy")

pd = pandas.read_csv("./GoldStandard2024_Participants.csv")

tweetlist = [Tweet(tweet.ID, tweet.Username, tweet.CreateDate, tweet.Biased, tweet.Keyword, tweet.Text) for row, tweet in pd.iterrows()]

def GetData(tweet:str):

    doc: Doc = nlp(tweet)
    
    return doc.cats['score']

print(GetData("")) # THIS IS FOR TESTING, DON'T TAKE THESE MESSAGES LITERALLY