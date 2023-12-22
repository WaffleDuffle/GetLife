import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("GetLife") # name of the app
        self.myframe = tk.Frame(root, width = 750, height = 600, bg = "#7bd3ea").grid(row=0, column=0).grid_propagate(False) # generate window
        
        self.create_widgets()
        

    def create_widgets(self):
        
        
        #create label of spaces to center buttons
        self.spacelabel = tk.Label(self.myframe, text="                                                                                "
                                   , bg="#7bd3ea")
        self.spacelabel.grid(row=0, column=0)

        self.hi_there = tk.Button(self.myframe, text="Hello World\n(click me)", fg="blue", command=self.say_hi)
        self.hi_there.grid(row=1, column=1, pady=10)
        
        self.quit = tk.Button(self.myframe, text="QUIT", fg="red", command=root.destroy)
        self.quit.grid(row=2, column=1, pady=10)

    def say_hi(self):
        self.mylabel = tk.Label(self.myframe, text="I clicked!")
        self.mylabel.grid(row=3, column=1, pady=10)
        

root = tk.Tk()
app = Application(master=root)
app.mainloop()