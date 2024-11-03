API_KEY = "AIzaSyD5-Vr5C-kamIeYShZW1JcFhIdYTY2RyJM"

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content(
    "Only give the rating, no other information, a scale of 0 (least) through 1 (most), how anti-semetic is this tweet: @realDonaldTrump Man you get so much hate, especially the �Jews�",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
    })

print(response.text)

# this code doesnt work with python 3.13 for some reason