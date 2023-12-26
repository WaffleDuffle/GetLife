import tkinter as tk
import os
import backgrounds as back
import mysql.connector
from tkinter import PhotoImage
from dotenv import load_dotenv
from PIL import Image, ImageTk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
    # name of the app
        self.master.title("GetLife")

    # load canvas
        self.canvas = tk.Canvas(self.master, width=1000, height=700)
        self.canvas.pack_propagate(False)

    # load login widgets
        self.login()
        

    def login(self):
        
    # refresh page
        self.refresh(back.bg_login_image_path)
    # self.canvas.create_text(500, 700, anchor=tk.S,text='  Constantin Denis\nMoroiu Eric-Gabriel', fill='black')
    
    # create blank character for positioning
        self.blank = tk.Label(self.canvas, text='', bg='#cf71ff')
        self.blank.pack(pady = 125)

    # create entry for username and password
        self.username = tk.Label(self.canvas, text="Enter your username:", fg='white', bg = 'black')
        self.username.pack()
        e_username = tk.Entry(self.canvas)
        e_username.pack()
        self.password = tk.Label(self.canvas, text="Enter your password:", fg='white', bg = 'black')
        self.password.pack()      
        e_password = tk.Entry(self.canvas, show="*")
        e_password.pack()

    # create button for login
        self.check = tk.Button(self.canvas, text="Log In", padx=50, pady=10, command=lambda: self.check_cred(e_username.get(), e_password.get()))
        self.check.pack(side="top", pady= 30)

    # exit button
        self.quit = tk.Button(self.canvas, text="EXIT", padx=50, fg="red", command=root.destroy)
        self.quit.pack(side='bottom', pady=30)


    def check_cred(self, name1, name2):
        load_dotenv()
    # delete the previous text item if it exists, hasattr checks if given text exists before attempting to delete it
        if hasattr(self.canvas, 'text') and self.canvas.text is not None:
            self.canvas.delete(self.canvas.text)

        if name1 == os.getenv('NAME') and name2 == os.getenv('PASSWORD'):
            self.main_menu()
        else:
            self.canvas.text = self.canvas.create_text(500, 455, anchor=tk.S,text='Incorrect credentials!', fill='white')
        

    def main_menu(self):
    # refresh page
        self.refresh(back.bg_main_menu_image_path)
        

    # blank character for positioning
        self.blank2 = tk.Label(self.canvas, text='', bg='black')
        self.blank2.pack(pady = 150)

    # show Doctors
        self.print_doctors = tk.Button(self.canvas, text="Doctors", padx=50, pady=10, command=lambda: self.doctors_menu())
        self.print_doctors.pack(side="top", pady= 15)

    # scheduling button
        self.schedule_button = tk.Button(self.canvas, text="Schedule a meeting", padx=50, pady=10, command=lambda: print('ok meeting!'))
        self.schedule_button.pack(pady= 15)

    # exit button
        self.quit = tk.Button(self.canvas, text="EXIT", padx=50, fg="red", command=root.destroy)
        self.quit.pack(side='bottom', pady=15)

    # logout button
        self.log_out = tk.Button(self.canvas, text='Log Out', command=lambda:self.login())
        self.log_out.pack(side='bottom')


    def doctors_menu(self):
    # refresh page
        self.refresh(back.bg_doc_menu_image_path)
        
    # initialize cursor in database
        self.db_cursor = conn.cursor() 
        self.db_cursor.execute("SELECT * FROM Medici")
        self.db_result = self.db_cursor.fetchall()
        self.i = 0
        

    # buttons for crossing 
        self.next_button = tk.Button(self.canvas, padx = 28, text='Next', command=lambda: self.next_doc()).pack(side=tk.RIGHT, anchor=tk.CENTER, padx=20)
        self.previous_button = tk.Button(self.canvas, text='Previous', command=lambda: self.previous_doc()).pack(side=tk.LEFT,padx=20)
        
    # return button
        self.ret = tk.Button(self.canvas, text="Return", padx=50, command=lambda:self.main_menu())
        self.ret.pack(side='bottom', pady=30)

    # print first medic
        self.print_medici()

    def next_doc(self):
        
        self.i += 1
        if self.i == len(self.db_result) or self.i < 0:
            print('OUT OF BOUNDS!!!')
            self.i = 0    
        self.print_medici()
        

    def previous_doc(self):
        self.i -= 1
        if self.i == len(self.db_result) or self.i < 0:
            print('OUT OF BOUNDS!!!')
            self.i = len(self.db_result) - 1            
        self.print_medici()
        
        
    def print_medici(self):
    # checks if image_label has been defined already
        if hasattr(self, 'image_label'):
            self.image_label.pack_forget()

        # remove old labels from the list
            for label in self.lista_date:
                label.pack_forget()

        self.image_path = '/home/waffleduffle/Desktop/python_proj_etti/GetLife/resources/' + str(self.i) + '.png'
        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)

    # create labels for image
        self.image_label = tk.Label(self.canvas, image=self.photo)
        self.image_label.pack(pady=50)

    # label list for data
        self.lista_date = []
        self.lista_date.append(tk.Label(self.canvas, text='ID: ' + str(self.db_result[self.i][0])))
        self.lista_date.append(tk.Label(self.canvas, text='Nume: ' + str(self.db_result[self.i][1])))
        self.lista_date.append(tk.Label(self.canvas, text='Specialitate: ' + str(self.db_result[self.i][2])))
        self.lista_date.append(tk.Label(self.canvas, text='Disponibilitate: ' + str(self.db_result[self.i][3])))
        self.lista_date.append(tk.Label(self.canvas, text='Contact: ' + str(self.db_result[self.i][4])))
    # label packing
        for label in self.lista_date:
            label.pack(pady=5)
        


    def refresh(self, background_name):
    # delete widgets
        for widget in self.canvas.winfo_children():
            widget.destroy()
    # import background
        self.canvas.delete("all")
        self.bg_image = PhotoImage(file=background_name)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)

# main loop
        
if __name__ == '__main__':
    root = tk.Tk()
    conn = mysql.connector.connect(
        host='localhost',
	password='MySQL1234',
	user='root',
	database='MyDB'
    )    

if conn.is_connected():
    print('Connection established...')
app = Application(master=root)
app.mainloop()
