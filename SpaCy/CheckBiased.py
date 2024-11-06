import spacy
from spacy.tokens import Doc
from CleanRawTweets import CleanedTweets
from TweetData import Tweet

nlp = spacy.load("./trained_model.spacy")

def CheckBiased(text: str) -> float:
    doc: Doc = nlp(text)
    return abs(doc.cats["BIASED"])