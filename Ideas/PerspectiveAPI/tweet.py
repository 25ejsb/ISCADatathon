import spacy
from spacy.tokens import Doc

tweetlist = []

# from Tweet.py
class Tweet:
    
    def __init__(self, ID:int, username:str, date:str, biased:int, keyword:str, text:str):
        
        self.ID = ID
        self.Username = username
        self.Date = date
        self.Biased = biased
        self.Keyword = keyword
        self.Text = text
        
    def GetCategory(self):
        
        return (self.Text, {"cats": {"BIASED": self.Biased}})
