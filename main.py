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
        chats.append(Chat(str(path), questions))

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
            displayStatus()

        if userInput[0] == "show":
            print("Show Operation") 
        
        if userInput[0] == "process":
            print("Processing Operation")

        if userInput[0] == "submit":
            print("Submit Operation")


def displayStatus() -> None:

    if not chats:
        print("No chats to display")
        return 
    
    print(f"{'File Path':<25} {'Name':<25} {'Processed':<10} {'Submitted':<10}")
    print("-" * 75)

    for chat in chats:
        print(f"{chat.filepath:<25} {chat.name:<25} {'Yes' if chat.isProcessed else 'False':<10} {'Yes' if chat.isSubmitted else 'False':<10}")
        print("-" * 75)

def showChats(names: list[str]) -> None:
    pass


def processChats(names: list[str]) -> None:
    pass 


def submitChats(names: list[str]) -> None:
    pass 


# Run program here 
if __name__ == "__main__":
    main()