from enum import IntEnum
from ai_assistant import *
from datetime import datetime
from typing import Self
from upload import *
import asyncio

from upload import submitForm

class ProgramField(IntEnum):
    NAME = 0
    DATE = 1
    FREQUENCY = 2
    RES = 3
    OTHER_RES = 4
    IS_SUBMITTED = 5
    IS_PROCESSED = 6
    NOTES = 7

class Chat:
    def __init__(self, filepath: str, questions: list[str]):
        self.filepath: str = filepath
        self.isProcessed = False
        self.questions: list[str] = questions
        self.answers: list[str] = []
        self.notes: list[str] = []
        self.name: str = ""
        self.date: str = ""
        self.frequency: str = ""
        self.resources: list[str] = []
        self.additionalResources: str = "" 
        self.isSubmitted: bool = False

        self.retrieveData()

    
    def __eq__(self, other):
       if isinstance(other, str):
           return self.name.split()[0] == other
       if isinstance(other, Chat):
           return self.name == other.name
       return False 


    def retrieveData(self) -> None:
        with open(self.filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Basic metadata
        self.name = lines[ProgramField.NAME].strip() if len(lines) > 0 else ""
        self.date = lines[ProgramField.DATE].strip() if len(lines) > 1 else ""
        self.frequency = lines[ProgramField.FREQUENCY].strip() if len(lines) > 2 else ""
        self.resources = [r.strip() for r in lines[ProgramField.RES].split(",")] if len(lines) > 3 else []
        self.additionalResources = lines[ProgramField.OTHER_RES].strip() if len(lines) > 4 else ""

        if lines[ProgramField.IS_PROCESSED].strip().lower() == "true":
            self.isProcessed = True

        if lines[ProgramField.IS_SUBMITTED].strip().lower() == "true":
            self.isSubmitted = True
        
        # Retrieve Notes and Answers 
        buffer = ""
        notes = True; 
        for line in lines[ProgramField.NOTES:]:
            
            if line.startswith("**"):
                if buffer:
                    if notes:
                        # Append to notes 
                        self.notes.append(buffer)
                    else:
                        # Append to asnswers
                        self.answers.append(buffer)
                buffer = ""
                buffer += line.lstrip("*")
                notes = True
                
            elif line.startswith("*"):
                if buffer:
                    if notes:
                        # Append to notes 
                        self.notes.append(buffer)
                    else:
                        # Append to answers 
                        self.answers.append(buffer)
                buffer = ""
                buffer += line.lstrip("*")
                notes = False 
            
            else:
                buffer += line 
            
        # Add last buffer if it exists 
        if buffer: 
            if notes:
                self.notes.append(buffer)
            else:
                self.answers.append(buffer)


    def displayChat(self) -> None:
        print("\n" + "=" * 50)
        print(f"📄 Chat Summary for: {self.name}")
        print("=" * 50)

        print(f"🗂️  File Path        : {self.filepath}")
        print(f"✅ Processed         : {self.isProcessed}")
        print(f"📅 Date              : {self.date}")
        print(f"🔁 Frequency         : {self.frequency}")
        print(f"📚 Resources         : {self.resources}")
        print(f"➕ Extra Resources   : {self.additionalResources}")
        print(f" Is Submitted        : {self.isSubmitted}")  
        print(f" Is processed        : {self.isProcessed}")
        print("\n📝 Notes:")
        print("-" * 50)

        for i, note in enumerate(self.notes, 1):
            print(f"\n  Note {i}:")
            print(note.strip())

        print("-" * 50)

        print("\n❓ Questions:")
        for i, q in enumerate(self.questions, 1):
            print(f"  {i}. {q.strip()}")

        print("\n💬 Answers:")
        for i, a in enumerate(self.answers, 1):
            if a and a.strip():
                print(f"  {i}. {a.strip()}")

        print("=" * 50 + "\n")

    async def processChat(self) -> tuple[Self, bool]:

        # Ensure the chat is not processed yet 
        if self.isProcessed:
            return self, False
        
        for i, q in enumerate(self.questions):
            try:
                answer = await asyncio.to_thread(getAnswer, q, self.notes[i], self.name)
                self.answers.append(answer)
            except Exception as e:
                with open("log.txt", "a") as f:
                    f.write(f"[{datetime.now()}] {str(e)}\n")
                return self, False
                
        # Mark chat as processed 
        self.isProcessed = True
        
        return self, True

    def submitChat(self) -> None:
        print(f"Submitting chat with resident {self.name}.")
        submitForm(self)
        
    def saveChat(self) -> None:

        '''
        Structure of the file 
        # Line 1: Resident Name
        # Line 2: Date when the conversation happened 
        # Line 3: Frequency
        # Line 4: Resources (separate with coma) 
        # Line 5: Additional Resources 
        # Line 6: Is submitted 
        # Line 7: Is processed 
        # Line 8 to Line n: **Notes
        # Line n + 1 to Line k: *Answers  
        '''

        with open("notes/temp.txt", "w", encoding="utf-8") as f:

            f.write(self.name + "\n")
            f.write(self.date + "\n")
            f.write(self.frequency + "\n")

            # Save resources 
            f.write(", ".join(self.resources) + "\n")

            f.write(self.additionalResources + "\n")
            f.write(str(self.isSubmitted) + "\n")
            f.write(str(self.isProcessed) + "\n")

            # Save Notes
            for note in self.notes:
                f.write("**" + note)
            f.write("\n")

            # Save Answers
            for answer in self.answers:
                f.write("*" + answer + "\n")
                
        # Delete old file and rename the temp.txt 
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
        os.replace("notes/temp.txt", self.filepath)