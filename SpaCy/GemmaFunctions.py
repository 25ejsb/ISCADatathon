import ollama, pandas, datetime, dotenv, os

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from TweetData import Tweet

pd = pandas.read_csv("SpaCy/GoldStandard2024_Participants.csv")

dotenv.load_dotenv()

API_KEY = os.environ.get("API_KEY")

genai.configure(api_key=API_KEY)

def rate_tweet_from_gemini(tweet: Tweet) -> float:
    response = ollama.chat(
        model="gemma2",
        messages=[
            {
                "role": "user",
                "content": f"Rate this tweet from 1 to 10 based on how anti-semetic it is, JUST GIVE THE RATING, NOTHING ELSE: {tweet.Text}",
            },
        ],
    )
    return float(response["message"]["content"])/10 # turns rating from range 0 -> 1

def add_gemini_score_to_biased(tweet: Tweet) -> dict:
    response = ollama.chat(
        model="gemma2",
        messages=[
            {
                "role": "user",
                "content": f"Rate this tweet from 1 to 10 based on how anti-semetic it is, JUST GIVE THE RATING, NOTHING ELSE: {tweet.Text}",
            },
        ],
    )
    real_score = (tweet.Biased+float(response["message"]["content"]))/2
    data_score = 1 if real_score >= 0.75 else 0
    tweet.Biased = data_score
    return {"real_score": real_score, "data_score": data_score}

def ai_generated_tweet_id() -> int:
    last_id = pd[pd.ID >= 2|000|000|000|000|000|000]["ID"].iloc[-1]
    if not last_id:
        return 2|000|000|000|000|000|000
    else:
        return int(last_id)+1

def find_text(text: str):
    found_text = pd[pd.Text.str.contains(text)]
    print(found_text)

find_text("You realize that “children of Israel” means “children of Jacob,” because he was given the name Israel after wrestling an angel? It does not mean the land of Israel and certainly not the modern state of Israel.")