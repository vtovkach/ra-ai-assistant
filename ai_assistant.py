# This source file will contain logic to generate answers to questions based on the provided notes 

from openai import OpenAI
import os 

# OpenAi Client 
_client = None

def getClient():
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client

def getAnswer(question: str, userNote: str, name: str) -> str:
    client = getClient()  

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are asked to turn the provided notes into a clear and complete answer to the following question: {question}. "
                    "Write as a Resident Assistant reflecting on your conversations with residents. "
                    "Use simple, natural language, as if you are personally describing what you know about the resident. "
                    "Keep your response straightforward and thoughtful—avoid exaggeration or unnecessary complexity. "
                    "Do not use colons, dashes, en dashes, or em dashes. "
                    f"Occasionally use the resident’s name instead of pronouns. The resident’s name is {name}. "
                    "Do not make up any information. "
                    "Focus mainly on what is written in the notes rather than the question itself, and keep the tone plain and simple. The whole answer should be no longer "
                    "than 4 sentences." 
                )
            },
            {"role": "user", "content": userNote}
        ]
    )

    return response.choices[0].message.content