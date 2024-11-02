import pandas
import spacy
from googleapiclient import discovery
from spacy.training import Example
from spacy.pipeline import TextCategorizer
from spacy.tokens import Doc
import spacy.training
import os, json
import numpy as np
from sklearn.preprocessing import MinMaxScaler

API_KEY = os.environ.get("API_KEY")

nlp = spacy.load("en_core_web_lg")

pd = pandas.read_csv("./GoldStandard2024_Participants.csv")

texts = []
scores = []

amount_to_check = 60

def create_model(check):
    num = 0
    for (row, item) in pd.iterrows():
        if num <= check:
            client = discovery.build(
                "commentanalyzer",
                "v1alpha1",
                developerKey=API_KEY,
                discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                static_discovery=False
            )

            analyze_request = {
                'comment': {"text": item.Text},
                'requestedAttributes': {'TOXICITY': {}}
            }

            response = client.comments().analyze(body=analyze_request).execute()

            score = eval(json.dumps(response, indent=2))["attributeScores"]["TOXICITY"]["summaryScore"]["value"]

            texts.append(item.Text)
            scores.append(score)

            num+=1
        else: break

    text_vectors = np.array([nlp(text).vector for text in texts])

    # Step 2: Scale the scores to match the range of text embeddings
    # For compatibility, we reshape scores to fit the shape of the text embeddings.
    scaler = MinMaxScaler()
    scaled_scores = scaler.fit_transform(np.array(scores).reshape(-1, 1))

    # Expand scaled scores to match text vector dimensions
    score_vectors = np.tile(scaled_scores, (1, text_vectors.shape[1]))

    # Step 3: Compute the cosine similarity between each text vector and its corresponding score vector
    similarities = np.array([np.dot(text_vectors[i], score_vectors[i]) / 
                            (np.linalg.norm(text_vectors[i]) * np.linalg.norm(score_vectors[i]))
                            for i in range(len(texts))])

    # Display results
    for i, similarity in enumerate(similarities):
        print(f"Text: {texts[i]}")
        print(f"Score: {scores[i]}")
        print(f"Similarity: {similarity:.4f}\n")

create_model(check=20)