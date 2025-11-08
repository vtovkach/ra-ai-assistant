
class OpenAIClientError(Exception):
    def __init__(self, message="OpenAI client initialization failed"):
        super().__init__(message)

class OpenAIRequestError(Exception):
    def __init__(self, message="OpenAI request failed"):
        super().__init__(message)