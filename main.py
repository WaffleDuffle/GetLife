import tkinter as tk
from tkinter import PhotoImage
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # name of the app
        self.master.title("GetLife")

        # generate window

        self.myframe = tk.Frame(root, width = 600, height = 800, bg = "#7bd3ea") 
        self.myframe.grid(row=0, column=0)
        self.myframe.grid_propagate(False)

        self.create_widgets()
        

    def create_widgets(self):

        #import logo
        self.myimage = PhotoImage(file = '/home/waffleduffle/Desktop/python_proj_etti/GetLife/resources/logo.png')
        self.imagelabel = tk.Label(self.myframe, image=self.myimage, bg = "#7bd3ea")
        self.imagelabel.grid(row=0, column=0, pady=50)

        self.hi_there = tk.Button(self.myframe, text="Hello World\n(click me)", fg="blue", command=self.say_hi)
        self.hi_there.grid(row=1, column=0, pady=10)
        
        self.quit = tk.Button(self.myframe, text="QUIT", fg="red", command=root.destroy)
        self.quit.grid(row=2, column=0, pady=0)

    def say_hi(self):
        self.mylabel = tk.Label(self.myframe, text="I clicked!")
        self.mylabel.grid(row=3, column=0, pady=10)
        

root = tk.Tk()
app = Application(master=root)
app.mainloop()