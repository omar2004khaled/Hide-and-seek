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
        self.payoff_matrix = self.generate_base_payoff_matrix()
        self.proximity_matrix = self.apply_proximity_effects() if self.use_proximity else self.payoff_matrix.copy()
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
        """Calculate absolute distance between positions"""
        if self.is_2d:
            x1, y1 = pos1 // self.cols, pos1 % self.cols
            x2, y2 = pos2 // self.cols, pos2 % self.cols
            return abs(x1 - x2) + abs(y1 - y2)  # Manhattan distance for 2D
        else:
            return abs(pos1 - pos2)  # Linear distance for 1D
    
    def get_proximity_multiplier(self, pos1, pos2):
        """Get proximity multiplier based on the distance between positions"""
        distance = self.calculate_distance(pos1, pos2)
        
        if distance == 1:
            return 0.5  # If one cell away, multiply by 0.5
        elif distance == 2:
            return 0.75  # If two cells away, multiply by 0.75
        else:
            return 1.0  # Otherwise, no change
    
    def generate_base_payoff_matrix(self):
        """Generate base payoff matrix without proximity effects"""
        matrix = np.zeros((self.world_size, self.world_size))
        
        # More distinct payoffs for each place type
        payoffs = {
            # (found_payoff, not_found_payoff)
            0: (-6, 0.5),  # hard for seeker
            1: (-2, 2),    # neutral for seeker
            2: (-0.5, 3)   # easy for seeker
        }
        
        for h in range(self.world_size):
            for s in range(self.world_size):
                if h == s:  # Seeker found hider
                    matrix[h, s] = payoffs[self.place_types[h]][0]
                else:  # Seeker didn't find hider
                    matrix[h, s] = payoffs[self.place_types[h]][1]
                        
        return matrix
    
    def apply_proximity_effects(self):
        """Apply proximity effects to create a separate proximity matrix (for reference only)"""
        proximity_matrix = np.zeros((self.world_size, self.world_size))
        
        for h in range(self.world_size):
            for s in range(self.world_size):
                if h == s:  # Seeker found hider - same as base matrix
                    proximity_matrix[h, s] = self.payoff_matrix[h, s]
                else:  # Apply proximity effects when seeker doesn't find hider
                    multiplier = self.get_proximity_multiplier(h, s)
                    proximity_matrix[h, s] = self.payoff_matrix[h, s] * multiplier
                    
        return proximity_matrix
    
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
        
        print("\nPayoff Matrix (Hider's perspective) - USED FOR GAME SCORING:")
        for i, row in enumerate(self.payoff_matrix):
            print(f"Pos {i+1:2} ({['Hard','Neutral','Easy'][self.place_types[i]]}):", 
                  " ".join(f"{x:5.1f}" for x in row))
        
        if self.use_proximity:
            print("\nProximity Matrix (NOT USED FOR SCORING - Reference Only):")
            for i, row in enumerate(self.proximity_matrix):
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

        base_score = self.payoff_matrix[hider_pos, seeker_pos]

        # Determine if proximity score applies
        use_proximity = self.use_proximity and hider_pos != seeker_pos
        proximity_score = self.proximity_matrix[hider_pos, seeker_pos] if use_proximity else None
        proximity_multiplier = self.get_proximity_multiplier(hider_pos, seeker_pos) if use_proximity else None

        # Pass both scores to update_scores
        self.update_scores(base_score, proximity_score)

        self.rounds_played += 1
        return self.format_result(
            base_score, hider_pos, seeker_pos, proximity_score, proximity_multiplier
        ), hider_pos, seeker_pos

    def update_scores(self, base_score, proximity_score):
        """Update scores, using proximity score if available"""
        score = proximity_score if proximity_score is not None else base_score

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

    
    def format_result(self, score, hider_pos, seeker_pos, proximity_score=None, proximity_multiplier=None):
        """Format the result message with proximity details if applicable"""
        place_type = ['Hard', 'Neutral', 'Easy'][self.place_types[hider_pos]]
        
        # Create a detailed message that explains proximity scoring if applicable
        proximity_detail = ""
        if proximity_score is not None and proximity_multiplier is not None:
            distance = self.calculate_distance(hider_pos, seeker_pos)
            proximity_detail = f" (Proximity score would be: {proximity_score:.1f}, Distance: {distance}, Multiplier: {proximity_multiplier:.2f}, but using base score)"
        
        if self.human_role == "hider":
            if score > 0:
                return f"You won! +{score:.1f} points{proximity_detail} (Hid at {hider_pos+1} [{place_type}], Computer searched at {seeker_pos+1})"
            return f"You lost! {score:.1f} points (Computer found you at {hider_pos+1} [{place_type}])"
        else:
            if score > 0:
                return f"You lost! -{score:.1f} points{proximity_detail} (Computer hid at {hider_pos+1} [{place_type}], you searched at {seeker_pos+1})"
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
            'proximity_matrix': self.proximity_matrix.tolist() if self.use_proximity else None,
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
        
        if self.use_proximity and state.get('proximity_matrix'):
            self.proximity_matrix = np.array(state['proximity_matrix'])
        else:
            self.proximity_matrix = self.apply_proximity_effects() if self.use_proximity else self.payoff_matrix.copy()
            
        self.human_role = state['human_role']
        self.human_score = state['human_score']
        self.computer_score = state['computer_score']
        self.rounds_played = state['rounds_played']
        self.human_wins = state['human_wins']
        self.computer_wins = state['computer_wins']
        
        self.calculate_optimal_strategies()


if __name__ == "__main__":
    # Example usage with proximity effects enabled
    game = HideAndSeekGame(world_size=6, use_proximity=True)
    game.human_role = "hider"
    
    # Print debug info to see the payoff matrix with proximity effects
    game.print_strategy_debug_info()
    
    # Example: Human hides at position 2 (index 1), computer searches at position 3 (index 2)
    # This should demonstrate the proximity effect you described
    human_move = 1  # Position 2
    result, hider_pos, seeker_pos = game.play_round(human_move)
    print("\nExample round result:")
    print(result)