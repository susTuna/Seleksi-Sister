from src.api.routes import get_math
import numexpr

class MathSolver():
    def __init__(self):
        self.math_challenge = get_math()
    
    def get_challenge(self):
        return self.math_challenge
    
    def solve(self):
        self.result = numexpr.evaluate(self.math_challenge.split("||")[0]).item()
    
    def get_result(self):
        return self.result