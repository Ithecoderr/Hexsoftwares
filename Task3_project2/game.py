import tkinter as tk
import random

# Game settings
ROWS = 4
COLS = 4
# Fruit data with colors
FRUITS = [
    {"name": "🍎", "color": "#FF0000"},  # Red Apple
    {"name": "🍊", "color": "#FFA500"},  # Orange
    {"name": "🍌", "color": "#FFD700"},  # Yellow Banana
    {"name": "🍇", "color": "#800080"},  # Purple Grape
    {"name": "🍒", "color": "#DC143C"},  # Red Cherry
    {"name": "🥝", "color": "#8B4513"},  # Brown Kiwi
    {"name": "🍉", "color": "#32CD32"},  # Green Watermelon
    {"name": "🍓", "color": "#FF1493"}   # Pink Strawberry
]

# Create pairs of fruits
SYMBOLS = []
for fruit in FRUITS:
    SYMBOLS.append(fruit)  # First card
    SYMBOLS.append(fruit)  # Pair card

class MemoryPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Puzzle - Fruits Edition")
        self.root.configure(bg="light pink")
        
        # Set window size and center it
        window_width = 700
        window_height = 750
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.root.minsize(600, 650)
        
        self.first_card = None
        self.second_card = None
        self.lock = False
        self.moves = 0
        self.matches = 0

        random.shuffle(SYMBOLS)
        self.board = [SYMBOLS[i * COLS:(i + 1) * COLS] for i in range(ROWS)]

        self.buttons = []
        self.create_ui()

    def create_ui(self):
        # Main container
        self.main_frame = tk.Frame(self.root, bg="light pink")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title label
        self.info = tk.Label(
            self.main_frame, 
            text="MOVES: 0", 
            font=("Arial", 20, "bold"),
            bg="light pink",
            fg="#8B4513"
        )
        self.info.pack(pady=(0, 20))
        
        # Game frame
        self.game_frame = tk.Frame(self.main_frame, bg="light pink")
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for even spacing
        for i in range(ROWS):
            self.game_frame.grid_rowconfigure(i, weight=1)
        for i in range(COLS):
            self.game_frame.grid_columnconfigure(i, weight=1)
        
        # Create buttons with fixed size
        self.buttons = []
        for r in range(ROWS):
            row_buttons = []
            for c in range(COLS):
                btn = tk.Button(
                    self.game_frame,
                    text="",  # Blank button
                    font=("Segoe UI Emoji", 32),  # Fixed font size
                    bg="#FFE4E1",
                    fg="#000000",
                    activebackground="#FFB6C1",
                    relief="raised",
                    bd=4,
                    cursor="hand2",
                    width=6,  # Fixed width
                    height=3,  # Fixed height
                    command=lambda r=r, c=c: self.flip_card(r, c)
                )
                btn.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def flip_card(self, r, c):
        if self.lock:
            return

        btn = self.buttons[r][c]
        
        # Don't flip if already showing a fruit
        if btn["text"] != "":
            return

        fruit_data = self.board[r][c]
        
        # Show the fruit emoji with color (keep same font size)
        btn.configure(
            text=fruit_data["name"],
            fg=fruit_data["color"],
            bg="#FFFACD",
            relief="sunken",
            font=("Segoe UI Emoji", 32)  # Same font size
        )

        if not self.first_card:
            self.first_card = (r, c)
        else:
            self.second_card = (r, c)
            self.lock = True
            self.root.after(800, self.check_match)

    def check_match(self):
        r1, c1 = self.first_card
        r2, c2 = self.second_card
        
        fruit1 = self.board[r1][c1]
        fruit2 = self.board[r2][c2]

        if fruit1["name"] == fruit2["name"]:
            self.matches += 1
            # Keep matched cards visible
            self.buttons[r1][c1].configure(
                bg="#90EE90", 
                state="disabled", 
                relief="flat",
                font=("Segoe UI Emoji", 32)  # Keep same font
            )
            self.buttons[r2][c2].configure(
                bg="#90EE90", 
                state="disabled", 
                relief="flat",
                font=("Segoe UI Emoji", 32)  # Keep same font
            )
        else:
            # Hide unmatched cards (make them blank again)
            self.buttons[r1][c1].configure(
                text="", 
                bg="#FFE4E1", 
                relief="raised",
                font=("Segoe UI Emoji", 32)  # Keep same font
            )
            self.buttons[r2][c2].configure(
                text="", 
                bg="#FFE4E1", 
                relief="raised",
                font=("Segoe UI Emoji", 32)  # Keep same font
            )

        self.moves += 1
        self.info.config(text=f"MOVES: {self.moves}")

        self.first_card = None
        self.second_card = None
        self.lock = False

        if self.matches == (ROWS * COLS) // 2:
            self.win_game()

    def win_game(self):
        win = tk.Toplevel(self.root)
        win.title("You Win! 🎉")
        win.configure(bg="light pink")
        
        win_width = 450
        win_height = 300
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width - win_width) // 2
        y = (screen_height - win_height) // 2
        win.geometry(f'{win_width}x{win_height}+{x}+{y}')
        
        tk.Label(
            win,
            text="🎉 YOU WIN! 🎉",
            font=("Arial", 24, "bold"),
            bg="light pink",
            fg="#FF1493"
        ).pack(padx=20, pady=20)
        
        tk.Label(
            win,
            text=f"Total moves: {self.moves}",
            font=("Arial", 16, "bold"),
            bg="light pink",
            fg="#8B4513"
        ).pack(pady=10)
        
        tk.Label(
            win,
            text="🍎 🍊 🍌 🍇 🍒 🥝 🍉 🍓",
            font=("Segoe UI Emoji", 20),
            bg="light pink"
        ).pack(pady=10)
        
        tk.Button(
            win, 
            text="Play Again", 
            command=self.restart_game,
            bg="#FFB6C1",
            font=("Arial", 14, "bold"),
            width=12,
            height=1,
            cursor="hand2"
        ).pack(pady=15)
        
        tk.Button(
            win, 
            text="Close", 
            command=self.root.quit,
            bg="#FFA07A",
            font=("Arial", 11),
            width=8,
            cursor="hand2"
        ).pack()

    def restart_game(self):
        self.root.destroy()
        new_root = tk.Tk()
        new_game = MemoryPuzzle(new_root)
        new_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryPuzzle(root)
    root.mainloop()