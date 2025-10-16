from dataclasses import dataclass


class Chat:
    def __init__(self, filepath: str, questions: list[str], isProcessed: bool):
        self.filepath: str = filepath
        self.isProcessed = isProcessed
        self.questions: list[str] = questions
        self.answers: list[str] = []
        self.notes: list[str] = []
        self.name: str = ""
        self.date: str = ""
        self.frequency: str = ""
        self.resources: list[str] = []
        self.additionalResources: str = "" 

        self.retrieveData()

    def retrieveData(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Basic metadata
        self.name = lines[0].strip() if len(lines) > 0 else ""
        self.date = lines[1].strip() if len(lines) > 1 else ""
        self.frequency = lines[2].strip() if len(lines) > 2 else ""
        self.resources = [r.strip() for r in lines[3].split(",")] if len(lines) > 3 else []
        self.additionalResources = lines[4].strip() if len(lines) > 4 else ""

    def displayChat(self):
        print("\n" + "=" * 50)
        print(f"📄 Chat Summary for: {self.name}")
        print("=" * 50)

        print(f"🗂️  File Path        : {self.filepath}")
        print(f"✅ Processed         : {self.isProcessed}")
        print(f"📅 Date              : {self.date}")
        print(f"🔁 Frequency         : {self.frequency}")
        print(f"📚 Resources         : {self.resources}")
        print(f"➕ Extra Resources   : {self.additionalResources}")

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