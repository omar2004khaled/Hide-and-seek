# 🕵️ Hide and Seek – Game Theory Simulation
A Python implementation of a strategic Hide-and-Seek game that demonstrates game theory concepts, optimal strategy calculation using linear programming, and proximity-based scoring mechanics.

# 📌 Overview
This game simulates a strategic interaction between a hider and a seeker in a linear or 2D world. The goal is to explore optimal strategies using payoff matrices and linear programming, with both interactive and simulation modes.

## 🎮 Game Theory Concepts Demonstrated
1. **Zero-Sum Games**: Pure conflict between hider and seeker
2. **Mixed Strategies**: Optimal probabilistic choices
3. **Minimax Theorem**: Security strategies for both players
4. **Nash Equilibrium**: Stable strategy profiles
5. **Payoff Matrix Analysis**: Complete strategic representation
   
# 📋 Features
- **Strategic Gameplay**:
  - Zero-sum game between Hider and Seeker
  - Three location types (Hard/Neutral/Easy) with different payoffs
  - Optional proximity-based scoring (distance multipliers)

- **Optimal Strategy Calculation**:
  - Computes Nash equilibrium using linear programming
  - Minimax solutions for both players
  - Mixed strategy probability visualization

- **Game Modes**:
  - Interactive human vs computer play
  - Automated simulation mode
  - 1D or 2D game worlds
  - Save/load game states

- **Analysis Tools**:
  - Payoff matrix visualization
  - Strategy debugging output
  - Extensive simulation statistics
    
# 🎲 Core Gameplay
- Three location types with different payoffs:
  - 🏋️ Hard (-3 if found, +1 if not)
  - ⚖️ Neutral (-1 if found, +1 if not)  
  - 🧩 Easy (-1 if found, +2 if not)
- Optional proximity scoring (distance multipliers)
- Both 1D (linear) and 2D grid worlds
  
# ⚙️ Technical Features
- Optimal strategy calculation via `scipy.optimize.linprog`
- Interactive human vs computer mode
- Automated simulation system
- Game state saving/loading (JSON)
- Visual grid display (2D mode)

# 📊 Analysis Tools
- Payoff matrix visualization
- Strategy probability distributions
- Simulation statistics:
  - Win rates
  - Score differentials
  - Round-by-round logging
    
# Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yaseenasaad12/Hide-and-seek.git
2. Install dependencies:
   ```bash
   pip install numpy
   pip install scipy
   pip install tkinter
