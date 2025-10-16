# Program Manager 

import os 
from pathlib import Path
from mytypes import Chat
from mytypes import Chat

## Questions 
questions: list[str] = []

## 
processedChat: dict[str, Chat] = {}
unprocessedChat: dict[str, Chat] = {}

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
        processedChat[path] = Chat(path, questions, True)
    
    ## Retrieve unprocessed chats
    for path in Path("notes").iterdir():
        if path in processedChat:
            continue
        unprocessedChat[path] = Chat(path, questions, False)

def main():
    
    ## Set up program 
    setupProgram()

    for chat in unprocessedChat.values():
        chat.displayChat()

# Run program here 
if __name__ == "__main__":
    main()