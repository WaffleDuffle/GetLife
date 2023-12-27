import tkinter as tk
import os
import backgrounds as back
import mysql.connector
import time
from plyer import notification
from tkinter import PhotoImage
from tkinter import ttk
from tkcalendar import Calendar
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

    # load witgets for first page
        self.first_page()
        
    
    def first_page(self):
    # define cursor for pacienti and medici tables
        self.db_cursor_pacienti = conn.cursor()
        self.db_cursor_medici = conn.cursor()
        self.db_cursor_programari = conn.cursor()

    # refresh page
        self.refresh(back.bg_login_image_path)

    # create blank character for positioning
        self.blank = tk.Label(self.canvas, text='', bg='#cf71ff')
        self.blank.pack(pady = 155)

    # load exit button
        self.quit = tk.Button(self.canvas, text="EXIT", padx=50, fg="red", command=root.destroy)
        self.quit.pack(side='bottom', pady=30)

    # load login widgets
        self.login_button = tk.Button(self.canvas, text='Sign In', padx=50, pady=10, command=lambda:self.login())
        self.login_button.pack(side='top')
    
    # load register widgets
        self.register_button = tk.Button(self.canvas, text='Sign Up', padx=47, pady=10, command=lambda:self.sign_up())
        self.register_button.pack(side='top', pady=30)

    def login(self):
    
    # refresh page
        self.refresh(back.bg_login_image_path)
    # self.canvas.create_text(500, 700, anchor=tk.S,text='  Constantin Denis\nMoroiu Eric-Gabriel', fill='black')

    # create blank character for positioning
        self.blank = tk.Label(self.canvas, text='', bg='#cf71ff')
        self.blank.pack(pady = 132)

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

    # return button
        self.ret = tk.Button(self.canvas, text="Return", padx=50, command=lambda:self.first_page())
        self.ret.pack(side='bottom')


    def check_cred(self, name1, name2):
        load_dotenv()
    # delete the previous text item if it exists, hasattr checks if given text exists before attempting to delete it
        if hasattr(self.canvas, 'text') and self.canvas.text is not None:
            self.canvas.delete(self.canvas.text)
        
        ok = 0

        if name1 == os.getenv('NAME') and name2 == os.getenv('PASSWORD'):
            self.main_menu('admin')
        else:
            ok += 1

        self.db_cursor_pacienti.execute("SELECT * FROM Pacienti WHERE Username = %s AND Parola = %s", (name1, name2))
        self.result_pacienti = self.db_cursor_pacienti.fetchone()
        if self.result_pacienti:
            self.main_menu(self.result_pacienti[6]) # username column for pacienti
        else:
            ok += 1

        self.db_cursor_medici.execute("SELECT * FROM Medici WHERE Username = %s AND Parola = %s", (name1, name2))
        self.result_medici = self.db_cursor_medici.fetchone()
        if self.result_medici:
            self.main_menu('Dr. ' + self.result_medici[1]) #name column for medici
        else:
            ok += 1
        
        if ok == 3:
            self.canvas.text = self.canvas.create_text(500, 465, anchor=tk.S,text='Incorrect credentials!', fill='white')
            

    def sign_up(self):
    # refresh page
        self.refresh(back.bg_doc_menu_image_path)
    
    # create blank character for positioning
        self.blank = tk.Label(self.canvas, text='', bg='black')
        self.blank.pack(pady = 50)

    #create entry for data
        self.register_list = []
        self.create_entry_register("Enter your username:")
        self.create_entry_register("Enter your password:")
        self.create_entry_register("Enter your ID:")
        self.create_entry_register("Enter your name:")
        self.create_entry_register("Enter your surname:")
        self.create_entry_register("Enter your contact:")
        self.create_entry_register("Enter your medical history:")

    # create button for register
        self.sign = tk.Button(self.canvas, text="Sign Up", padx=50, pady=10, command=lambda:self.create_account())
        self.sign.pack(side="top", pady= 30)

    # exit button
        self.quit = tk.Button(self.canvas, text="EXIT", padx=50, fg="red", command=root.destroy)
        self.quit.pack(side='bottom', pady=30)
    
    # return button
        self.ret = tk.Button(self.canvas, text="Return", padx=50, command=lambda:self.first_page())
        self.ret.pack(side='bottom')

    def create_account(self):
        user_data = []

        for entry_data in self.register_list:
            user_data.append(entry_data.get())

         
        try:
            self.db_cursor_pacienti.execute('INSERT INTO Pacienti (PacientID, Nume, prenume, DetaliiContact, AntecedenteMedicale, Parola, Username) VALUES ('
                                            + user_data[2] + ','
                                            + "'" + user_data[3] + "'" + ','
                                            + "'" + user_data[4] + "'" + ','
                                            + "'" + user_data[5] + "'" + ','
                                            + "'" + user_data[6] + "'" + ','
                                            + "'" + user_data[1] + "'" + ','
                                            + "'" + user_data[0] + "'" + ')') # register widgets order doesn't correspond to database columns orders, I know
            conn.commit()
            print('Account created')
            self.login()
        except:
            if hasattr(self.canvas, 'text'):
                self.canvas.delete(self.canvas.text)    
            self.canvas.text = self.canvas.create_text(500, 525, anchor=tk.S,text='Blank fiedls or already used ID', fill='red')
        
        

    def create_entry_register(self, label_text):

        label = tk.Label(self.canvas, text=label_text, fg='white', bg='black')
        label.pack()
        if label_text == 'Enter your password:':
            entry = tk.Entry(self.canvas, show='*')
        else:
            entry = tk.Entry(self.canvas)
        entry.pack()
        self.register_list.append(entry)
        

    def main_menu(self, account_name):
        
    # refresh page
        self.refresh(back.bg_main_menu_image_path)
        
    # show what account is logged in
        self.canvas.account_text = self.canvas.create_text(5, 695, anchor=tk.SW,text='Logged in as: ' + account_name, font=12)

    # blank character for positioning
        self.blank2 = tk.Label(self.canvas, text='', bg='black')
        self.blank2.pack(pady = 132)

    # show Doctors
        self.print_doctors = tk.Button(self.canvas, text="Doctors", padx=50, pady=10, command=lambda: self.doctors_menu(account_name))
        self.print_doctors.pack(side="top", pady= 15)

    # scheduling button
        self.schedule_button = tk.Button(self.canvas, text="Schedule a meeting", padx=50, pady=10, command=lambda: self.meeting_scheduling(account_name))
        self.schedule_button.pack(pady= 15)

    #refresh button
        self.refresh_button = tk.Button(self.canvas, text="Refresh", command=lambda:self.main_menu(account_name))
        self.refresh_button.pack(side='bottom', anchor='se')    

    # exit button
        self.quit = tk.Button(self.canvas, text="EXIT", padx=50, fg="red", command=root.destroy)
        self.quit.pack(side='bottom', pady=30)

    

    # logout button
        self.log_out = tk.Button(self.canvas, text='Log Out', command=lambda:self.login())
        self.log_out.pack(side='bottom')


    def doctors_menu(self, account_name):
    # refresh page
        self.refresh(back.bg_doc_menu_image_path)
        
    # show what account is logged in
        self.canvas.account_text = self.canvas.create_text(5, 695, anchor=tk.SW,text='Logged in as: ' + account_name, font=12)

    # initialize cursor in database
        self.db_cursor_medici = conn.cursor() 
        self.db_cursor_medici.execute("SELECT * FROM Medici")
        self.db_result = self.db_cursor_medici.fetchall()
        self.i = 0
        

    # buttons for crossing 
        self.next_button = tk.Button(self.canvas, padx = 28, text='Next', command=lambda: self.next_doc()).pack(side=tk.RIGHT, anchor=tk.CENTER, padx=20)
        self.previous_button = tk.Button(self.canvas, text='Previous', command=lambda: self.previous_doc()).pack(side=tk.LEFT,padx=20)

    # return button
        self.ret = tk.Button(self.canvas, text="Return", padx=50, command=lambda:self.main_menu(account_name))
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

        self.image_path = 'resources/' + str(self.i) + '.png'
        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)

    # create labels for image
        self.image_label = tk.Label(self.canvas, image=self.photo)
        self.image_label.pack(pady=50)

    # label list for data
        self.lista_date = []
        self.lista_date.append(tk.Label(self.canvas, borderwidth=2, relief='raised', text='ID: ' + str(self.db_result[self.i][0])))
        self.lista_date.append(tk.Label(self.canvas, borderwidth=2, relief='raised', text='Nume: ' + str(self.db_result[self.i][1])))
        self.lista_date.append(tk.Label(self.canvas, borderwidth=2, relief='raised', text='Specialitate: ' + str(self.db_result[self.i][2])))
        self.lista_date.append(tk.Label(self.canvas, borderwidth=2, relief='raised', text='Disponibilitate: ' + str(self.db_result[self.i][3])))
        self.lista_date.append(tk.Label(self.canvas, borderwidth=2, relief='raised', text='Contact: ' + str(self.db_result[self.i][4])))
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
        

    def meeting_scheduling(self, account_name):
        
    # refresh page
        self.refresh(back.bg_doc_menu_image_path)

    # create blank character for positioning
        self.blank = tk.Label(self.canvas, text='', bg='black')
        self.blank.pack(pady = 50)

    # show what account is logged in
        self.canvas.account_text = self.canvas.create_text(5, 695, anchor=tk.SW,text='Logged in as: ' + account_name, font=12)

    # refresh button
        self.refresh_button = tk.Button(self.canvas, text="Refresh", command=lambda:self.meeting_scheduling(account_name))
        self.refresh_button.pack(side='bottom', anchor='se')

    # return button
        self.ret = tk.Button(self.canvas, text="Return", padx=50, command=lambda:self.main_menu(account_name))
        self.ret.pack(side='bottom', pady=30)

        self.db_cursor_medici.execute("SELECT * FROM Medici")
        self.result_medici = self.db_cursor_medici.fetchall()
        medici_list = []
        for element in self.result_medici:
            medici_list.append(element[1])
    
    # label for date
        self.date_label = tk.Label(self.canvas, text='Select a date:', bg='black', fg='white')
        self.date_label.pack()
    # calendar    
        self.date_calendar = Calendar(self.canvas, selectmode='day', date_pattern='yyyy-mm-dd')
        self.date_calendar.pack(pady=5)
        

    # label for doc choosing
        self.doc_label = tk.Label(self.canvas, text='Select a Doctor', bg='black', fg='white')
        self.doc_label.pack()
    # combobox for doc list
        self.doc_combobox = ttk.Combobox(self.canvas, values=medici_list, width=21)
        self.doc_combobox.pack(pady=5)
        

        time_list = ['08:00-09:00','09:00-10:00','10:00-11:00','11:00-12:00','12:00-13:00',
                     '13:00-14:00','14:00-15:00','15:00-16:00','16:00-17:00','17:00-18:00']
        
        
    # label for time
        self.time_label = tk.Label(self.canvas, text='Select a time:', bg='black', fg='white')
        self.time_label.pack()
    # combobox for time
        self.time_combobox = ttk.Combobox(self.canvas, values=time_list, width=10)
        self.time_combobox.pack(pady=5)
        

        location_list = ['Spitalul Clinic de Urgență pentru Copii „Grigore Alexandrescu”',
                         'Spitalul Clinic de Urgență București',
                         'Spitalul Universitar de Urgență București',
                         'Institutul Clinic Fundeni']
        
    # label for hospitals
        self.location_label = tk.Label(self.canvas, text='Select a location:', bg='black', fg='white')
        self.location_label.pack()
    # combobox for hospitals
        self.location_combobox = ttk.Combobox(self.canvas, values=location_list, width=51)
        self.location_combobox.pack(pady=5)
        

    # schedule button
        self.schedule = tk.Button(self.canvas, padx=50, pady=10, text='Schedule', command=lambda:self.create_schedule(account_name))
        self.schedule.pack(pady=15)
    
    def create_schedule(self, account_name):
        scheduling_list = []
        try:
            # Fetch PacientID for the given account_name
            self.db_cursor_programari.execute('SELECT PacientID FROM Pacienti WHERE Username = %s', (account_name,))
            pacient_id_result = self.db_cursor_programari.fetchone()
            
        # 0 - Rejected   1 - Awaiting response   2 - Accepted
            if pacient_id_result:
                self.db_cursor_programari.execute('SELECT MedicID FROM Medici WHERE Nume = %s', (self.doc_combobox.get(),))
                pacient_id = pacient_id_result[0]
                medic_id = self.db_cursor_programari.fetchone()[0]
                scheduling_list.append(pacient_id)
                scheduling_list.append(medic_id)
                scheduling_list.append(self.date_calendar.get_date())
                scheduling_list.append(self.time_combobox.get()[0:5])
                scheduling_list.append(self.time_combobox.get()[6:11])
                scheduling_list.append(self.location_combobox.get())
                scheduling_list.append(1)
                print(scheduling_list)
                query = 'INSERT INTO Programari (PacientID, MedicID, DataProgramare, OraInceput, OraSfarsit, Locatie, Confirmare) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                self.db_cursor_programari.execute(query, (
                    str(scheduling_list[0]),
                    str(scheduling_list[1]),
                    scheduling_list[2],
                    scheduling_list[3],
                    scheduling_list[4],
                    scheduling_list[5],
                    str(scheduling_list[6])
                    ))
                conn.commit()
            else:
                print("No PacientID found for %s", (account_name,))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.db_cursor_programari.close()

# main loop
        
if __name__ == '__main__':
    root = tk.Tk()
    conn = mysql.connector.connect(
        host='16.171.166.64',
        password='admin', 
        user='admin', 
        database='mossad'
    )

if conn.is_connected():
    print('Connection established...')
    
app = Application(master=root)
app.mainloop()
