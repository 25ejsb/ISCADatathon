import spacy

class Tweet:
    
    def __init__(self, ID:int, username:str, date:str, biased:int, keyword:str, text:str):
        
        self.ID = ID
        self.Username = username
        self.Date = date
        self.Biased = biased
        self.Keyword = keyword
        self.Text = text
        
    def GetCategory(self) -> tuple:
        
        return (self.Text, {"cats": {"BIASED": self.Biased, 
                                     "JEWS": 1 if self.Keyword == 'Jews' else 0,
                                     "ISREAL": 1 if self.Keyword == 'Isreal' else 0,
                                     "KIKES": 1 if self.Keyword == 'Kikes' else 0,
                                     "ZIONAZI": 1 if self.Keyword == 'ZioNazi' else 0}})
        
        
def CleanTweet(data:str, nlp) -> Tweet:
    
    text_split = data.split(',')
    
    if text_split[0].isdigit():
        ID:int = int(text_split[0])
    
    username:str = text_split[1]
    
    date:str = text_split[2]
    
    if text_split[3].isdigit():
        biased:int = int(text_split[3])
    
    keyword:str = text_split[4]
    
    text:str = RemoveLinks(','.join(text_split[5:]))
    
    return Tweet(ID, username, date, biased, keyword, text)
    

def RemoveLinks(text:str):
    
    link_split_text:list[str] = text.split('https')
    
    return link_split_text[0]
        