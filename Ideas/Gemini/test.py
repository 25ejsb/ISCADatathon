API_KEY = "AIzaSyD5-Vr5C-kamIeYShZW1JcFhIdYTY2RyJM"

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
import pandas

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction="Give a rating, on a scale of 1 (least) through 100 (most), of how overall anti-semetic each of these tweets are.")

pd = pandas.read_csv("./SpaCy/GoldStandard2024_Participants.csv")

response = model.generate_content(
    f"{[str(row.Text) + ', ' for item, row in pd.head(100).iterrows()]}",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
    },
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": list[int]
    }
    )

print(response.text)

# this code doesnt work with python 3.13 for some reason