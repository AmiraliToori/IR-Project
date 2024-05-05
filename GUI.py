
import tkinter as tk # import tkinter for implementing the UI
from tkinter import filedialog, ttk # file dialog for address and select the file
                                    # ttk is for Progress Bar
from icecream import ic # type: ignore
from pathlib import Path
import time

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

def select_file():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"/home/glados/Documents/AmirAli Toori/Lessons/Python/IR-Project/Tkinter-Designer-master/build/assets/frame0")


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def open_file():
        global entry
        dataset_path = filedialog.askopenfilename(title = "Open a file.",
                                                    filetypes = [("All the file", "*.*")],
                                                    initialdir = "/home/glados/Documents/AmirAli Toori/Lessons/Python/IR-Project")    
        with open(dataset_path, "r") as f:
            raw_dataset = f.read()
            entry = raw_dataset
            window.destroy()

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
    
    return entry


# def extract_the_docs(path):
    
#     window = tk.Tk()
#     window.geometry("900x35")
#     window.title("Extract the documents")
    
#     path_variable = tk.StringVar(window, f"Extracting the docs in to the {path}.")
    
#     label = tk.Label(window, textvariable = path_variable, font = ["Ubuntu Mono", 12])
#     label.pack()
    
#     window.resizable(False, False)
#     window.mainloop()

def custom_window(size, title, text):
    window = tk.Tk()
    window.geometry(size)
    window.title(title)
    
    label = tk.Label(window, text = text, font = ("Ubuntu Mono", 12))
    label.pack()
    
    window.after(5000, lambda:window.destroy())
    window.mainloop()




