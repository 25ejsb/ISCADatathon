import spacy
from spacy.tokens import Doc
from tweet import Tweet
import pandas

# from GetAccuracy.py
nlp = spacy.load("./trained_model.spacy")

pd = pandas.read_csv("Ideas\PerspectiveAPI\GoldStandard2024_Participants.csv")

tweetlist = [Tweet(tweet.ID, tweet.Username, tweet.CreateDate, tweet.Biased, tweet.Keyword, tweet.Text) for row, tweet in pd.iterrows()]

def GetData(tweet:str):

    doc: Doc = nlp(tweet)
    
    return abs(doc.cats['BIASED'])

print(GetData("0,asd,0/0/0,1,Jews,death to the jews"))