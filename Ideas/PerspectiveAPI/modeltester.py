import spacy
from spacy.tokens import Doc
from tweet import Tweet, tweetlist

# from GetAccuracy.py
nlp = spacy.load("./train.spacy")

def GetError(tweet:Tweet):

    doc: Doc = nlp(tweet.Text)
    
    return abs(tweet.Biased - doc.cats['BIASED'])

for tweet in tweetlist:
    print(GetError(tweet))