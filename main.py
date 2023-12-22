import tkinter as tk
import os
from tkinter import PhotoImage
from dotenv import load_dotenv

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # name of the app
        self.master.title("GetLife")

        #load background
        bg_image_path = '/home/waffleduffle/Desktop/python_proj_etti/GetLife/resources/login_background.png'
        self.bg_image = PhotoImage(file=bg_image_path)

        self.canvas = tk.Canvas(self.master, width=1000, height=700)
        self.canvas.pack()
        self.canvas.pack_propagate(False)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)

        self.login_widgets()
        

    def login_widgets(self):

        #create blank character for positioning
        self.blank = tk.Label(self.canvas, text='', bg='#cf71ff')
        self.blank.pack(pady = 125)


        #create entry for username and password

        self.username = tk.Label(self.canvas, text="Enter your username:", fg='white', bg = 'black')
        self.username.pack()
        
        e_username = tk.Entry(self.canvas)
        e_username.pack()

        self.password = tk.Label(self.canvas, text="Enter your password:", fg='white', bg = 'black')
        self.password.pack()
        
        e_password = tk.Entry(self.canvas, show="*")
        e_password.pack()

        #create button for login
        
        self.hi_there = tk.Button(self.canvas, text="Log In", padx=50, command=lambda: self.say_hi(e_username.get(), e_password.get()))
        self.hi_there.pack(side="top", pady= 30)
        
        #create button for exit
        self.quit = tk.Button(self.canvas, text="QUIT", padx=50, fg="red", command=root.destroy)
        self.quit.pack()

    def say_hi(self, name1, name2):
        load_dotenv()
        print(os.getenv('NAME'))
        print(os.getenv('PASSWORD'))
        if name1 == os.getenv('NAME') and name2 == os.getenv('PASSWORD'):
            self.mylabel = tk.Label(self.canvas, text="Correct!")
            self.mylabel.pack()
        else:
            self.mylabel = tk.Label(self.canvas, text="Incorrect!")
            self.mylabel.pack()
        
#main loop
root = tk.Tk()
app = Application(master=root)
app.mainloop()
