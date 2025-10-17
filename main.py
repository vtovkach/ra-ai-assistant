# Program Manager 

import os 
from pathlib import Path
from mytypes import Chat
from mytypes import Chat
from dotenv import load_dotenv

# Load environment variables 
load_dotenv()

## Questions 
questions: list[str] = []

## 
processedChats: dict[str, Chat] = {}
unprocessedChats: dict[str, Chat] = {}

def setupProgram():

    ##  Get questions ## 
    with open("config/questions", "r") as f:
        cur_question: str = ""
        for line in f: 
            if not line.strip():
                continue
            if line[0] == '*':
                questions.append(cur_question)
                cur_question = ""
            else: 
                cur_question += line

    ## Retrieve processed chats 
    for path in Path("output").iterdir():
        processedChats[path] = Chat(path, questions, True)
    
    ## Retrieve unprocessed chats
    for path in Path("notes").iterdir():
        if path in processedChats:
            continue
        unprocessedChats[path] = Chat(path, questions, False)

def main():
    
    ## Set up program 
    setupProgram()

    for chat in unprocessedChats.values():
        chat.displayChat()

    for chat in processedChats.values():
        chat.displayChat()
    
    
# Run program here 
if __name__ == "__main__":
    main()