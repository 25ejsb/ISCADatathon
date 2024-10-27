import pandas
import spacy

# main goal, use perspective api to find the toxicity of common words used, then find the polarity and details along with it
# Biased: unfairly prejudiced for or against someone or something.

from googleapiclient import discovery

from spacy.training import Example
from spacy.pipeline import TextCategorizer
from spacy.tokens import Doc
import spacy.training
import os, json
from tweet import tweetlist, Tweet

API_KEY = os.environ.get("API_KEY")

nlp = spacy.load("en_core_web_lg")
if "textcat_multilabel" not in nlp.pipe_names:
    nlp.add_pipe("textcat_multilabel", last=True)
text_cat: TextCategorizer = nlp.get_pipe("textcat_multilabel")
text_cat.add_label("score")

pd = pandas.read_csv("./GoldStandard2024_Participants.csv")
training_data = []
amount_to_check = 100
num = 0
for (row, item) in pd.iterrows():
    if num <= 20:
        client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=API_KEY,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False
        )
        analyze_request = {
            'comment': {"text": item.Text},
            'requestedAttributes': {'PROFANITY': {}}
        }
        response = client.comments().analyze(body=analyze_request).execute()
        score = str(eval(json.dumps(response, indent=2))["attributeScores"]["PROFANITY"]["summaryScore"]["value"])
        finalscore = 0
        if (float(item.Biased) + float(score))/2 <= 0.75:
            finalscore = 1
        training_data.append((item.Text, {"cats": {"score": finalscore}}))
        tweetlist.append(Tweet(item.ID, item.Username, item.CreateDate, item.Biased, item.Keyword, item.Text))
        num+=1
    else: break

# from TrainSpacy.py
text: list[str] = list(map(lambda x: x[0], training_data))
scores: list = list(map(lambda x: x[1], training_data))
text_as_docs: list[Doc] = list(map(nlp.make_doc, text))
examples: list[Example] = list(map(Example.from_dict, text_as_docs, scores))
text_cat.initialize(lambda: examples, nlp=nlp)
text_cat.update(examples, drop=0.5)
nlp.to_disk("./train.spacy")