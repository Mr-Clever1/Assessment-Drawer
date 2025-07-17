#16/07/2025
#Schematic Drawer
#James Burt
from tkinter import *

IMAGE_FOLDER_PATH = r"Toolbar_Icons/"
TOOLBAR_BUTTONS = {
    "RECTANGLE":"BUTTON_1.png",
    "ELIPSE":"BUTTON_2.png",
    "TRIANGLE":"BUTTON_3.png",
    "LINE":"BUTTON_4.png"
}

#Stores all of the information I require about each polygon on the canvas
class Shape:
    def __init__(self,type,vertices,rect,colour) -> None:
        self.type = type
        self.vertices = vertices
        self.rect = rect
        self.colour = colour
        pass


class Drawer:
    def __init__(self) -> None:
        self.current_shape = 0
        self.root = self.createMainWindow()
        self.place_buttons(TOOLBAR_BUTTONS,self.toolbar_frame)

        pass

    #Creates the main window
    def createMainWindow(self):
        
        #Establish window
        root = Tk()

        #Establish toolbar to store all of the tools useable
        self.toolbar_frame = Frame(root,bg="grey")
        self.toolbar_frame.grid(row=0,column=0,sticky="news")       
        
        #Establish dimension bar to display the dimensions and mouse position
        self.dimensions_bar_frame = Frame(root,bg="grey")
        self.dimensions_bar_frame.grid(row=1,column=0,sticky="news")
        
        #Establish design frame where the user will be able to draw on the canvas
        self.design_frame = Frame(root,bg="red")
        self.design_frame.grid(row=2,column=0,sticky="news")
        


        return root

    def mouseDown(self,event):
        pass

    def mouseUp(self,event):
        pass    
    
    def mouseDrag(self,event):
        pass

    def place_buttons(self,to_be_placed:dict,frame:Frame):
        self.labels = []
        for index,key in enumerate(to_be_placed):
            print(key)
            to_be_placed[key] = (PhotoImage(file=IMAGE_FOLDER_PATH+to_be_placed[key]))
            label = Button(frame,image=to_be_placed[key],command=None)
            label.grid(row=0,column=index)
            self.labels.append(label)
            
            

window = Drawer()
window.root.mainloop()