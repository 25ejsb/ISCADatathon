import GenerateNGrams
import nltk

if __name__ == '__main__':
    freq_dist:nltk.FreqDist = GenerateNGrams.GenerateNGramsFromFile(r"C:\Users\hunte\OneDrive\Documents\Python Scripts\CalculateAntiSemitism\HOPG.txt", 3)
    
    freq_dist.pprint()