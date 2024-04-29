
import tkinter as tk # import tkinter for implementing the UI
from tkinter import filedialog, ttk # file dialog for address and select the file
                                    # ttk is for Progress Bar
import main # import the main code to execute

from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/glados/Documents/AmirAli Toori/Lessons/Python/IR-Project/Tkinter-Designer-master/build/assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_file():
    global entry
    dataset_path = filedialog.askopenfilename(title = "Open a file.",
                                                filetypes = [("All the file", "*.*"), ("Text Document", "*.txt")],
                                                initialdir = "/home/glados/Documents/AmirAli Toori/Lessons/Python/IR-Project")    
    with open(dataset_path, "r") as f:
        raw_dataset = f.read()
        entry = raw_dataset
        window.destroy()
        return entry


window = Tk()

window.title("Selecting file")
window.geometry("329x63")
window.configure(bg = "#D9D9D9")


canvas = Canvas(
    window,
    bg = "#D9D9D9",
    height = 63,
    width = 329,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    16.0,
    0.0,
    anchor="nw",
    text="Please select the desire file:",
    fill="#000000",
    font=("Ubuntu Mono", 12)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command= open_file,
    relief="flat"
)
button_1.place(
    x=285.0,
    y=15.4000244140625,
    width=36.0,
    height=30.799999237060547
)
window.resizable(False, False)
window.mainloop()

# run the app method in main file
main.app(entry) 