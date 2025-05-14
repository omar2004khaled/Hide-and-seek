import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import os

from main import HideAndSeekGame


class HideAndSeekGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hide and Seek Game - Game Theory Implementation")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configure style with modern colors
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        self.game = None
        self.create_setup_frame()
        
        # Load icons if available
        self.icons = self.load_icons()
    
    def configure_styles(self):
        """Configure GUI styles with modern colors"""
        # Color palette
        bg_color = '#f8f9fa'
        primary_color = '#4e73df'
        secondary_color = '#858796'
        success_color = '#1cc88a'
        info_color = '#36b9cc'
        warning_color = '#f6c23e'
        danger_color = '#e74a3b'
        dark_color = '#5a5c69'
        
        # Configure standard styles first
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TLabel', background=bg_color, font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), foreground=dark_color)
        self.style.configure('TButton', font=('Segoe UI', 10))
        self.style.configure('TCombobox', font=('Segoe UI', 10))
        self.style.configure('TRadiobutton', background=bg_color, font=('Segoe UI', 10))
        self.style.configure('TNotebook', background=bg_color)
        self.style.configure('TEntry', font=('Segoe UI', 10))
        self.style.configure('TSpinbox', font=('Segoe UI', 10))
        
        # Configure LabelFrame - fix for the error
        self.style.configure('TLabelframe', background=bg_color, font=('Segoe UI', 11, 'bold'), foreground=dark_color)
        self.style.configure('TLabelframe.Label', background=bg_color, font=('Segoe UI', 11, 'bold'), foreground=dark_color)
        
        # Configure Tab style
        self.style.configure('TNotebook.Tab', background=secondary_color, foreground='white', padding=[15, 5], font=('Segoe UI', 10))
        self.style.map('TNotebook.Tab', background=[('selected', primary_color)])
        
        # Custom button styles
        self.style.configure('Game.TButton', font=('Segoe UI', 11, 'bold'))
        self.style.map('Game.TButton', foreground=[('!disabled', 'white')], background=[('!disabled', primary_color)])
        
        self.style.configure('Primary.TButton', font=('Segoe UI', 10))
        self.style.map('Primary.TButton', foreground=[('!disabled', 'white')], background=[('!disabled', primary_color)])
        
        self.style.configure('Success.TButton', font=('Segoe UI', 10))
        self.style.map('Success.TButton', foreground=[('!disabled', 'white')], background=[('!disabled', success_color)])
        
        self.style.configure('Info.TButton', font=('Segoe UI', 10))
        self.style.map('Info.TButton', foreground=[('!disabled', 'white')], background=[('!disabled', info_color)])
        
        self.style.configure('Warning.TButton', font=('Segoe UI', 10))
        self.style.map('Warning.TButton', foreground=[('!disabled', 'white')], background=[('!disabled', warning_color)])
        
        self.style.configure('Danger.TButton', font=('Segoe UI', 10))
        self.style.map('Danger.TButton', foreground=[('!disabled', 'white')], background=[('!disabled', danger_color)])
        
        # Configure the root window background
        self.root.configure(background=bg_color)
    
    def load_icons(self):
        """Load icons for the GUI"""
        icons = {}
        icon_paths = {
            'save': 'icons/save.png',
            'load': 'icons/open.png',
            'reset': 'icons/reset.png',
            'simulate': 'icons/simulate.png',
            'new': 'icons/new.png'
        }
        
        for name, path in icon_paths.items():
            try:
                if os.path.exists(path):
                    img = Image.open(path)
                    img = img.resize((20, 20), Image.Resampling.LANCZOS)
                    icons[name] = ImageTk.PhotoImage(img)
            except:
                pass
        
        return icons
    
    def create_setup_frame(self):
        """Create initial game setup frame with modern styling"""
        self.clear_frame()
        
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding=(30, 20))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with accent color
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 30))
        ttk.Label(header, text="Hide and Seek Game", style='Header.TLabel').pack()
        
        # Configuration panel with card-like appearance - FIXED: Use TLabelframe instead of TLabelFrame
        config_frame = ttk.LabelFrame(main_frame, text="Game Configuration", padding=20)
        config_frame.pack(fill=tk.X, pady=10, ipady=10)
        
        # World type selection
        self.type_frame = ttk.Frame(config_frame)
        self.type_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(self.type_frame, text="World Type:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        self.dim_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.type_frame, text="2D Grid", variable=self.dim_var, 
                       command=self.update_grid_options, style='TRadiobutton').pack(side=tk.LEFT, padx=15)
        
        # Grid size frame
        self.grid_frame = ttk.Frame(config_frame)
        self.grid_frame.pack(fill=tk.X, pady=5)
        ttk.Label(self.grid_frame, text="Grid Size:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        
        self.grid_size_var = tk.StringVar(value="4x4")
        grid_entry = ttk.Entry(self.grid_frame, textvariable=self.grid_size_var, width=8, font=('Segoe UI', 10))
        grid_entry.pack(side=tk.LEFT, padx=10)
        
        # Linear size frame (initially hidden)
        self.linear_frame = ttk.Frame(config_frame)
        ttk.Label(self.linear_frame, text="World Size:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        self.linear_size_var = tk.IntVar(value=4)
        ttk.Spinbox(self.linear_frame, from_=4, to=36, textvariable=self.linear_size_var, 
                   width=5, font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=10)
        
        # Set default
        self.update_grid_options()
        
        # Game options
        opt_frame = ttk.Frame(config_frame)
        opt_frame.pack(fill=tk.X, pady=15)
        ttk.Label(opt_frame, text="Game Options:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        self.prox_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(opt_frame, text="Proximity Scoring", variable=self.prox_var, 
                       style='TRadiobutton').pack(side=tk.LEFT, padx=15)
        
        # Player role selection with card styling - FIXED: Use LabelFrame without style
        role_frame = ttk.LabelFrame(config_frame, text="Player Role", padding=15)
        role_frame.pack(fill=tk.X, pady=15)
        
        self.role_var = tk.StringVar(value="hider")
        ttk.Radiobutton(role_frame, text="Hider", variable=self.role_var, value="hider",
                        style='TRadiobutton').pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(role_frame, text="Seeker", variable=self.role_var, value="seeker",
                        style='TRadiobutton').pack(side=tk.LEFT, padx=15)
        
        # Action buttons with consistent styling
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        start_btn = ttk.Button(btn_frame, text="Start Game", style='Game.TButton', 
                              command=self.start_game)
        start_btn.pack(side=tk.LEFT, padx=10, ipady=8, ipadx=15)
        
        # Add load game button if save files exist
        if os.path.exists('saves'):
            load_btn = ttk.Button(btn_frame, text="Load Game", style='Info.TButton',
                                command=self.load_game_dialog)
            load_btn.pack(side=tk.LEFT, padx=10, ipady=5, ipadx=15)
    
    def update_grid_options(self):
        if self.dim_var.get():  # 2D mode
            self.linear_frame.pack_forget()
            self.grid_frame.pack(fill=tk.X, pady=5 , after=self.type_frame)
        else:                   # 1D mode
            self.grid_frame.pack_forget()
            self.linear_frame.pack(fill=tk.X, pady=5 , after=self.type_frame)
    
    def get_world_size(self):
        """Get world size based on current settings"""
        if self.dim_var.get():  # 2D mode
            grid_size = self.grid_size_var.get()
            rows, cols = map(int, grid_size.split('x'))
            return rows * cols
        else:  # 1D mode
            return self.linear_size_var.get()
    
    def get_grid_dimensions(self):
        """Get grid dimensions for 2D mode"""
        if self.dim_var.get():
            grid_size = self.grid_size_var.get()
            rows, cols = map(int, grid_size.split('x'))
            return rows, cols
        else:
            # For 1D, treat as Nx1 grid
            return self.linear_size_var.get(), 1
    
    def start_game(self):
            """Initialize game with selected parameters"""
            
            try:
                is_2d = self.dim_var.get()

                # Validate and get world size
                if is_2d:
                    grid_size = self.grid_size_var.get()
                    if(grid_size.count('x') != 1 ):
                            raise ValueError("Invalid grid size format. Use 'NxN' (e.g., 4x4).")
                    try:
                        rows, cols = map(int, grid_size.lower().split('x'))
                        if rows < 2 or cols < 2:
                            raise ValueError("Grid dimensions must be at least 2x2.")
                        if rows != cols:
                            raise ValueError("Grid must be square (e.g., 4x4).")
                        
                    except ValueError as e:
                        # This will catch both our custom errors and conversion errors
                        raise ValueError(str(e))
                    world_size = rows * cols
                else:
                    world_size = self.get_world_size()
                    if world_size < 2:
                        raise ValueError("World size must be at least 2.")

                # Initialize game
                self.game = HideAndSeekGame(
                    world_size=world_size,
                    use_proximity=self.prox_var.get(),
                    is_2d=is_2d
            )

            # If 2D mode, set grid dimensions
                if is_2d:
                    self.game.rows = rows
                    self.game.cols = cols

                self.game.human_role = self.role_var.get()
                self.create_game_interface()

            # Print debug info to console
                self.game.print_strategy_debug_info()

            except ValueError as e:
                messagebox.showerror("Configuration Error", str(e))
            
    def is_perfect_square(self, n):
        """Check if a number is a perfect square"""
        return int(np.sqrt(n)) ** 2 == n
    
    def create_game_interface(self):
        """Create the main game interface"""
        self.clear_frame()
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top panel - Game info and controls
        top_panel = ttk.Frame(main_frame)
        top_panel.pack(fill=tk.X, pady=(0, 10))
        
        # Game info
        info_frame = ttk.Frame(top_panel)
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Show world type and dimensions
        if self.game.is_2d:
            world_text = f"World: 2D Grid ({self.game.rows}x{self.game.cols})"
        else:
            world_text = f"World: 1D Linear ({self.game.world_size} positions)"
        ttk.Label(info_frame, text=world_text, font=('Arial', 11)).pack(anchor=tk.W)
        
        # Show proximity setting
        prox_text = "Proximity Scoring: Enabled" if self.game.use_proximity else "Proximity Scoring: Disabled"
        ttk.Label(info_frame, text=prox_text, font=('Arial', 11)).pack(anchor=tk.W)
        
        role_text = "Hider" if self.game.human_role == "hider" else "Seeker"
        ttk.Label(info_frame, text=f"Role: {role_text}", font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        
        self.score_label = ttk.Label(info_frame, 
                                   text=f"Score: You {self.game.human_score} - Computer {self.game.computer_score}",
                                   font=('Arial', 11))
        self.score_label.pack(anchor=tk.W)
        
        self.rounds_label = ttk.Label(info_frame, 
                                     text=f"Rounds: {self.game.rounds_played} (Wins: You {self.game.human_wins} - Computer {self.game.computer_wins})",
                                     font=('Arial', 11))
        self.rounds_label.pack(anchor=tk.W)
        
        # Action buttons
        btn_frame = ttk.Frame(top_panel)
        btn_frame.pack(side=tk.RIGHT)
        
        button_config = [
            ("New Game", self.create_setup_frame, 'new'),
            ("Reset", self.reset_game, 'reset'),
            ("Simulate", self.run_simulation, 'simulate'),
            ("Save", self.save_game, 'save'),
            ("Load", self.load_game_dialog, 'load')
        ]
        
        for text, command, icon_key in button_config:
            icon = self.icons.get(icon_key)
            if icon:
                btn = ttk.Button(btn_frame, text=text, image=icon, compound=tk.LEFT, command=command)
            else:
                btn = ttk.Button(btn_frame, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Visualization panel
        viz_frame = ttk.Frame(main_frame)
        viz_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for multiple views
        self.notebook = ttk.Notebook(viz_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # World view tab
        world_tab = ttk.Frame(self.notebook)
        self.notebook.add(world_tab, text="World View")
        self.create_world_visualization(world_tab)
        
        # Matrix view tab
        matrix_tab = ttk.Frame(self.notebook)
        self.notebook.add(matrix_tab, text="Payoff Matrix")
        self.create_matrix_visualization(matrix_tab)
        
        # Strategies tab
        strategy_tab = ttk.Frame(self.notebook)
        self.notebook.add(strategy_tab, text="Optimal Strategies")
        self.create_strategy_visualization(strategy_tab)
        
        # Game controls
        ctrl_frame = ttk.Frame(main_frame)
        ctrl_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Move selection
        move_frame = ttk.Frame(ctrl_frame)
        move_frame.pack(side=tk.LEFT, padx=10)
        
        # Move label based on game type
        if self.game.is_2d:
            ttk.Label(move_frame, text="Your Position:").pack(side=tk.LEFT)
        else:
            ttk.Label(move_frame, text="Your Move:").pack(side=tk.LEFT)
        
        self.move_var = tk.StringVar()
        moves = [str(i+1) for i in range(self.game.world_size)]
        move_combo = ttk.Combobox(move_frame, textvariable=self.move_var, values=moves, state="readonly")
        move_combo.current(0)
        move_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(move_frame, text="Submit", command=self.make_move).pack(side=tk.LEFT)
        
        # Result display
        self.result_var = tk.StringVar(value="Make your move!")
        ttk.Label(ctrl_frame, textvariable=self.result_var, font=('Arial', 11, 'italic')).pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def create_world_visualization(self, parent):
        """Create visualization of the game world"""
        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        if self.game.is_2d:
            # 2D grid visualization
            rows = self.game.rows
            cols = self.game.cols
            
            place_colors = ['red', 'gray', 'green']  # Hard, Neutral, Easy
            place_labels = ['Hard', 'Neutral', 'Easy']
            
            for i in range(self.game.world_size):
                row = i // cols
                col = i % cols
                ax.add_patch(plt.Rectangle((col, row), 1, 1, 
                              color=place_colors[self.game.place_types[i]], alpha=0.7))
                ax.text(col + 0.5, row + 0.5, str(i+1), 
                        ha='center', va='center', fontsize=10)
            
            ax.set_xlim(0, cols)
            ax.set_ylim(0, rows)
            ax.set_xticks(np.arange(cols) + 0.5)
            ax.set_yticks(np.arange(rows) + 0.5)
            ax.set_xticklabels(range(1, cols + 1))
            ax.set_yticklabels(range(1, rows + 1))
            ax.grid(True, color='white', linestyle='-', linewidth=1)
            ax.set_title("2D Game World")
        else:
            # 1D linear visualization
            place_colors = ['red', 'gray', 'green']
            for i in range(self.game.world_size):
                ax.bar(i, 1, color=place_colors[self.game.place_types[i]], alpha=0.7)
                ax.text(i, 0.5, str(i+1), ha='center', va='center', fontsize=10)
            
            ax.set_xlim(-0.5, self.game.world_size - 0.5)
            ax.set_ylim(0, 1)
            ax.set_xticks(range(self.game.world_size))
            ax.set_xticklabels([str(i+1) for i in range(self.game.world_size)])
            ax.set_yticks([])
            ax.set_title("1D Game World")
        
        # Add legend
        handles = [plt.Rectangle((0, 0), 1, 1, color=place_colors[i]) for i in range(3)]
        ax.legend(handles, ['Hard', 'Neutral', 'Easy'], loc='upper right')
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_matrix_visualization(self, parent):
        """Create visualization of the payoff matrix"""
        fig = plt.Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Create heatmap
        cax = ax.matshow(self.game.payoff_matrix, cmap="RdYlGn", aspect='auto')
        fig.colorbar(cax, label='Payoff Value')
        
        # Add annotations
        for i in range(self.game.world_size):
            for j in range(self.game.world_size):
                ax.text(j, i, f"{self.game.payoff_matrix[i, j]:.1f}", 
                        ha='center', va='center', 
                        color='black' if abs(self.game.payoff_matrix[i, j]) < 2 else 'white')
        
        # Formatting
        ax.set_title("Payoff Matrix (Hider's Perspective)")
        ax.set_xlabel("Seeker Position")
        ax.set_ylabel("Hider Position")
        ax.set_xticks(range(self.game.world_size))
        ax.set_yticks(range(self.game.world_size))
        ax.set_xticklabels([str(i+1) for i in range(self.game.world_size)])
        ax.set_yticklabels([str(i+1) for i in range(self.game.world_size)])
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_strategy_visualization(self, parent):
        """Create visualization of optimal strategies"""
        fig = plt.Figure(figsize=(10, 5), dpi=100)
        
        # Calculate significance threshold (hide very small probabilities)
        threshold = 0.5 / self.game.world_size
        
        for i, (probs, title, color) in enumerate(zip(
            [self.game.hider_probabilities, self.game.seeker_probabilities],
            ["Hider's Optimal Strategy", "Seeker's Optimal Strategy"],
            ['blue', 'green']
        )):
            ax = fig.add_subplot(1, 2, i+1)

            if self.game.is_2d:
                # 2D grid visualization of strategy
                rows = self.game.rows
                cols = self.game.cols
                strategy_grid = np.zeros((rows, cols))
                
                for pos in range(self.game.world_size):
                    row = pos // cols
                    col = pos % cols
                    strategy_grid[row, col] = probs[pos]
                
                im = ax.imshow(strategy_grid, cmap='Blues' if i == 0 else 'Greens', 
                              vmin=0, vmax=max(probs)*1.2)
                
                # Add text annotations for significant probabilities
                for row in range(rows):
                    for col in range(cols):
                        pos = row * cols + col
                        if probs[pos] > threshold:
                            ax.text(col, row, f'{probs[pos]:.1%}', 
                                   ha='center', va='center', 
                                   color='black' if probs[pos] < 0.5 else 'white')
                
                # Add grid
                for row in range(rows):
                    for col in range(cols):
                        ax.add_patch(plt.Rectangle((col-0.5, row-0.5), 1, 1, fill=False, 
                                                 edgecolor='black', linewidth=0.5))
                
                ax.set_xticks(range(cols))
                ax.set_yticks(range(rows))
                ax.set_xticklabels(range(1, cols+1))
                ax.set_yticklabels(range(1, rows+1))
                ax.invert_yaxis()
                
                # Add colorbar
                cbar = fig.colorbar(im, ax=ax, label='Probability')

            else: 
                bars = ax.bar(range(1, self.game.world_size + 1), probs, color=color, alpha=0.7)
                
                # Add labels for significant probabilities
                for bar in bars:
                    height = bar.get_height()
                    if height > threshold:
                        ax.text(bar.get_x() + bar.get_width()/2, height,
                            f'{height:.1%}',
                            ha='center', va='bottom', fontsize=9)
                        
                ax.set_xticks(range(1, self.game.world_size + 1))
                ax.set_ylim(0, max(probs)*1.2)        
            

            ax.set_title(title, pad=15)
            ax.set_xlabel("Position", labelpad=10)
            if not self.game.is_2d:
                ax.set_ylabel("Probability", labelpad=10)

        
        fig.tight_layout(pad=3.0)
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def make_move(self):
        """Handle player's move"""
        try:
            human_move = int(self.move_var.get()) - 1
            if not 0 <= human_move < self.game.world_size:
                raise ValueError("Invalid position selected")
            
            result, hider_pos, seeker_pos = self.game.play_round(human_move)
            self.result_var.set(result.split("(")[0].strip())  # Show brief result
            
            # Update displays
            self.update_displays()
            
            # Show detailed result in dialog
            self.show_move_result(result, hider_pos, seeker_pos)
            
        except ValueError as e:
            messagebox.showerror("Invalid Move", str(e))
    
    def update_displays(self):
        """Update all information displays"""
        self.score_label.config(
            text=f"Score: You {self.game.human_score} - Computer {self.game.computer_score}"
        )
        self.rounds_label.config(
            text=f"Rounds: {self.game.rounds_played} (Wins: You {self.game.human_wins} - Computer {self.game.computer_wins})"
        )
    
    def show_move_result(self, result, hider_pos, seeker_pos):
        """Show detailed move result in dialog"""
        messagebox.showinfo("Round Result", result)
    
    def run_simulation(self):
        """Run and display simulation results"""
        confirm = messagebox.askyesno(
            "Run Simulation",
            "Run 100 rounds of simulation with random moves?\n\n"
            "This will temporarily reset scores for the simulation only."
        )
        
        if not confirm:
            return
        
        results = self.game.run_simulation(100)
        
        message = (
            f"Simulation Results (100 rounds):\n\n"
            f"Your role: {'Hider' if self.game.human_role == 'hider' else 'Seeker'}\n"
            f"Final scores:\n"
            f"  You: {results['human_score']}\n"
            f"  Computer: {results['computer_score']}\n\n"
            f"Wins:\n"
            f"  You: {results['human_wins']}\n"
            f"  Computer: {results['computer_wins']}\n\n"
            f"Win rate: {results['human_wins'] / results['rounds_played'] * 100:.1f}%"
        )
        
        messagebox.showinfo("Simulation Complete", message)
    
    def reset_game(self):
        """Reset the current game"""
        if self.game:
            self.game.reset_game()
            self.create_game_interface()
            messagebox.showinfo("Game Reset", "Game has been reset to initial state")
    
    def save_game(self):
        """Save current game state"""
        if not self.game:
            messagebox.showerror("Error", "No game to save")
            return
        
        # Create saves directory if it doesn't exist
        if not os.path.exists('saves'):
            os.makedirs('saves')
        
        filename = filedialog.asksaveasfilename(
            initialdir='saves',
            title="Save Game",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        
        if filename:
            try:
                self.game.save_state(filename)
                messagebox.showinfo("Game Saved", f"Game successfully saved to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save game:\n{str(e)}")
    
    def load_game_dialog(self):
        """Show dialog to load a saved game"""
        filename = filedialog.askopenfilename(
            initialdir='saves',
            title="Load Game",
            filetypes=[("JSON files", "*.json")]
        )
        
        if filename:
            self.load_game(filename)
    
    def load_game(self, filename):
        """Load game from file"""
        try:
            if not self.game:
                self.game = HideAndSeekGame(4)  # Temporary instance
            
            self.game.load_state(filename)
            self.create_game_interface()
            messagebox.showinfo("Game Loaded", f"Successfully loaded game from:\n{filename}")
            
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load game:\n{str(e)}")
    
    def clear_frame(self):
        """Clear all widgets from root"""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HideAndSeekGUI(root)
    root.mainloop()
