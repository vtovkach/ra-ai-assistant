from dataclasses import dataclass

class UnprocessedChat:
    def __init__(self, filepath: str, questions: list[str]):
        self.filepath: str = filepath
        self.questions: list[str] = questions
        self.notes: str = ""
        self.name: str = ""
        self.date: str = ""
        self.frequency: str = ""
        self.resources: list[str] = []
        self.additionalResources: str = "" 

        self.retrieveData()

    def retrieveData(self):
        # Open the file and read the notes 
        with open(self.filepath, "r") as f:
            notes = ""
            for i, line in enumerate(f):
                if i == 0:
                    self.name = line.strip()
                elif i == 1:
                    self.date = line.strip()
                elif i == 2:
                    self.frequency = line.strip()
                elif i == 3:
                    self.resources = line.split(", ")
                elif i == 4:
                    self.additionalResources = line.strip()
                else:    
                    notes += line
            self.notes = notes.strip()
    
    def displayChat(self):
        ## Display chats's data 
        print(f"File Path: {self.filepath}")
        print(f"Name: {self.name}")
        print(f"Date: {self.date}")
        print(f"Frequency: {self.frequency}")
        print(f"Resources: {self.resources}")
        print(f"Extra Resources: {self.additionalResources}")
        print("Notes")
        print(self.notes)
        
        for q in self.questions:
            print(f"Question: {q}")

        
    
class ProcessedChat:
    def __init__(self, filepath: str, questions: list[str]):
        self.filepath: str = filepath
        self.questions: list[str] = questions
        self.answers: list[str] = []
        self.questionsNum: int = len(questions)

    def retrieveAnswers(self):
        pass 