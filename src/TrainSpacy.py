import spacy
from spacy.training import Example
from spacy.pipeline import TextCategorizer, Morphologizer
from CleanRawTweets import CleanedTweets
import random

# Load the base model
nlp = spacy.load("en_core_web_lg")

# Create text categorizer with multi-label classification
if "textcat_multilabel" not in nlp.pipe_names:
    nlp.add_pipe("textcat_multilabel", last=True)
text_cat = nlp.get_pipe("textcat_multilabel")
text_cat.add_label("BIASED")
text_cat.add_label("JEWS")
text_cat.add_label("ISRAEL")
text_cat.add_label("KIKES")
text_cat.add_label("ZIONAZI")
# Add more categories as needed

# Add a custom morphologizer
nlp.add_pipe("morphologizer", last=True)

# Combine the data
train_data = [i.GetCategory() for i in CleanedTweets]

# Training function
def train_model(nlp, train_data, n_iter=10):       
    
    examples = []
    for text, annotations in train_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        examples.append(example)
        
    text_cat.initialize(lambda: examples, nlp=nlp)
    text_cat.update(examples, drop=0.5)
    
    for i in range(n_iter):
        random.shuffle(train_data)
        
        # Create the examples for text categorization
        examples = []
        for text, annotations in train_data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            examples.append(example)

        # Update the text categorizer
        nlp.update(examples, drop=0.5)

# Train the model
train_model(nlp, train_data, n_iter=10)

# Save the trained model
nlp.to_disk("./trained_model.spacy")
