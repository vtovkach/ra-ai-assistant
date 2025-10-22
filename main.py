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
            # Save all chats before exiting 
            saveChats(["all"])
            break

        if userInput[0] == "status":
            displayStatus()
            continue

        if userInput[0] == "show":
            showChats(userInput[1:])
            continue
        
        if userInput[0] == "process":
            processChats(userInput[1:])
            continue

        if userInput[0] == "submit":
            submitChats(userInput[1:])
            continue

        if userInput[0] == "save":
            saveChats(userInput[1:])

        if userInput[0] == "clear":
            os.system("clear")
            continue


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

# Integrate async requests later 
def processChats(names: list[str]) -> None:

    if len(names) <= 0:
        return 

    print("Processing...")

    if names[0] == "all":
        # process all chats 
        for chat in chats:
            chat.processChat()
            print(f"Chat with resident {chat.name} is processed.")
        return    
    
    for name in names:
        try:
            targetIndex = chats.index(name)
            chats[targetIndex].processChat()
            print(f"Chat with resident {chats[targetIndex].name} is processed.")
        except ValueError:
            print(f"Resident {name} does not exist!")
            continue
    

def submitChats(names: list[str]) -> None:
    
    if len(names) <= 0:
        return

    if names[0] == "all":
        for chat in chats:
            chat.submitChat()
        return 

    for name in names:
        try:
            targetIndex = chats.index(name)
            chats[targetIndex].submitChat()
        except ValueError:
            print(f"Resident {name} does not exist.")
            continue


def saveChats(names: list[str]) -> None:
    if len(names) <= 0:
        return

    if names[0] == "all":
        for chat in chats:
            try:
                chat.saveChat()
                print(f"Chat with resident {chat.name} is saved ✅")
            except Exception as e:
                print(f"Failed to save chat with resident {chat.name} ❌")
                continue
        return 

    for name in names:
        try:
            targetIndex = chats.index(name)
            chats[targetIndex].saveChat()
            print(f"Chat with resident {chats[targetIndex].name} is saved ✅")
        except ValueError:
            print(f"Resident {name} does not exist.")
            continue
        except Exception as e:
            print(f"Failed to save chat with resident {chats[targetIndex].name} ❌ ")
            continue

# Run program here 
if __name__ == "__main__":
    main()