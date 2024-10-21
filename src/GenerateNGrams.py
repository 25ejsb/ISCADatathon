import nltk
import re

regex = re.compile('[^a-zA-Z_1-9]')

def SplitText(text:str) -> list[str]:
    text_lower:str = text.lower()
    
    split_text:list[str] = nltk.word_tokenize(text_lower)
    
    split_text_len = len(split_text)
    
    for i in range(split_text_len):
        split_text[split_text_len - i - 1] = regex.sub('', split_text[split_text_len - i - 1])
        
        if len(split_text[split_text_len - i - 1]) <= 0:
            split_text.pop(split_text_len - i - 1)
    
    return split_text

def GenerateNGramsFromText(text:str, length:int) -> list[tuple]:    
    split_text:list[str] = SplitText(text)
    
    return list(nltk.ngrams(split_text, length))

def CountNGramsFromText(text:str, length:int) -> nltk.FreqDist:
    n_grams:list[tuple] = GenerateNGramsFromText(text, length)
    
    freq_dist:nltk.FreqDist = nltk.FreqDist(n_grams)
    
    return freq_dist
    
    
        
        