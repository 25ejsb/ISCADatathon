API_KEY = "AIzaSyD5-Vr5C-kamIeYShZW1JcFhIdYTY2RyJM"

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(
    "On a scale of 1 through 10, give a rating on how anti-semetic this tweet is: You realize that “children of Israel” means “children of Jacob,” because he was given the name Israel after wrestling an angel? It does not mean the land of Israel and certainly not the modern state of Israel.",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
    })

print(response.text)

# this code doesnt work with python 3.13 for some reason