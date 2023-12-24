import tkinter as tk
import os
import backgrounds as back
import mysql.connector
from tkinter import PhotoImage
from dotenv import load_dotenv

conn = mysql.connector.connect(host='localhost', password='MySQL1234', user='root', database='MyDB')
if conn.is_connected():
    print('Connection established...')

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # name of the app
        self.master.title("GetLife")

        #load canvas
        self.canvas = tk.Canvas(self.master, width=1000, height=700)
        self.canvas.pack_propagate(False)

        #load login widgets
        self.login()
        

    def login(self):
        
        #refresh page
        self.refresh(back.bg_login_image_path)
       # self.canvas.create_text(500, 700, anchor=tk.S,text='  Constantin Denis\nMoroiu Eric-Gabriel', fill='black')
    
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
        self.check = tk.Button(self.canvas, text="Log In", padx=50, pady=10, command=lambda: self.check_cred(e_username.get(), e_password.get()))
        self.check.pack(side="top", pady= 30)

        #exit button
        self.quit = tk.Button(self.canvas, text="EXIT", padx=50, fg="red", command=root.destroy)
        self.quit.pack(side='bottom', pady=30)


    def check_cred(self, name1, name2):
        load_dotenv()
        # Delete the previous text item if it exists, hasattr check if given text exists before attempting to delete it
        if hasattr(self.canvas, 'text') and self.canvas.text is not None:
            self.canvas.delete(self.canvas.text)

        if name1 == os.getenv('NAME') and name2 == os.getenv('PASSWORD'):
            self.main_menu()
        else:
            self.canvas.text = self.canvas.create_text(500, 455, anchor=tk.S,text='Incorrect credentials!', fill='white')
        

    def main_menu(self):
        #refresh page
        self.refresh(back.bg_main_menu_image_path)
        

        #blank character for positioning
        self.blank2 = tk.Label(self.canvas, text='', bg='black')
        self.blank2.pack(pady = 150)

        #Show Doctors
        self.print_doctors = tk.Button(self.canvas, text="Doctors", padx=50, pady=10, command=lambda: print('ok doctor!'))
        self.print_doctors.pack(side="top", pady= 15)

        #Scheduling button
        self.schedule_button = tk.Button(self.canvas, text="Schedule a meeting", padx=50, pady=10, command=lambda: print('ok meeting!'))
        self.schedule_button.pack(pady= 15)

        #Exit button
        self.quit = tk.Button(self.canvas, text="EXIT", padx=50, fg="red", command=root.destroy)
        self.quit.pack(side='bottom', pady=15)

        #logout button
        self.log_out = tk.Button(self.canvas, text='Log Out', command=lambda:self.login())
        self.log_out.pack(side='bottom')


    def refresh(self, background_name):
        #delete widgets
        for widget in self.canvas.winfo_children():
            widget.destroy()

        #import background
        self.canvas.delete("all")
        self.bg_image = PhotoImage(file=background_name)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)

#main loop
if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
