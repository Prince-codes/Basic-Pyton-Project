#           TIC-TAC-TOE

import tkinter as tk 
from tkinter import messagebox

def check_winner():
    for combo in [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] ==buttons[combo[2]]["text"] !="":
            buttons[combo[0]].config(bg="green")
            buttons[combo[1]].config(bg="green")
            buttons[combo[2]].config(bg="green")
            messagebox.showinfo("Tic-Tac-Toe",f"Player {buttons[combo[0]]['text']} wins! ")
            root.destroy()
            return 2
         
            
        elif all(button["text"] != "" for button in buttons):
            label.config(text="")
            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
            root.destroy()
            break

           
            
def button_click(index):
    if buttons[index]["text"]=="" and not winner:
        buttons[index]["text"] =current_player
        toggle_player()
        if check_winner() == 2:
            pass
        else:
            pass    
def toggle_player():
    global current_player
    current_player = "X" if current_player == "O" else "O"
    label.config(text=f"Player {current_player}'s turn")
    
def exit_game():
    root.quit()


root = tk.Tk()
root.title("TIC-TAC-TOE")

buttons = [tk.Button(root, text="", font=("narmal,25"), width=6, height= 2, command=lambda i=i: button_click(i)) for i in range(9)]

for i, button in enumerate(buttons):
    button.grid(row=i //3, column=i%3)

current_player = "X"
winner = False


label= tk.Label(root, text=f"Player {current_player}'s turn", font=("normal", 16))
label.grid(row=3, column=0, columnspan=3)

#Exit button
exit_button = tk.Button(root, text="Exit", font=("normal", 16), command=exit_game)
exit_button.grid(row=4, column=0, columnspan=3)

root.mainloop()