import nltk

nltk.download('punkt_tab')

def SplitText(text:str) -> list[str]:
    text_lower:str = text.lower()
    
    return set(nltk.word_tokenize(text_lower))

def GenerateNGramsFromFile(path:str, length:int) -> list[tuple]:
    with open(path) as file:
        text:str = file.read()
    
    split_text:list[str] = SplitText(text)
    
    return list(nltk.ngrams(split_text, length))

def CountNGramsFromFile(path:str, length:int) -> nltk.FreqDist:
    n_grams:list[tuple] = GenerateNGramsFromFile(path, length)
    
    return nltk.FreqDist(n_grams)
    
    
        
        