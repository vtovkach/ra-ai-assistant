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

chats: list[Chat] = []

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

    ## Retrieve chats  
    for path in Path("notes").iterdir():
        chats.append(Chat(path, questions))

def main():
    
    ## Set up program 
    setupProgram()

    userInput = []
    while(True):

        # Use the name of the resident for selection 
        userInput = input("(RA Vadym) ").split()
        
        if len(userInput) <= 0:
            continue
        
        if userInput[0] == "exit":
            break

        if userInput[0] == "status":
            print("Status Operation")

        if userInput[0] == "show":
            showChats(userInput[1:])
            continue
        
        if userInput[0] == "process":
            print("Processing Operation")

        if userInput[0] == "submit":
            print("Submit Operation")

        if userInput[0] == "clear":
            os.system("clear")


def displayStatus() -> None:
    pass


def showChats(names: list[str]) -> None:
    
    if len(names) <= 0:
        return 
    
    if names[0] == "all":
        # Display all chats 
        for chat in chats:
            chat.displayChat()
        return 
    
    # Display chats based on input names

    for name in names:
        try:
            targetIndex = chats.index(name)
            chats[targetIndex].displayChat()
        except ValueError:
            print(f"Resident {name} does not exist!")
            continue


def processChats(names: list[str]) -> None:
    pass 


def submitChats(names: list[str]) -> None:
    pass 


# Run program here 
if __name__ == "__main__":
    main()