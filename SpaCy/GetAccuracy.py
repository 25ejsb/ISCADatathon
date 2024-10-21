import spacy
from spacy.tokens import Doc
from CleanRawTweets import CleanedTweets
from TweetData import Tweet

nlp = spacy.load("./trained_model.spacy")

def GetError(tweet:Tweet) -> float:

    doc: Doc = nlp(tweet.Text)
    
    return abs(tweet.Biased - doc.cats['BIASED'])

cumulative_error:float = 0

for i in CleanedTweets:
    cumulative_error += GetError(i)
    
average_error = cumulative_error / float(len(CleanedTweets))

percent_error = average_error * 100

print(f"{percent_error}% Error")