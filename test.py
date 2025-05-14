import numpy as np
from scipy.optimize import linprog

# Payoff matrix (Hider's perspective)
payoff_matrix = np.array([
    [-3.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0],
    [ 1.0, -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0],
    [ 2.0,  2.0, -1.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0],
    [ 1.0,  1.0,  1.0, -3.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0],
    [ 2.0,  2.0,  2.0,  2.0, -1.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0],
    [ 1.0,  1.0,  1.0,  1.0,  1.0, -3.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0],
    [ 2.0,  2.0,  2.0,  2.0,  2.0,  2.0, -1.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0],
    [ 2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0, -1.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0],
    [ 2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0, -1.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0],
    [ 1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -3.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0],
    [ 1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -3.0,  1.0,  1.0,  1.0,  1.0,  1.0],
    [ 1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -3.0,  1.0,  1.0,  1.0,  1.0],
    [ 1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -3.0,  1.0,  1.0,  1.0],
    [ 2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0, -1.0,  2.0,  2.0],
    [ 2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0, -1.0,  2.0],
    [ 2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0,  2.0, -1.0]
])

# Solve for Hider's strategy (maximin)
num_hider_strategies, num_seeker_strategies = payoff_matrix.shape

# Hider's problem: maximize v subject to A_ub @ p <= b_ub
# We need to reformulate as: minimize -v subject to payoff_matrix.T @ p >= v
# Which is equivalent to: [-payoff_matrix.T, 1] @ [p, v] <= 0

c = np.zeros(num_hider_strategies + 1)
c[-1] = -1  # maximize v

A_ub = np.hstack([-payoff_matrix.T, np.ones((num_seeker_strategies, 1))])
b_ub = np.zeros(num_seeker_strategies)

A_eq = np.zeros((1, num_hider_strategies + 1))
A_eq[0, :num_hider_strategies] = 1  # probabilities sum to 1
b_eq = np.array([1])

bounds = [(0, None) for _ in range(num_hider_strategies)] + [(None, None)]

result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)

hider_probs = result.x[:-1]
game_value = result.x[-1]

print("Hider's optimal strategy:")
for i, prob in enumerate(hider_probs):
    if prob > 1e-6:  # ignore near-zero probabilities
        print(f"Position {i+1}: {prob:.4f}")

print(f"\nGame value (from Hider's perspective): {game_value:.4f}")

# Solve for Seeker's strategy (minimax)
# Seeker's problem: minimize u subject to payoff_matrix @ q <= u

c = np.zeros(num_seeker_strategies + 1)
c[-1] = 1  # minimize u

A_ub = np.hstack([payoff_matrix, -np.ones((num_hider_strategies, 1))])
b_ub = np.zeros(num_hider_strategies)

A_eq = np.zeros((1, num_seeker_strategies + 1))
A_eq[0, :num_seeker_strategies] = 1  # probabilities sum to 1
b_eq = np.array([1])

bounds = [(0, None) for _ in range(num_seeker_strategies)] + [(None, None)]

result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)

seeker_probs = result.x[:-1]
game_value_seeker = result.x[-1]

print("\nSeeker's optimal strategy:")
for j, prob in enumerate(seeker_probs):
    if prob > 1e-6:  # ignore near-zero probabilities
        print(f"Search Position {j+1}: {prob:.4f}")

print(f"\nGame value (from Seeker's perspective): {game_value_seeker:.4f}")