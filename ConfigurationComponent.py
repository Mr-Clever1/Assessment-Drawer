#ConfigurationComponent
#Paired with SchematicDrawer.py
#31/07/2025
#James Burt
#Create secondary window at make it always at the top
from tkinter import *
from tkinter import messagebox
drawer = None

def create_configure_window(self):
    global drawer
    drawer = self
    drawer.configure_window = Toplevel(drawer.root)
    drawer.configure_window.attributes('-topmost', True)

    #Create entry box to take in the paper size value
    drawer.paper_size_val  =  StringVar()
    drawer.paper_size_entry = Entry(drawer.configure_window,textvariable=drawer.paper_size_val)
    drawer.paper_size_entry.insert("0",f"{drawer.current_paper_size}")

    #Call function whenever you click off of the entry box
    drawer.paper_size_entry.bind("<FocusOut>",  lambda k="size":entry_edited(k))
    drawer.paper_size_entry.grid(row=0,column=0)

    drawer.configure_print_button = Button(drawer.configure_window,command=lambda:drawer.button_commands("PRINT"))
    drawer.configure_print_button.grid(row=0,column=1)
    
    drawer.calibration_val = IntVar()
    drawer.config_calibrate_entry = Entry(drawer.configure_window,textvariable=drawer.paper_size_val)
    drawer.config_calibrate_entry.insert("0","100")
    #Call function whenever you click off of the entry box
    drawer.config_calibrate_entry.bind("<FocusOut>", lambda k="cali":entry_edited(k))
    drawer.config_calibrate_entry.grid(row=1,column=0)

def entry_edited(val,lower,upper,exception_val):
    try:         
        if drawer.paper_size_val.get()=="":
            raise ValueError
        else:
            size = int(drawer.paper_size_val.get())
            if (size < 0 or size > len(drawer.AN_SIZES)-1):
                raise ValueError
    except ValueError:            
        messagebox.showerror("Invalid Paper Size", f"Please enter a value between 0 and {len(drawer.AN_SIZES)-1}")
        drawer.paper_size_val.set(f"{drawer.current_paper_size}")
        return None
    drawer.current_paper_size = size            