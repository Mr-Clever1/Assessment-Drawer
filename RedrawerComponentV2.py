#RedrawerComponent
#Paired with SchematicDrawer.py
#30/07/2025
#James Burt
from PIL import Image,ImageDraw
import win32com.client
import os
import threading
import pythoncom

#Called when attempting to print an image
def tkinter_to_PIL(self,shapes,scale):
    global file
    #Creates a new file and canvas
    file = Image.new("RGB",self.canvas_size,"white")
    draw = ImageDraw.Draw(file)
    #Loops through every existing shape and redraws them onto the new canvas
    for polygon in shapes:
        for index,vertex in enumerate(polygon.vertices):
            #Creates a adjusts the list item to be scaled correctly
            polygon.vertices[index] = (vertex[0]*scale,vertex[1]*scale)

        if polygon.colour == ("" or "None"):
            polygon.colour = None
        #Draws onto new canvas
        draw.polygon(polygon.vertices,outline="black",fill=polygon.colour)
    #Scales drawing to be desired paper size
    file = file.resize(self.AN_SIZES[self.current_paper_size][0])
    threading.Thread(target=print_picture,daemon=True).start()
def print_picture():

    pythoncom.CoInitialize() 
    #Saves and opens image
    file_name = "RecentPrint.png"
    file_path = os.path.abspath(os.getcwd())+f"\{file_name}"
    file.save(file_path)
    

    wia_dialog = win32com.client.Dispatch("WIA.CommonDialog")

    # Launch the photo printing wizard with the specified file
    wia_dialog.ShowPhotoPrintingWizard(file_path)