from src.mathsolver.solver import MathSolver

M = MathSolver()
challenge = M.get_challenge()
M.solve()
result = M.get_result()
print(f"Challenge: {challenge}")
print(f"Result: {result}")