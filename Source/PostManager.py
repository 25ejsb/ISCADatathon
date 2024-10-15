def ReadFile(path:str) -> list[str]:
    with open(path) as file:
        lines:list[str] = file.readlines()
        
    tweets:list[str] = []
    
    tweet_index:int = 0
    reading_lines:bool = False
    for i in range(len(lines)):
        if not reading_lines and lines[i][0] == '<':
            reading_lines = True
            tweets.append(r"")
            
        elif reading_lines and lines[i][:2] == '/>':
            reading_lines = False
            tweet_index += 1
            
        elif reading_lines:
            tweets[tweet_index] += lines[i]
            
    return tweets

def RetrieveNewPost() -> list[str]:
    post:list[str] = []
    
    print("Copy and Paste whole tweet here")
    print("End it by writing END and pressing enter\n")
    
    while True:
        line:str = input()
        if line == 'END':
            break
        post.append(line)
        
    return post

def AddPostToFile(path:str, post:list[str]):
    with open(path) as file:
        text = file.readlines()
        
    text.append('<\n')
    
    for line in post:
        text.append(line + '\n')
        
    text.append('/>\n')
    
    with open(path, 'w') as file:
        file.writelines(text)