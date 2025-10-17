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

def getAnswer(question: str, userNote: str) -> str:
    client = getClient()  

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are asked to turn the provided notes into a clear and complete answer to the following question: {question}. " \
                    "Respond as a Resident Assistant writing reflections about your conversations with residents. " \
                    "Keep the language simple and natural, as if you are personally describing what you know about the resident. " \
                    "Avoid overcomplicating or exaggerating — just give a straightforward and thoughtful answer " \
                    "and do not use colons, dashes, en dashes, or em dashes in your response."
                )
            },
            {"role": "user", "content": userNote}
        ]
    )

    return response.choices[0].message.content