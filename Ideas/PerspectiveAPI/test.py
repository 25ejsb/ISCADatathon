#pip install google-api-python-client
from googleapiclient import discovery
from textblob import TextBlob
from dotenv import load_dotenv
import json, os

load_dotenv()

API_KEY = os.environ.get("API_KEY")
text = "We got very difficult situation with Kikes. They think they can buy our people, land, faith, but this will not happen. These Jewish degenerates defamed our Jesus Christ”. Antisemitic rally took place in Uman."

client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False
)

analyze_request = {
    'comment': {"text": text},
    'requestedAttributes': {'PROFANITY': {}}
}

blob = TextBlob(text)

response = client.comments().analyze(body=analyze_request).execute()
print("Score: " + str(eval(json.dumps(response, indent=2))["attributeScores"]["PROFANITY"]["summaryScore"]["value"]))
print("Polarity: " + str(blob.polarity))