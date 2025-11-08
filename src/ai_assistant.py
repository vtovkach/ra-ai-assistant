# This source file will contain logic to generate answers to questions based on the provided notes 

from openai import OpenAI, APIError, RateLimitError, AuthenticationError
import os 
from exceptions.OpenAiExceptions import *

# OpenAi Client 
_client = None

def getClient():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise OpenAIClientError("Missing OPENAI_API_KEY in environment variables")
        try:
            _client = OpenAI(api_key=api_key)
        except Exception as e:
            raise OpenAIClientError(f"Failed to initialize OpenAI client: {e}")
    return _client

def getAnswer(question: str, userNote: str, name: str) -> str:
    client = getClient()  

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are asked to turn the provided notes into a clear and complete answer to the following question: {question}. "
                        "Write as a Resident Assistant reflecting on your conversations with residents. "
                        "Use simple, natural language, as if you are personally describing what you know about the resident. "
                        "Keep your response straightforward and use simple English structures and language."
                        "Do not use colons, dashes, en dashes, or em dashes. "
                        f"Occasionally use the resident’s first name instead of pronouns. The resident’s name is {name.split(" ")[0]}. "
                        "Don't invent any information about resident. Use only provided information. If it says resident could not answer question, " 
                        "state that in the answer. Never, NEVER invent anything."
                        "Focus mainly on what is written in the notes rather than the question itself, and use simple English language."
                        "The whole answer should be short, no longer than 3 sentences and everything is placed in a single paragraph." 
                    )
                },
                {"role": "user", "content": userNote}
            ]
        )

        if not response.choices:
            raise OpenAIRequestError("No response choices returned from API")

        return response.choices[0].message.content
    
    except (RateLimitError, AuthenticationError, APIError) as e:
        raise OpenAIRequestError(f"API error: {e}") 
    except Exception as e:
        raise OpenAIRequestError(f"Unexpected error while getting answer: {e}")