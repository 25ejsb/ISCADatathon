import nltk
import GenerateNGrams
import PostManager

def PrintActions():
    print()
    print("--POSSIBLE ACTIONS--")
    print()
    print("ADD-----------Add new tweet to database")
    print("GET (x)-------Print tweet from database of index x")
    print("NGRAM (x)(n)--Print NGrams of length n from tweet of index x")
    print("QUIT----------Kill process")
    print("?-------------List possible actions")

if __name__ == '__main__':
    while True:
        action = input("\nENTER ACTION: (? for list of possible actions)\n").lower().split()
        
        if action == ['?']:
            PrintActions()
            
        elif action[0] == ['add']:
            print()
            new_tweet = PostManager.RetrieveNewPost()
            PostManager.AddPostToFile(r"C:\Users\hunte\OneDrive\Documents\Python Scripts\CalculateAntiSemitism\Tweets.txt", new_tweet)
            
        elif action[0] == 'get' and action[1].isdigit() and len(action) == 2:
            tweets:list[str] = PostManager.ReadFile(r"C:\Users\hunte\OneDrive\Documents\Python Scripts\CalculateAntiSemitism\Tweets.txt")
            print()
            print("----\n")
            print(tweets[int(action[1]) - 1])
            print("----")
            
        elif action[0] == 'ngram' and action[1].isdigit() and action[2].isdigit() and len(action) == 3:
            tweets:list[str] = PostManager.ReadFile(r"C:\Users\hunte\OneDrive\Documents\Python Scripts\CalculateAntiSemitism\Tweets.txt")
        
            freq_dist:nltk.FreqDist = GenerateNGrams.CountNGramsFromText(tweets[int(action[2]) - 1], int(action[3]))
            
            freq_dist.pprint()
        
        elif action == ['quit']:
            break
            

        
        
