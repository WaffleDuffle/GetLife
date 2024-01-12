import tkinter as tk
import os
import backgrounds as back
import mysql.connector
from datetime import datetime, timedelta
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
    # define cursor for pacienti, medici and programari tables
        self.db_cursor_pacienti = conn.cursor()
        self.db_cursor_medici = conn.cursor()
        self.db_cursor_programari = conn.cursor()

    # refresh page
        self.refresh(back.bg_login_image_path)

    # create blank character for positioning
        self.blank = tk.Label(self.canvas, text='', bg='#cf71ff')
        self.blank.pack(pady = 155)

    # load exit button
        self.quit = tk.Button(self.canvas, text="EXIT", padx=50, fg="red", command=lambda:self.exit_program())
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
        self.quit = tk.Button(self.canvas, text="EXIT", padx=50, fg="red", command=lambda:self.exit_program())
        self.quit.pack(side='bottom', pady=30)

    # return button
        self.ret = tk.Button(self.canvas, text="Return", padx=50, command=lambda:self.first_page())
        self.ret.pack(side='bottom')


    def check_cred(self, name1, name2):
    # load environmental variables for admin username and password
        load_dotenv()
    
        
        ok = 0 # this variable checks for all the different guest types

        if name1 == os.getenv('NAME') and name2 == os.getenv('PASSWORD'):
            self.main_menu('admin', 1)
        else:
            ok += 1

    # query to fetch username and password from Pacienti
        self.db_cursor_pacienti.execute("SELECT * FROM Pacienti WHERE Username = %s AND Parola = %s", (name1, name2))
        self.result_pacienti = self.db_cursor_pacienti.fetchone()
        if self.result_pacienti:
            self.main_menu(self.result_pacienti[6], 1) # username column for pacienti
        else:
            ok += 1
    # querry to fetch username and password form Medici
        self.db_cursor_medici.execute("SELECT * FROM Medici WHERE Username = %s AND Parola = %s", (name1, name2))
        self.result_medici = self.db_cursor_medici.fetchone()
        if self.result_medici:
            self.main_menu(self.result_medici[1], 0) #name column for medici
        else:
            ok += 1
        
        if ok == 3:
            self.send_notification('Error', 'Incorect Username or Password!')
            

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
        self.quit = tk.Button(self.canvas, text="EXIT", padx=50, fg="red", command=lambda:self.exit_program())
        self.quit.pack(side='bottom', pady=30)
    
    # return button
        self.ret = tk.Button(self.canvas, text="Return", padx=50, command=lambda:self.first_page())
        self.ret.pack(side='bottom')


    def create_entry_register(self, label_text):

        label = tk.Label(self.canvas, text=label_text, fg='white', bg='black')
        label.pack()
        if label_text == 'Enter your password:':
            entry = tk.Entry(self.canvas, show='*')
        else:
            entry = tk.Entry(self.canvas)
        entry.pack()
        self.register_list.append(entry)


    def create_account(self):
        user_data = []
    # entry_data gets all the entries from sign_up
        for entry_data in self.register_list:
            user_data.append(entry_data.get())

         
        try:
            self.db_cursor_pacienti.execute('INSERT INTO Pacienti (PacientID, Nume, Prenume, DetaliiContact, AntecedenteMedicale, Parola, Username) VALUES ('
                                            + user_data[2] + ','
                                            + "'" + user_data[3] + "'" + ','
                                            + "'" + user_data[4] + "'" + ','
                                            + "'" + user_data[5] + "'" + ','
                                            + "'" + user_data[6] + "'" + ','
                                            + "'" + user_data[1] + "'" + ','
                                            + "'" + user_data[0] + "'" + ')') # register widgets order doesn't correspond to database columns orders, I know
            conn.commit()
            self.send_notification('GetLife', 'Account created')
            self.login()
        except:
            self.send_notification('Error', 'Blank fields or already used ID') 
            
        

    def main_menu(self, account_name, guest_type):   #guest_type:     1 = Pacient     0 = Medic
    #check if you have notifications
        self.check_notification(account_name, guest_type)

    #check if you have reminders
        if guest_type == 1:
            self.reminders(account_name)
        
    # refresh page
        self.refresh(back.bg_main_menu_image_path)
        
    # show what account is logged in
        self.canvas.account_text = self.canvas.create_text(5, 695, anchor=tk.SW,text='Logged in as: ' + account_name, font=12)

    # blank character for positioning
        self.blank2 = tk.Label(self.canvas, text='', bg='black')
        self.blank2.pack(pady = 132)

    # show Doctors
        self.print_doctors = tk.Button(self.canvas, text="Doctors", padx=50, pady=10, command=lambda: self.doctors_menu(account_name, guest_type))
        self.print_doctors.pack(side="top", pady= 15)

        if guest_type == 1:
        # scheduling button
            self.schedule_button = tk.Button(self.canvas, text="Schedule a meeting", padx=50, pady=10, command=lambda: self.meeting_scheduling(account_name))
            self.schedule_button.pack(pady= 15)

    #meeting button
        self.schedule_button = tk.Button(self.canvas, text="Meetings", padx=50, pady=10, command=lambda: self.meetings(account_name, guest_type))
        self.schedule_button.pack(pady= 15)
        
    #refresh button
        self.refresh_button = tk.Button(self.canvas, text="Refresh", command=lambda:self.main_menu(account_name, guest_type))
        self.refresh_button.pack(side='bottom', anchor='se')    

    # exit button
        self.quit = tk.Button(self.canvas, text="EXIT", padx=50, fg="red", command=lambda:self.exit_program())
        self.quit.pack(side='bottom', pady=30)

    # logout button
        self.log_out = tk.Button(self.canvas, text='Log Out', command=lambda:self.login())
        self.log_out.pack(side='bottom')


    def doctors_menu(self, account_name, guest_type):
    # refresh page
        self.refresh(back.bg_doc_menu_image_path)
        
    # show what account is logged in
        self.canvas.account_text = self.canvas.create_text(5, 695, anchor=tk.SW,text='Logged in as: ' + account_name, font=12)

    # initialize cursor in database
        self.db_cursor_medici.execute("SELECT * FROM Medici")
        self.db_result = self.db_cursor_medici.fetchall()
        self.increment = 0
        

    # buttons for crossing 
        self.next_button = tk.Button(self.canvas, padx = 28, text='Next', command=lambda: self.next_doc())

        self.next_button.pack(side=tk.RIGHT, padx=20)

        self.previous_button = tk.Button(self.canvas, text='Previous', command=lambda: self.previous_doc())

        self.previous_button.pack(side=tk.LEFT,padx=20)

    # return button
        self.ret = tk.Button(self.canvas, text="Return", padx=50, command=lambda:self.main_menu(account_name, guest_type))
        self.ret.pack(side='bottom', pady=30)

    # print first medic
        self.print_medici()

    def next_doc(self):
        
        self.increment += 1
        if self.increment == len(self.db_result) or self.increment < 0:
            print('OUT OF BOUNDS!!!')
            self.increment = 0    
        self.print_medici()
                                            # next_doc and previous_doc are used to show doctors and go in circle

    def previous_doc(self):
        self.increment -= 1
        if self.increment == len(self.db_result) or self.increment < 0:
            print('OUT OF BOUNDS!!!')
            self.increment = len(self.db_result) - 1            
        self.print_medici()
        
        
    def print_medici(self):
    # checks if image_label has been defined already
        if hasattr(self, 'image_label'):
            self.image_label.pack_forget()
        # remove old labels from the list
            for label in self.lista_date:
                label.pack_forget()

        self.image_path = 'resources/' + str(self.increment) + '.png'
        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)

    # create labels for image
        self.image_label = tk.Label(self.canvas, image=self.photo)
        self.image_label.pack(pady=50)

    # label list for data
        self.lista_date = []
        self.lista_date.append(tk.Label(self.canvas, borderwidth=2, relief='raised', text='ID: ' + str(self.db_result[self.increment][0])))
        self.lista_date.append(tk.Label(self.canvas, borderwidth=2, relief='raised', text='Nume: ' + str(self.db_result[self.increment][1])))
        self.lista_date.append(tk.Label(self.canvas, borderwidth=2, relief='raised', text='Specialitate: ' + str(self.db_result[self.increment][2])))
        self.lista_date.append(tk.Label(self.canvas, borderwidth=2, relief='raised', text='Disponibilitate: ' + str(self.db_result[self.increment][3])))
        self.lista_date.append(tk.Label(self.canvas, borderwidth=2, relief='raised', text='Contact: ' + str(self.db_result[self.increment][4])))
    # label packing
        for label in self.lista_date:
            label.pack(pady=5)
        


    def refresh(self, background_path):
    # Delete widgets
        for widget in self.canvas.winfo_children():
            widget.destroy()

        # Import background using PIL
        self.canvas.delete("all")
        pil_image = Image.open(background_path)
        self.bg_image = ImageTk.PhotoImage(pil_image)

        # Create image on canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
        self.canvas.pack()

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
        self.ret = tk.Button(self.canvas, text="Return", padx=50, command=lambda:self.main_menu(account_name, 1))
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
            # fetch PacientID for the given account_name
            self.db_cursor_programari.execute('SELECT PacientID FROM Pacienti WHERE Username = %s', (account_name,))
            pacient_id_result = self.db_cursor_programari.fetchone()
            
        
            if pacient_id_result:
                self.db_cursor_programari.execute('SELECT MedicID FROM Medici WHERE Nume = %s', (self.doc_combobox.get(),))
                pacient_id = pacient_id_result[0]
                medic_id = self.db_cursor_programari.fetchone()[0]
                scheduling_list.append(pacient_id)
                scheduling_list.append(medic_id)
                scheduling_list.append(self.date_calendar.get_date())
                scheduling_list.append(self.time_combobox.get()[0:5])    # stirng splicing for time
                scheduling_list.append(self.time_combobox.get()[6:11])
                scheduling_list.append(self.location_combobox.get())
                scheduling_list.append('Awaiting response...') 
                print(scheduling_list)
                query = 'INSERT INTO Programari (PacientID, MedicID, DataProgramare, OraInceput, OraSfarsit, UniqueKey, Locatie, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                self.db_cursor_programari.execute(query, (
                    str(scheduling_list[0]),                                                                      #PacientID
                    str(scheduling_list[1]),                                                                      #MedicID
                    scheduling_list[2],                                                                           #DataProgramare
                    scheduling_list[3],                                                                           #OraInceput
                    scheduling_list[4],                                                                           #OraSfarsit
                    str(scheduling_list[1]) + scheduling_list[2] + scheduling_list[3] + scheduling_list[4],       #UniqueKey
                    scheduling_list[5],                                                                           #Locatie
                    str(scheduling_list[6])                                                                       #Status
                    ))                                                  
                
                query = 'UPDATE Medici SET Notificari = 1 WHERE MedicID = %s' 

                self.db_cursor_programari.execute(query, (str(scheduling_list[1]),))

                self.send_notification('GetLife', 'Your request has been submitted, awaiting response...')
                conn.commit()
                self.main_menu(account_name, 1)

            else:
                print("No PacientID found for %s", (account_name,))

        except Exception as e:
            self.send_notification('Error', 'Slot already taken!')
            print(f"ERROR: {e}")
        

    def meetings(self, account_name, guest_type):

    # new window because table is too big
        self.new_window = tk.Toplevel(self.canvas)
        self.new_window.title('Meetings')

    # Treeview of Programari table
        self.tree = ttk.Treeview(self.new_window)
        self.tree["columns"] = ("ProgramareID", "PacientID", "MedicID", "DataProgramare", "OraInceput", "OraSfarsit", "Locatie", "Status")  
        self.tree.heading('#1', text='ProgramareID')  
        self.tree.heading('#2', text='PacientID')
        self.tree.heading('#3', text='MedicID')
        self.tree.heading('#4', text='DataProgramare')
        self.tree.heading('#5', text='OraInceput')
        self.tree.heading('#6', text='OraSfarsit')
        self.tree.heading('#7', text='Locatie')
        self.tree.heading('#8', text='Status')

        self.programariID = [] # this ID list exists for easy selection in next combobox

    # button to fetch and display data
        fetch_button = tk.Button(self.new_window, text="Fetch Data", command=lambda: self.fetch_data(account_name, guest_type))
        fetch_button.pack(pady=10)

    # exit button
        self.quit = tk.Button(self.new_window, text="EXIT", padx=50, fg="red", command=self.new_window.destroy)
        self.quit.pack(side='bottom', pady=10)

    # pack the Treeview
        self.tree.pack(fill=tk.BOTH)


    def fetch_data(self, account_name, guest_type):
        
        conn.commit()
        try:
            if guest_type == 0:  # if guest is doctor
                self.db_cursor_programari.execute('SELECT MedicID FROM Medici WHERE Nume = %s', (account_name,))
                medic_id = self.db_cursor_programari.fetchone()[0]
                self.db_cursor_programari.execute('SELECT * FROM Programari WHERE MedicID = %s ORDER BY FIELD(Status, "Awaiting response...", "Rescheduled, awaiting response...", "Accepted", "Rejected") DESC', (medic_id,))
            else:
                self.db_cursor_programari.execute('SELECT PacientID FROM Pacienti WHERE Username = %s', (account_name,))
                pacient_id = self.db_cursor_programari.fetchone()[0]
                self.db_cursor_programari.execute('SELECT * FROM Programari WHERE PacientID = %s ORDER BY FIELD(Status, "Awaiting response...", "Rescheduled, awaiting response...", "Accepted", "Rejected") DESC', (pacient_id,))

        except Exception as e:
            print(f'ERROR: {e}')
            self.send_notification('GetLife', 'You have no meetings')
            
        data = self.db_cursor_programari.fetchall()

        
        
    # update the Treeview with fetched data
        self.update_treeview(data)

    # combobox for id selection
        if guest_type == 0:
            self.medic_meeting_widgets()
        else:
            self.pacient_meeting_widgets()



    def update_treeview(self, data):
        self.programariID.clear() # clear existing data in list
        
        # clear existing data in the Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # insert new data into the Treeview
        for row in data:
            self.tree.insert("", "end", values=row[:6] + row[7:])
            self.programariID.append(row[0])  # first column for ProgramareID



    def medic_meeting_widgets(self):
     # refresh widgets   
        try:
            self.id_label.destroy()
            self.id_combobox.destroy()
            self.accept_button.destroy()
            self.reject_button.destroy()
        except Exception as e:
            print('first iteration')

    # label for ID
        self.id_label = tk.Label(self.new_window, text='Select an ID')
        self.id_label.pack(pady=10)

    # combobox for ID selection
        self.id_combobox = ttk.Combobox(self.new_window, values=self.programariID, width=10)
        self.id_combobox.pack(pady=10)

    # button for accept
        self.accept_button = tk.Button(self.new_window, padx=50, pady=10, text ='Accept', command=lambda:self.accept_meeting())
        self.accept_button.pack(pady=10)
        
    # button for reject
        self.reject_button = tk.Button(self.new_window, padx=50, pady=10, text ='Reject', command=lambda:self.reject_meeting())
        self.reject_button.pack(pady=10)


    def accept_meeting(self):

        self.selected_id = self.id_combobox.get()

        self.db_cursor_programari.execute('SELECT * FROM Programari WHERE ProgramareID = %s', (self.selected_id,))
        self.programare_result = self.db_cursor_programari.fetchone()

        self.db_cursor_pacienti.execute('UPDATE Pacienti SET Notificari = 1 WHERE PacientID = %s', (self.programare_result[1],))

        self.db_cursor_programari.execute('UPDATE Programari SET Status = %s WHERE ProgramareID = %s', ('Accepted', self.selected_id,))

        conn.commit()
        string = f'A meeting has been established at {self.programare_result[7]}\nDate: {self.programare_result[3]}\nStarting hour: {str(self.programare_result[4])}\nFinish hour: {str(self.programare_result[5])}\nPacientID: {self.programare_result[1]}'
        self.send_notification('GetLife', string)


    def reject_meeting(self):

        self.selected_id = self.id_combobox.get()

        self.db_cursor_programari.execute('SELECT * FROM Programari WHERE ProgramareID = %s', (self.selected_id,))
        self.programare_result = self.db_cursor_programari.fetchone()

        self.db_cursor_pacienti.execute('UPDATE Pacienti SET Notificari = 1 WHERE PacientID = %s', (self.programare_result[1],))

        self.db_cursor_programari.execute('UPDATE Programari SET Status = %s WHERE ProgramareID = %s', ('Rejected', self.selected_id,))

        conn.commit()
        self.send_notification('GetLife', 'Meeting has been rejected')


    def pacient_meeting_widgets(self):
        # refresh widgets   
        try:
            self.id_label.destroy()
            self.id_combobox.destroy()
            self.cancel_button.destroy()
            self.reschedule_button.destroy()
        except Exception as e:
            print('first iteration')

    # label for ID
        self.id_label = tk.Label(self.new_window, text='Select an ID')
        self.id_label.pack(pady=10)

    # combobox for ID selection
        self.id_combobox = ttk.Combobox(self.new_window, values=self.programariID, width=10)
        self.id_combobox.pack(pady=10)

    # button for cancel
        self.cancel_button = tk.Button(self.new_window, padx=50, pady=10, text ='Cancel', command=lambda:self.cancel_meeting())
        self.cancel_button.pack(pady=10)
        
    #button for rescheduling
        self.reschedule_button = tk.Button(self.new_window, padx=35, pady=10, text ='Reschedule', command=lambda:self.reschedule_meeting())
        self.reschedule_button.pack(pady=10)


    def cancel_meeting(self):

        self.selected_id = self.id_combobox.get()

        self.db_cursor_programari.execute('SELECT * FROM Programari WHERE ProgramareID = %s', (self.selected_id,))
        self.programare_result = self.db_cursor_programari.fetchone()

        self.db_cursor_medici.execute('UPDATE Medici SET Notificari = 1 WHERE MedicID = %s', (self.programare_result[2],))

        self.db_cursor_programari.execute('UPDATE Programari SET Status = %s WHERE ProgramareID = %s', ('Canceled', self.selected_id,))

        conn.commit()
        self.send_notification('GetLife', 'Meeting has been canceled')


    def reschedule_meeting(self):

    # new window for reschedule
        self.reschedule_window = tk.Toplevel(self.new_window)
        self.reschedule_window.title('Reschedule')

        selected_id = self.id_combobox.get()

    # label for date
        self.reschedule_date_label = tk.Label(self.reschedule_window, text='Select a date:')
        self.reschedule_date_label.pack()
    # calendar    
        self.reschedule_date_calendar = Calendar(self.reschedule_window, selectmode='day', date_pattern='yyyy-mm-dd')
        self.reschedule_date_calendar.pack(pady=5)

        
        time_list = ['08:00-09:00','09:00-10:00','10:00-11:00','11:00-12:00','12:00-13:00',
                     '13:00-14:00','14:00-15:00','15:00-16:00','16:00-17:00','17:00-18:00']
        
        
    # label for time
        self.reschedule_time_label = tk.Label(self.reschedule_window, text='Select a time')
        self.reschedule_time_label.pack()
    # combobox for time
        self.reschedule_time_combobox = ttk.Combobox(self.reschedule_window, values=time_list, width=10)
        self.reschedule_time_combobox.pack(pady=5)

    # exit button
        self.quit = tk.Button(self.reschedule_window, text="EXIT", padx=50, fg="red", command=lambda:self.reschedule_window.destroy())
        self.quit.pack(side='bottom', pady=10)

    # ok button
        self.ok_button = tk.Button(self.reschedule_window, text="OK", padx=50, command=lambda:self.reschedule(selected_id))
        self.ok_button.pack(side='bottom', pady=10)

    
    def reschedule(self, selected_id):
        rescheduling_list = []
        try:
            rescheduling_list.append(self.reschedule_date_calendar.get_date())
            rescheduling_list.append(self.reschedule_time_combobox.get()[0:5])    # stirng splicing for time
            rescheduling_list.append(self.reschedule_time_combobox.get()[6:11])

        # this query updates the already existing meetin, uniqueid must be updated by concatenating the first character coresponding to medic ID 
            # with the new key
            query = 'UPDATE Programari SET UniqueKey = LEFT(UniqueKey, 1) WHERE ProgramareID = %s'
            self.db_cursor_programari.execute(query, (selected_id,))

            query = 'UPDATE Programari SET DataProgramare = %s, OraInceput = %s, OraSfarsit = %s, UniqueKey = CONCAT(UniqueKey, %s), Status = %s WHERE ProgramareID = %s'

            self.db_cursor_programari.execute(query, (rescheduling_list[0], rescheduling_list[1], rescheduling_list[2], 
                                                      str(rescheduling_list[0]+rescheduling_list[1]+rescheduling_list[2]),
                                                      'Rescheduled, awaiting response...', selected_id,))

            conn.commit()
            self.send_notification('GetLife', 'Meeting has been rescheduled, awaiting respone...')
            self.reschedule_window.destroy()
        except Exception as e:
            print(f'ERROR: {e}')
            self.send_notification('ERROR', 'Slot already taken!')            

    def check_notification(self, account_name, guest_type):
       #if guest is medic 
        if guest_type == 0:
            self.db_cursor_medici.execute('SELECT Notificari FROM Medici WHERE Nume = %s', (account_name,))
            notificare = self.db_cursor_medici.fetchone()[0]
            self.db_cursor_medici.nextset()

            if notificare == 1:    # if there are changes to entires
                self.send_notification('GetLife', 'You have new entries, check your inbox')
                self.db_cursor_medici.execute('UPDATE Medici SET Notificari = 0 WHERE Nume = %s', (account_name,))
                conn.commit()

        #else guest is pacient
        else:
            self.db_cursor_pacienti.execute('SELECT Notificari FROM Pacienti WHERE Username = %s', (account_name,))
            notificare = self.db_cursor_pacienti.fetchone()[0]
            self.db_cursor_pacienti.nextset()
            if notificare == 1:     # if there are changes to entires
                self.send_notification('GetLife', 'You have new entries, check your inbox')
                self.db_cursor_pacienti.execute('UPDATE Pacienti SET Notificari = 0 WHERE Username = %s', (account_name,))
                conn.commit()


    def reminders(self, account_name):
    #fetch corresponding data
        self.db_cursor_programari.execute('SELECT PacientID FROM Pacienti WHERE Username = %s', (account_name,))
        pacient_id = self.db_cursor_programari.fetchone()[0]
        self.db_cursor_programari.execute('SELECT * FROM Programari WHERE PacientID = %s', (pacient_id,))
        data = self.db_cursor_programari.fetchall()

        current_datetime = datetime.now()

        for element in data:
            if element[9] == 0 and element[8] == 'Accepted':
                date_value = element[3]  # Data
                start_time_value = element[4]  # OraInceput


                # Convert timedelta to time
                start_time = (datetime.min + start_time_value).time()

                appointment_datetime = datetime.combine(date_value, start_time)  # Combine date and start time

                # Calculate the time difference
                time_difference = appointment_datetime - current_datetime
                # Check if the time difference is less than one hour
                if timedelta(minutes=0) <= time_difference <= timedelta(days=1):
                    self.send_notification('Reminder', f'You have an upcoming meeting today at {element[4]}\n{element[7]}')
                    print(element[0])
                    self.db_cursor_programari.execute('UPDATE Programari SET Reminder = 1 WHERE ProgramareID = %s', (element[0],))
                    conn.commit()
            

    def send_notification(self, tmp_title, tmp_message):
        notification.notify(
            title=tmp_title,
            message=tmp_message,
            app_name='GetLife',
        )

    def exit_program(self):
        self.db_cursor_medici.close()
        self.db_cursor_pacienti.close()
        self.db_cursor_programari.close()
        print('End of program')
        root.destroy()

    

# main loop
        
if __name__ == '__main__':
    root = tk.Tk()

    #load environment varaibles
    load_dotenv()

    #trying to connect
    try:
        conn = mysql.connector.connect(
            host = os.getenv('HOST'),
            password = os.getenv('DB_PASSWORD'), 
            user = os.getenv('DB_USER'), 
            database = os.getenv('DATABASE')
        )
        print('Connection established...')
        app = Application(master=root)
        app.mainloop()

    except Exception as e:
        print(e)
        print('Connection failed')    

