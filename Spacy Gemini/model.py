import pandas, ollama, spacy, random, threading

# main goal, use perspective api to find the toxicity of common words used, then find the polarity and details along with it
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from spacy.training import Example
from spacy.pipeline import TextCategorizer
from spacy.tokens import Doc
import spacy.training
import os, json, time
from tweet import tweetlist, Tweet
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")

spacy.prefer_gpu()

nlp = spacy.load("en_core_web_lg")
if "textcat_multilabel" not in nlp.pipe_names:
    nlp.add_pipe("textcat_multilabel", last=True)
text_cat: TextCategorizer = nlp.get_pipe("textcat_multilabel")
text_cat.add_label("score")

genai.configure(api_key=API_KEY)

pd = pandas.read_csv("./GoldStandard2024_Participants.csv")

training_data = []

def add_training_data(amount: int, start_index: int):
    for i, (row, item) in enumerate(pd.head(amount).iterrows(), start=start_index):
        print(i)
        response = ollama.chat(
            model="gemma2",
            messages=[
                {
                    "role": "user",
                    "content": f"Rate this tweet from 1 to 10 based on how anti-semetic it is, JUST GIVE THE RATING, NOTHING ELSE: {item.Text}",
                },
            ],
        )
        score = (item.Biased)+(float(int(response["message"]["content"])/10))/2
        finalscore = 0
        if (float(item.Biased) + score)/2 <= 0.75:
            finalscore = 1
        training_data.append((item.Text, {"cats": {"score": finalscore}}))
        tweetlist.append(Tweet(item.ID, item.Username, item.CreateDate, item.Biased, item.Keyword, item.Text))

add_training_data(1000, 500) 

#from TrainSpacy.py
text: list[str] = list(map(lambda x: x[0], training_data))
scores: list = list(map(lambda x: x[1], training_data))
text_as_docs: list[Doc] = list(map(nlp.make_doc, text))
examples: list[Example] = list(map(Example.from_dict, text_as_docs, scores))
text_cat.initialize(lambda: examples, nlp=nlp)
text_cat.update(examples, drop=0.5)
# for i in range(10):
#     print(i)
#     random.shuffle(training_data)
        
#     text: list[str] = list(map(lambda x: x[0], training_data))
#     annotations: list = list(map(lambda x: x[1], training_data))
        
#     text_as_docs: list[Doc] = list(map(nlp.make_doc, text))
        
#     examples: list[Example] = list(map(Example.from_dict, text_as_docs, annotations))

#     nlp.update(examples, drop=0.5)
nlp.to_disk("./train.spacy")