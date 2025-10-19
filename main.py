# Program Manager 

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

        if userInput[0] == "show":
            print("Show Operation") 
        
        if userInput[0] == "process":
            print("Processing Operation")

        if userInput[0] == "submit":
            print("Submit Operation")


# Run program here 
if __name__ == "__main__":
    main()