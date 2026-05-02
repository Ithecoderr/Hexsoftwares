import tkinter as tk
from tkinter import messagebox

PLAYER_X_COLOR = "#3498db"  # Blue
PLAYER_O_COLOR = "#e74c3c"  # Red

def check_winner():
    for combo in [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != "":
            global winner  # ← Add this line
            winner = True  # ← Add this line
            winner_name = buttons[combo[0]]["text"]  # ← Store winner name
            # Color winning line (changed from "green" to "#2ecc71" for better color)
            for idx in combo:
                buttons[idx].config(bg="#2ecc71", fg="white")
            messagebox.showinfo("Tic-Tac-Toe", f"🎉 Player {winner_name} wins! 🎉")
            # Disable all buttons instead of closing window
            for i in range(9):
                buttons[i].config(state="disabled")
            label.config(text=f"Game Over - Player {winner_name} Wins! 🎉")
            return  # ← Exit the functio

def button_click(index):
    if buttons[index]["text"] == "" and not winner:
        buttons[index]["text"] = current_player
         # Add this block to change button colors
        if current_player == "X":
            buttons[index].config(fg="white", bg="#3498db", disabledforeground="white")
        else:
            buttons[index].config(fg="white", bg="#e74c3c", disabledforeground="white")
        buttons[index].config(state="disabled")  # Disable button after click
        check_winner()
        check_tie()  # Add this line - checks for draw after each move
        toggle_player()

def toggle_player():
    global current_player
    current_player = "X" if current_player == "O" else "O"
    label.config(text=f"Player {current_player}'s turn")

def on_enter(event, index):
    if buttons[index]["text"] == "" and not winner:
        buttons[index].config(bg="#f0f0f0")  # Light gray on hover

def on_leave(event, index):
    if buttons[index]["text"] == "" and not winner:
        buttons[index].config(bg="SystemButtonFace")  # Default color

def check_tie():
    global winner
    # Check if all buttons are filled
    if all(buttons[i]["text"] != "" for i in range(9)):
        winner = True
        messagebox.showinfo("Tic-Tac-Toe", "It's a DRAW! 🤝")
        # Don't close the window - just disable further moves
        for i in range(9):
            buttons[i].config(state="disabled")
        label.config(text="Game Over - It's a Draw! 🤝")

def reset_game():
    global current_player, winner
    current_player = "X"
    winner = False
    for i in range(9):
        buttons[i].config(text="", bg="SystemButtonFace", state="normal")
    label.config(text=f"Player {current_player}'s turn")

root = tk.Tk()
root.title("Tic-Tac-Toe")
root.configure(bg="#2c3e50")  # Dark blue background
root.resizable(False, False)  # Prevent resizing
root.geometry("400x450")  # Set window size

buttons = [tk.Button(root, text="", font=("normal", 25), width=6, height=2, command=lambda i=i: button_click(i)) for i in range (9)] 

for i, button in enumerate(buttons):
    button.grid(row=i //3, column=i % 3)
    button.bind("<Enter>", lambda e, idx=i: on_enter(e, idx))
    button.bind("<Leave>", lambda e, idx=i: on_leave(e, idx))

current_player = "X"
winner = False
label = tk.Label(root, text=f"Player {current_player}'s turn", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50")
label.grid(row=3, column=0, columnspan=3, pady=10)

# Add reset button
reset_btn = tk.Button(root, text="New Game", font=("normal", 12), command=reset_game, bg="#95a5a6", fg="white")
reset_btn.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()