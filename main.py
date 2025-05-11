import numpy as np
import random
from scipy.optimize import linprog
import json



class HideAndSeekGame:
    def __init__(self, world_size, use_proximity=False, is_2d=False):
        self.world_size = world_size
        self.use_proximity = use_proximity
        self.is_2d = is_2d
        
        # Calculate grid dimensions for 2D worlds
        if is_2d:
            self.rows = int(np.sqrt(world_size))
            while world_size % self.rows != 0:
                self.rows -= 1
            self.cols = world_size // self.rows
        else:
            self.rows = 1
            self.cols = world_size
            
        self.reset_game()
    
    def reset_game(self):
        self.place_types = self.generate_place_types()
        self.payoff_matrix = self.generate_payoff_matrix()
        self.human_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.human_wins = 0
        self.computer_wins = 0
        self.human_role = None
        self.calculate_optimal_strategies()
    
    def generate_place_types(self):
        """Generate place types ensuring at least one of each type"""
        # First ensure we have at least one of each type
        place_types = [0, 1, 2]  # One hard, one neutral, one easy
        
        # Fill remaining positions with weighted random choices
        remaining = self.world_size - 3
        if remaining > 0:
            type_weights = [0.3, 0.4, 0.3]  # Hard, Neutral, Easy
            place_types.extend(random.choices([0, 1, 2], weights=type_weights, k=remaining))
        
        # Shuffle the positions
        random.shuffle(place_types)
        return place_types
    
    def calculate_distance(self, pos1, pos2):
        """Enhanced distance calculation with scaling"""
        if self.is_2d:
            x1, y1 = pos1 // self.cols, pos1 % self.cols
            x2, y2 = pos2 // self.cols, pos2 % self.cols
            distance = np.sqrt((x1-x2)*2 + (y1-y2)*2)  # Euclidean distance
        else:
            distance = abs(pos1 - pos2)  # Linear distance for 1D
        
        # Scale distance to 0-1 range based on world size
        max_distance = np.sqrt((self.rows-1)*2 + (self.cols-1)*2) if self.is_2d else self.world_size-1
        return distance / max_distance
    
    def generate_payoff_matrix(self):
        """Generate payoff matrix with enhanced proximity effects"""
        matrix = np.zeros((self.world_size, self.world_size))
        
        # More distinct payoffs for each place type
        payoffs = {
            # (found_payoff, not_found_payoff)
            0: (-6, 0.5), #hard for seeker : the seeker gets higher points upon winning, while the hider gets lower points upon winning 
            1: (-2, 2),   #neutral for seeker : both hider and seeker get the same amount of points upon winning
            2: (-0.5, 3)  #easy for seeker : the seeker gets lower points upon winning, and the hider gets higher points upon winning
        }
        
        for h in range(self.world_size):
            for s in range(self.world_size):
                if h == s:  # Seeker found hider
                    base = payoffs[self.place_types[h]][0]
                    if self.use_proximity:
                        distance = self.calculate_distance(h, s)
                        matrix[h, s] = base * (0.5 + 0.5*distance)  # 50-100% of penalty
                    else:
                        matrix[h, s] = base
                else:  # Seeker didn't find hider
                    base = payoffs[self.place_types[h]][1]
                    if self.use_proximity:
                        distance = self.calculate_distance(h, s)
                        matrix[h, s] = base * (1.5 - distance)  # 50-150% of reward
                    else:
                        matrix[h, s] = base
                        
        return matrix
    
    def calculate_optimal_strategies(self):
        # For hider (row player) - maximin
        # Decision variables: [x1, x2, ..., xn, v] where v is the value of the game
        c = np.zeros(self.world_size + 1)
        c[-1] = -1  # Maximize v (negate for minimization)
        
        # Constraints: x1*A_1j + x2*A_2j + ... + xn*A_nj - v ≥ 0 for all j
        A_ub = np.column_stack([-self.payoff_matrix.T, np.ones(self.world_size)])
        b_ub = np.zeros(self.world_size)
        
        # Sum of probabilities = 1, excluding v
        A_eq = np.zeros((1, self.world_size + 1))
        A_eq[0, :-1] = 1
        b_eq = np.ones(1)
        
        # All probabilities non-negative, v unconstrained
        bounds = [(0, None)] * self.world_size + [(None, None)]
        
        hider_result = linprog(
            c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
            bounds=bounds, method='highs'
        )
        
        if hider_result.success:
            self.hider_probabilities = hider_result.x[:-1]  # Exclude v
            game_value = -hider_result.fun  # The value of the game
        
        # For seeker (column player) - minimax
        # Decision variables: [y1, y2, ..., yn, u] where u is the value of the game
        c = np.zeros(self.world_size + 1)
        c[-1] = 1  # Minimize u
        
        # Constraints: A_i1*y1 + A_i2*y2 + ... + A_in*yn - u ≤ 0 for all i
        A_ub = np.column_stack([self.payoff_matrix, -np.ones(self.world_size)])
        b_ub = np.zeros(self.world_size)
        
        # Sum of probabilities = 1, excluding u
        A_eq = np.zeros((1, self.world_size + 1))
        A_eq[0, :-1] = 1
        b_eq = np.ones(1)
        
        # All probabilities non-negative, u unconstrained
        bounds = [(0, None)] * self.world_size + [(None, None)]
        
        seeker_result = linprog(
            c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
            bounds=bounds, method='highs'
        )
        
        if seeker_result.success:
            self.seeker_probabilities = seeker_result.x[:-1]  # Exclude u
            # The values should be approximately equal
            assert abs(game_value - seeker_result.fun) < 1e-6
    
    def print_strategy_debug_info(self):
        """Print debug information about strategies"""
        print("\n=== Strategy Debug Info ===")
        print("Place Types:", [['Hard','Neutral','Easy'][t] for t in self.place_types])
        print("\nPayoff Matrix (Hider's perspective):")
        for i, row in enumerate(self.payoff_matrix):
            print(f"Pos {i+1:2} ({['Hard','Neutral','Easy'][self.place_types[i]]}):", 
                  " ".join(f"{x:5.1f}" for x in row))
        
        print("\nHider Probabilities:")
        for i, p in enumerate(self.hider_probabilities):
            print(f"Pos {i+1:2}: {p:.1%}")
        
        print("\nSeeker Probabilities:")
        for i, p in enumerate(self.seeker_probabilities):
            print(f"Pos {i+1:2}: {p:.1%}")
    
    def play_round(self, human_move):
        """Play one round of the game"""
        computer_move = self.get_computer_move()
        
        if self.human_role == "hider":
            hider_pos, seeker_pos = human_move, computer_move
        else:
            hider_pos, seeker_pos = computer_move, human_move
        
        score = self.payoff_matrix[hider_pos, seeker_pos]
        self.update_scores(score, hider_pos, seeker_pos)
        
        self.rounds_played += 1
        return self.format_result(score, hider_pos, seeker_pos), hider_pos, seeker_pos
    
    def update_scores(self, score, hider_pos, seeker_pos):
        """Update scores based on game outcome"""
        if self.human_role == "hider":
            if score > 0:
                self.human_score += score
                self.human_wins += 1
            else:
                self.computer_score -= score
                self.computer_wins += 1
        else:
            if score > 0:
                self.computer_score += score
                self.computer_wins += 1
            else:
                self.human_score -= score
                self.human_wins += 1
    
    def format_result(self, score, hider_pos, seeker_pos):
        """Format the result message"""
        place_type = ['Hard', 'Neutral', 'Easy'][self.place_types[hider_pos]]
        if self.human_role == "hider":
            if score > 0:
                return f"You won! +{score:.1f} points (Hid at {hider_pos+1} [{place_type}], Computer searched at {seeker_pos+1})"
            return f"You lost! {score:.1f} points (Computer found you at {hider_pos+1} [{place_type}])"
        else:
            if score > 0:
                return f"You lost! -{score:.1f} points (Computer hid at {hider_pos+1} [{place_type}], you searched at {seeker_pos+1})"
            return f"You won! +{-score:.1f} points (Found hider at {hider_pos+1} [{place_type}])"
    
    def get_computer_move(self):
        """Get computer's move based on optimal strategy"""
        probs = self.seeker_probabilities if self.human_role == "hider" else self.hider_probabilities
        return np.random.choice(self.world_size, p=probs)
    
    def run_simulation(self, rounds=100):
        """Run automated simulation"""
        original_state = {
            'human_score': self.human_score,
            'computer_score': self.computer_score,
            'rounds_played': self.rounds_played,
            'human_wins': self.human_wins,
            'computer_wins': self.computer_wins
        }
        
        # Reset temporary state
        self.human_score = self.computer_score = 0
        self.human_wins = self.computer_wins = 0
        self.rounds_played = 0
        
        for _ in range(rounds):
            human_move = random.randint(0, self.world_size - 1)
            self.play_round(human_move)
        
        results = {
            'human_score': self.human_score,
            'computer_score': self.computer_score,
            'human_wins': self.human_wins,
            'computer_wins': self.computer_wins,
            'rounds_played': rounds
        }
        
        # Restore original state
        for key, val in original_state.items():
            setattr(self, key, val)
        
        return results
    
    def save_state(self, filename):
        """Save game state to file"""
        state = {
            'world_size': self.world_size,
            'use_proximity': self.use_proximity,
            'is_2d': self.is_2d,
            'place_types': self.place_types,
            'payoff_matrix': self.payoff_matrix.tolist(),
            'human_role': self.human_role,
            'human_score': self.human_score,
            'computer_score': self.computer_score,
            'rounds_played': self.rounds_played,
            'human_wins': self.human_wins,
            'computer_wins': self.computer_wins
        }
        
        with open(filename, 'w') as f:
            json.dump(state, f)
    
    def load_state(self, filename):
        """Load game state from file"""
        with open(filename, 'r') as f:
            state = json.load(f)
        
        self.world_size = state['world_size']
        self.use_proximity = state['use_proximity']
        self.is_2d = state['is_2d']
        self.rows = int(np.sqrt(self.world_size)) if self.is_2d else 1
        self.cols = self.world_size // self.rows if self.is_2d else self.world_size
        self.place_types = state['place_types']
        self.payoff_matrix = np.array(state['payoff_matrix'])
        self.human_role = state['human_role']
        self.human_score = state['human_score']
        self.computer_score = state['computer_score']
        self.rounds_played = state['rounds_played']
        self.human_wins = state['human_wins']
        self.computer_wins = state['computer_wins']
        
        self.calculate_optimal_strategies()


if __name__ == "__main__":
    game = HideAndSeekGame(world_size=4)
