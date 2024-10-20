API_KEY = "AIzaSyD5-Vr5C-kamIeYShZW1JcFhIdYTY2RyJM"

import google.generativeai as genai
import os

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("On a scale of 1 through 10, give a rating on how anti-semetic this tweet is: You realize that “children of Israel” means “children of Jacob,” because he was given the name Israel after wrestling an angel? It does not mean the land of Israel and certainly not the modern state of Israel.")
with open("result.txt", "w") as file:
    file.write(response.text)

# this code doesnt work with python 3.13 for some reason