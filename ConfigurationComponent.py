#ConfigurationComponent
#Paired with SchematicDrawer.py
#31/07/2025
#James Burt
#Create secondary window at make it always at the top
from tkinter import *
from tkinter import messagebox
drawer = None

def create_configure_window(self):
    #Creates global variable so that I can access it in entry edited function without having to pass in self again
    global drawer
    drawer = self
    #Creates config window and attributes it to always be the topmost window on the screen
    drawer.configure_window = Toplevel(drawer.root)
    drawer.configure_window.attributes('-topmost', True)

    #Create entry box to take in the paper size value
    drawer.paper_size_val  =  StringVar()
    drawer.paper_size_entry = Entry(drawer.configure_window,textvariable=drawer.paper_size_val)
    drawer.paper_size_entry.insert("0",f"{drawer.current_paper_size}")

    #Call function whenever you click off of the entry box
    drawer.paper_size_entry.bind("<FocusOut>",  lambda k:entry_edited(drawer.paper_size_val.get(),0,len(drawer.AN_SIZES)-1,"PAPER_SIZE"))
    drawer.paper_size_entry.grid(row=0,column=0)

    #Button to print configuration line
    drawer.configure_print_button = Button(drawer.configure_window,command=lambda:drawer.button_commands("PRINT"))
    drawer.configure_print_button.grid(row=0,column=1)
    
    #Real scale input box.
    drawer.calibration_val = IntVar()
    drawer.config_calibrate_entry = Entry(drawer.configure_window,textvariable=drawer.calibration_val)
    
    #Clear box and add real scale
    drawer.config_calibrate_entry.delete("0",END)
    drawer.config_calibrate_entry.insert("0",f"{drawer.real_scale}")

    #Call function whenever you click off of the entry box
    drawer.config_calibrate_entry.bind("<FocusOut>",  lambda k:entry_edited(drawer.calibration_val.get(),0,drawer.AN_SIZES[drawer.current_paper_size][1][0],"CONFIG_SCALE"))
    drawer.config_calibrate_entry.grid(row=1,column=0)

#Called when an entry box has its value eddited
def entry_edited(val,lower,upper,exception_val):
    try:         
        #Fail if entry is blank
        if val=="":
            raise ValueError
        else:
            size = int(val)
            #Fail if it exceeds the bounds provided
            if (size < lower or size > upper):
                raise ValueError
    except ValueError: 
        #Reset value back to what it was previously
        if exception_val == "PAPER_SIZE":
            drawer.paper_size_val.set(f"{drawer.current_paper_size}")
        elif exception_val == "CONFIG_SCALE":
            drawer.calibration_val.set(f"{drawer.real_scale}")
        #Send error message informing user of error
        messagebox.showerror(exception_val, f"Please enter a whole number between {lower} and {upper}")
        return None
    #If no error occurs update desired value
    if exception_val == "PAPER_SIZE":
        drawer.current_paper_size = size
    elif exception_val == "CONFIG_SCALE":
        drawer.real_scale = size
            