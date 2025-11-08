

class LoginFail(Exception):
    def __init__(self, value, code =None):
        self.value = value
        self.code = code 
        super().__init__(f"Error {value}")
    
    def __str__(self):
        return f"[Runtime Exception] {self.value}"