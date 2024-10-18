#pip install google-api-python-client
from googleapiclient import discovery
from textblob import TextBlob
from dotenv import load_dotenv
import json, os

load_dotenv()

API_KEY = os.environ.get("API_KEY")
text = "You realize that “children of Israel” means “children of Jacob,” because he was given the name Israel after wrestling an angel? It does not mean the land of Israel and certainly not the modern state of Israel."

client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False
)

analyze_request = {
    'comment': {"text": text},
    'requestedAttributes': {'TOXICITY': {}}
}

blob = TextBlob(text)

response = client.comments().analyze(body=analyze_request).execute()
print("Toxicity: " + str(eval(json.dumps(response, indent=2))["attributeScores"]["TOXICITY"]["summaryScore"]["value"]))
print("Polarity (Opinion): " + str(blob.polarity))
