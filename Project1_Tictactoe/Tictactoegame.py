import tkinter as tk
from tkinter import messagebox
import random

PLAYER_X_COLOR = "#3498db"  # Blue (You)
PLAYER_O_COLOR = "#e74c3c"  # Red (Computer)

def check_winner():
    for combo in [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != "":
            global winner
            winner = True
            winner_name = buttons[combo[0]]["text"]
            for idx in combo:
                buttons[idx].config(bg="#2ecc71", fg="white")
            messagebox.showinfo("Tic-Tac-Toe", f"🎉 Player {winner_name} wins! 🎉")
            for i in range(9):
                buttons[i].config(state="disabled")
            label.config(text=f"Game Over - Player {winner_name} Wins! 🎉")
            return

def check_winner_condition():
    """Helper function to check if current board has a winner (without showing message)"""
    for combo in [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != "":
            return True
    return False

def button_click(index):
    if buttons[index]["text"] == "" and not winner:
        buttons[index]["text"] = current_player
        if current_player == "X":
            buttons[index].config(fg="white", bg="#3498db", disabledforeground="white")
        else:
            buttons[index].config(fg="white", bg="#e74c3c", disabledforeground="white")
        buttons[index].config(state="disabled")
        check_winner()
        check_tie()
        toggle_player()
        
        if not winner and vs_computer and current_player == "O":
            root.after(500, computer_move)

def computer_move():
    """Medium AI: Tries to win first, then blocks player, then random move"""
    global winner, current_player
    
    if not winner and current_player == "O" and vs_computer:
        empty_cells = [i for i in range(9) if buttons[i]["text"] == ""]
        
        if not empty_cells:
            return
            
        
        for move in empty_cells:
            
            buttons[move]["text"] = "O"
            if check_winner_condition():
                
                buttons[move]["text"] = ""
                
                buttons[move]["text"] = current_player
                buttons[move].config(fg="white", bg=PLAYER_O_COLOR, disabledforeground="white")
                buttons[move].config(state="disabled")
                check_winner()
                check_tie()
                toggle_player()
                return
         
            buttons[move]["text"] = ""
        
         
        for move in empty_cells:
           
            buttons[move]["text"] = "X"
            if check_winner_condition():
                
                buttons[move]["text"] = ""
                
                buttons[move]["text"] = current_player
                buttons[move].config(fg="white", bg=PLAYER_O_COLOR, disabledforeground="white")
                buttons[move].config(state="disabled")
                check_winner()
                check_tie()
                toggle_player()
                return
           
            buttons[move]["text"] = ""
        
        
        if buttons[4]["text"] == "":
            move = 4
            buttons[move]["text"] = current_player
            buttons[move].config(fg="white", bg=PLAYER_O_COLOR, disabledforeground="white")
            buttons[move].config(state="disabled")
            check_winner()
            check_tie()
            toggle_player()
            return
        
        
        corners = [0, 2, 6, 8]
        available_corners = [c for c in corners if buttons[c]["text"] == ""]
        if available_corners:
            move = random.choice(available_corners)
            buttons[move]["text"] = current_player
            buttons[move].config(fg="white", bg=PLAYER_O_COLOR, disabledforeground="white")
            buttons[move].config(state="disabled")
            check_winner()
            check_tie()
            toggle_player()
            return
        
       
        if empty_cells:
            move = random.choice(empty_cells)
            buttons[move]["text"] = current_player
            buttons[move].config(fg="white", bg=PLAYER_O_COLOR, disabledforeground="white")
            buttons[move].config(state="disabled")
            check_winner()
            check_tie()
            toggle_player()

def toggle_player():
    global current_player
    current_player = "X" if current_player == "O" else "O"
    if vs_computer and current_player == "O":
        label.config(text=f"Computer's turn 🤖 (Thinking...)")
    else:
        label.config(text=f"Player {current_player}'s turn")

def on_enter(event, index):
    if buttons[index]["text"] == "" and not winner:
        buttons[index].config(bg="#f0f0f0")

def on_leave(event, index):
    if buttons[index]["text"] == "" and not winner:
        buttons[index].config(bg="SystemButtonFace")

def check_tie():
    global winner
    if all(buttons[i]["text"] != "" for i in range(9)):
        winner = True
        messagebox.showinfo("Tic-Tac-Toe", "It's a DRAW! 🤝")
        for i in range(9):
            buttons[i].config(state="disabled")
        label.config(text="Game Over - It's a Draw! 🤝")

def reset_game():
    global current_player, winner
    current_player = "X"
    winner = False
    for i in range(9):
        buttons[i].config(text="", bg="SystemButtonFace", state="normal")
    if vs_computer:
        label.config(text="Player X's turn (You)")
    else:
        label.config(text=f"Player {current_player}'s turn")

def set_mode(mode):
    global vs_computer, current_player, winner
    vs_computer = mode
    reset_game()
    if mode:
        mode_label.config(text="🤖 VS Computer 🤖")
        label.config(text="Player X's turn (You)")
    else:
        mode_label.config(text="👥 2 Players Mode 👥")
        label.config(text="Player X's turn")

root = tk.Tk()
root.title("Tic-Tac-Toe - Medium AI")
root.configure(bg="#2c3e50")
root.resizable(False, False)
root.geometry("400x520")

buttons = [tk.Button(root, text="", font=("normal", 25), width=6, height=2, command=lambda i=i: button_click(i)) for i in range(9)]

for i, button in enumerate(buttons):
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
    button.bind("<Enter>", lambda e, idx=i: on_enter(e, idx))
    button.bind("<Leave>", lambda e, idx=i: on_leave(e, idx))

current_player = "X"
winner = False
vs_computer = False

label = tk.Label(root, text=f"Player {current_player}'s turn", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50")
label.grid(row=3, column=0, columnspan=3, pady=10)

reset_btn = tk.Button(root, text="New Game", font=("normal", 12), command=reset_game, bg="#95a5a6", fg="white")
reset_btn.grid(row=4, column=0, columnspan=3, pady=10)


mode_frame = tk.Frame(root, bg="#2c3e50")
mode_frame.grid(row=5, column=0, columnspan=3, pady=10)

btn_2player = tk.Button(mode_frame, text="👥 2 Players", font=("Arial", 10), 
                        command=lambda: set_mode(False), bg="#3498db", fg="white", width=12)
btn_2player.pack(side=tk.LEFT, padx=5)

btn_vs_computer = tk.Button(mode_frame, text="🤖 VS Computer", font=("Arial", 10), 
                           command=lambda: set_mode(True), bg="#e74c3c", fg="white", width=12)
btn_vs_computer.pack(side=tk.LEFT, padx=5)

mode_label = tk.Label(root, text="👥 2 Players Mode 👥", font=("Arial", 10), 
                      fg="white", bg="#2c3e50")
mode_label.grid(row=6, column=0, columnspan=3, pady=5)


difficulty_label = tk.Label(root, text="⭐ Computer Wins & Blocks ⭐", font=("Arial", 9), 
                            fg="#f39c12", bg="#2c3e50")
difficulty_label.grid(row=7, column=0, columnspan=3, pady=5)

root.mainloop()