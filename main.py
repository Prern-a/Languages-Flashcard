from tkinter import *
from tkinter import messagebox
import pandas
import random

BACKGROUND_COLOR = "#7af9ab"
current_card = {}
to_learn = {}
score = 0
instructions = """Welcome to FlashCard Generator!
This program will help you learn French words.
You will have 5 seconds to see each French word,
then its English translation will appear.
Click the green button if you know the translation,
or the red button if you don't.
Let's get started!"""

try:
    data = pandas.read_csv('data/words_to_learn.csv')
    if data.empty:
        raise ValueError("The file is empty. Loading the original dataset.")
except (FileNotFoundError, ValueError) as e:
    print(f"Error: {e}")
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

def next_card():
    global current_card, timer
    window.after_cancel(timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_bg, image=card_img)
    timer = window.after(5000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="brown")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    canvas.itemconfig(card_bg, image=card_back)

def know():
    global score
    score += 1
    score_label.config(text=f"Score: {score}")
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

def restart_game():
    global to_learn, score
    score = 0
    score_label.config(text=f"Score: {score}")
    try:
        data = pandas.read_csv('data/words_to_learn.csv')
        if data.empty:
            raise ValueError("The file is empty. Loading the original dataset.")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        original_data = pandas.read_csv("data/french_words.csv")
        to_learn = original_data.to_dict(orient="records")
    else:
        to_learn = data.to_dict(orient="records")
    next_card()

def start_program():
    messagebox.showinfo("Instructions", instructions)
    next_card()

def exit_program():
    messagebox.showinfo("Final Score", f"Your final score is: {score}")
    window.quit()
    window.destroy()

window = Tk()
window.title("FlashCard Generator")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)  # Adjust padding for better centering
window.protocol("WM_DELETE_WINDOW", exit_program)

# Center the window on the screen
window.update_idletasks()
width = window.winfo_width()
height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)
window.geometry(f'{width}x{height}+{x}+{y}')

# Ensure grid columns and rows are centered
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)

timer = window.after(5000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_img = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_bg = canvas.create_image(400, 263, image=card_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=1, column=0, columnspan=3)  # Spanning three columns for centering

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=2, column=0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=know)
right_button.grid(row=2, column=2)

score_label = Label(text="Score: 0", font=("Helvetica", 30), bg=BACKGROUND_COLOR)
score_label.grid(row=0, column=2)

menu_bar = Menu(window)
window.config(menu=menu_bar)

game_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Game", menu=game_menu)
game_menu.add_command(label="Restart", command=restart_game)
game_menu.add_separator()
game_menu.add_command(label="Instructions", command=lambda: messagebox.showinfo("Instructions", instructions))
game_menu.add_command(label="Exit", command=exit_program)

start_program()
window.mainloop()
