import spacy
from spacy.training import Example
from spacy.pipeline import TextCategorizer
from spacy.tokens import Doc
import spacy.training
from CleanRawTweets import CleanedTweets
import random
import time

start_time = time.time()

print("Loading Base Model!")

# Load the base model
nlp = spacy.load("en_core_web_lg")

# Create text categorizer with multi-label classification
if "textcat_multilabel" not in nlp.pipe_names:
    nlp.add_pipe("textcat_multilabel", last=True)
text_cat = nlp.get_pipe("textcat_multilabel")
text_cat.add_label("BIASED")


train_data: list[tuple] = [i.GetCategory() for i in CleanedTweets]

def train_model(nlp: spacy.language.Language, train_data:list[tuple], n_iter=10):       
    
    print("Started Training")
    
    text: list[str] = list(map(lambda x: x[0], train_data))
    annotations: list = list(map(lambda x: x[1], train_data))
    
    text_as_docs: list[Doc] = list(map(nlp.make_doc, text))
    examples: list[Example] = list(map(Example.from_dict, text_as_docs, annotations))
        
    text_cat.initialize(lambda: examples, nlp=nlp)
    text_cat.update(examples, drop=0.5)
    
    print("Completed Initialization!")
    
    for i in range(n_iter):
        random.shuffle(train_data)
        
        text: list[str] = list(map(lambda x: x[0], train_data))
        annotations: list = list(map(lambda x: x[1], train_data))
        
        text_as_docs: list[Doc] = list(map(nlp.make_doc, text))
        
        examples: list[Example] = list(map(Example.from_dict, text_as_docs, annotations))

        nlp.update(examples, drop=0.5)
        
        print(f"{float(i + 1) / float(n_iter) * 100}% complete after {time.time() - start_time} Seconds")

train_model(nlp, train_data, n_iter=1000)

nlp.to_disk("./trained_model.spacy")

print(f"Done in {time.time() - start_time} Seconds")