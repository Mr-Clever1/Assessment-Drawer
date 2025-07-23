#16/07/2025
#Schematic Drawer
#James Burt
from tkinter import *

CANVAS_SIZE = (437, 614)
IMAGE_FOLDER_PATH = r"Toolbar_Icons/"
TOOLBAR_LAYOUT = {
    "CONFIGURE":"SETTINGS.png",
    "PRINT":"PRINT.png",
    "RECTANGLE":"RECTANGLE.png",
    "ELIPSE":"ELIPSE.png",
    "TRIANGLE":"TRIANGLE.png",
    "LINE":"LIne.png"
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
        #Establish basic shape information
        self.current_shape = None
        self.drawing_type = "RECTANGLE"
        self.current_vertices = []
        self.is_drawing = False
        self.all_polygons = []
        self.temp_shape = None
        self.root = self.createMainWindow()
        self.place_buttons(TOOLBAR_LAYOUT,self.toolbar_frame)

        #Bindings for inputs
        self.design.bind("<Motion>", self.mouseDrag)
        self.design.bind('<Button-1>', self.mouseDown)
        self.design.bind("<ButtonRelease-1>",  self.mouseUp)
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
        
        #Establish the Tkinter canvas for drawing on
        self.design = Canvas(self.design_frame,width=CANVAS_SIZE[0],height=CANVAS_SIZE[1],bg="white")
        self.design.grid(row=1,column=0)
        return root

    def mouseDown(self,event):
        if self.drawing_type != "":
            self.mouse_down_event = event
            self.is_drawing = True
            self.current_vertices = [0,0,0,0,0,0]
            #Create temp shape for design guide
            self.temp_shape = self.design.create_polygon(*self.current_vertices, outline='black', fill='', dash=(4, 2))
            pass

    def mouseUp(self,event):
        self.mouse_up_event = event
        self.is_drawing = False
        rect = self.design.create_polygon(self.current_vertices, outline='black', fill='')
        print(rect)
        new_shape = Shape(self.drawing_type,self.convert_coordinates(self.current_vertices),rect,"None")
        self.all_polygons.append(new_shape)
        pass    
    
    def mouseDrag(self,event):
         if self.is_drawing == True:
            self.mouse_pos = (event.x,event.y)
            x0,y0 = (self.mouse_down_event.x,self.mouse_down_event.y)
            x1,y1 = self.mouse_pos
            shape_vertices = []
            match(self.drawing_type):
                case "RECTANGLE":
                    shape_vertices = [x0,y0,x1,y0,x1,y1,x0,y1]
                case "TRIANGLE":
                    shape_vertices = [x0,y0,x1,y1,x0,y1]


                    
            self.design.coords(self.temp_shape,*shape_vertices)                    
            self.current_vertices = shape_vertices  

                
    def place_buttons(self,to_be_placed:dict,frame:Frame):
        self.labels = []
        for index,key in enumerate(to_be_placed):
            print(key)
            to_be_placed[key] = (PhotoImage(file=IMAGE_FOLDER_PATH+to_be_placed[key]))
            label = Button(frame,image=to_be_placed[key],command=lambda:self.toolbar_commands(key))
            label.grid(row=0,column=index)
            self.labels.append(label)
    
    def convert_coordinates(self,inital_coords):
        #Converts coordinates from each value being its own item to tuples of coords
        #tkinter likes each value as its own item in a list
        #PIL likes tuples of coordinates
        tuple_coords = []
        for i in range(len(inital_coords),2):
            tuple_coords.append((inital_coords[i],inital_coords[i+1]))
        return tuple_coords

    def toolbar_commands(self,command):
        print("called")
        print(command)
        if command == "RECTANGLE":
            print("boos")


            
            

window = Drawer()
window.root.mainloop()