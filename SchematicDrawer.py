#16/07/2025
#Schematic Drawer
#James Burt
from tkinter import *
import math

#Define program constants
#How big the canvas will be in the program, has to maintain this ratio of 1:√2
CANVAS_SIZE = (437, 614)

#Defines image names and folder that they're in
IMAGE_FOLDER_PATH = r"Toolbar_Icons/"
TOOLBAR_LAYOUT = {
    "CONFIGURE":"SETTINGS.png",
    "PRINT":"PRINT.png",
    "RECTANGLE":"RECTANGLE.png",
    "ELIPSE":"ELIPSE.png",
    "TRIANGLE":"TRIANGLE.png",
    "LINE":"LIne.png"
}

#Paper Sizes, sizes in pixles then mm
AN_SIZES = {
    0: [(9933,14043),(841, 1189)],
    1: [(7016,9933),(594, 841)],
    2: [(4961,7016),(420, 594)],
    3: [(3508,4961), (297, 420)],
    4: [(2480,3508),(210, 297)],
    5: [(1748,2480),(148, 210)],
    6: [(1240,1748),(105, 148)],
    7: [(874,1240),(74, 105)],
    8: [(614,874),(52, 74)],
    9: [(437,614), (37, 52)],
    10:[(307,437),(26, 37)]

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
        #Establish basic drawing information
        self.current_shape = None
        self.drawing_type = ""
        self.current_vertices = []
        self.is_drawing = False
        self.temp_shape = None
        self.current_paper_size = 5

        self.all_polygons = []
        self.all_coordinates = []

        self.mouse_pos = (0,0)
        #Create the main window
        self.root = self.createMainWindow()
        self.place_buttons(TOOLBAR_LAYOUT,self.toolbar_frame)
        self.dimensions_bar_setup()

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
        self.dimensions_bar_frame = Frame(root,bg="light grey")
        self.dimensions_bar_frame.grid(row=1,column=0,sticky="news")
        
        #Establish design frame where the user will be able to draw on the canvas
        self.design_frame = Frame(root,bg="red")
        self.design_frame.grid(row=2,column=0,sticky="news")
        
        #Establish the Tkinter canvas for drawing on
        self.design = Canvas(self.design_frame,width=CANVAS_SIZE[0],height=CANVAS_SIZE[1],bg="white")
        self.design.grid(row=1,column=0)
        return root
    

    def dimensions_bar_setup(self):
        self.dimension_val = StringVar()
        self.dimensions_label = Label(self.dimensions_bar_frame,textvariable=self.dimension_val,bg="light grey")
        self.dimensions_label.pack(side=LEFT)
        self.update_dimensions()


    #Called when mouse down
    def mouseDown(self,event):
        if self.drawing_type != "":
            self.mouse_down_event = event
            self.is_drawing = True
            self.current_vertices = [0,0,0,0,0,0]
            #Create temp shape for design guide
            self.temp_shape = self.design.create_polygon(*self.current_vertices, outline='black', fill='', dash=(4, 2))
            pass

    #Called when mouse released
    def mouseUp(self,event):
        if self.is_drawing == True:
            self.mouse_up_event = event
            self.is_drawing = False
            rect = self.design.create_polygon(*self.current_vertices, outline='black', fill='')
            print(rect)
            #Create shape info to store
            new_shape = Shape(self.drawing_type,self.convert_coordinates_format(self.current_vertices),rect,"None")
            self.all_polygons.append(new_shape)
            pass    
    #Called when mouse is moved over the canvas
    def mouseDrag(self,event):
        self.mouse_pos = (self.clamp(event.x,0,CANVAS_SIZE[0]),self.clamp(event.y,0,CANVAS_SIZE[1]))
        if self.is_drawing == True:
            x0,y0 = (self.mouse_down_event.x,self.mouse_down_event.y)
            x1,y1 = self.mouse_pos
            shape_vertices = []
            #Set the vertices depending on selected shape
            match(self.drawing_type):
                case "RECTANGLE":
                    shape_vertices = [x0,y0,x1,y0,x1,y1,x0,y1]
                case "TRIANGLE":
                    shape_vertices = [x0,y0,x1,y1,x0,y1]
                case "LINE":
                    shape_vertices = [x0,y0,x1,y1]


            #Resize current shape to be new size
            self.design.coords(self.temp_shape,*shape_vertices)                    
            self.current_vertices = shape_vertices  

        self.update_dimensions()
    #Place buttons from dictionary        
    def place_buttons(self,to_be_placed:dict,frame:Frame):
        self.all_buttons = []
        for index,key in enumerate(to_be_placed):
            print(key)
            to_be_placed[key] = (PhotoImage(file=IMAGE_FOLDER_PATH+to_be_placed[key]))
            self.all_buttons.append(Button(frame,image=to_be_placed[key],command=lambda k=key:self.button_commands(k)))
            self.all_buttons[-1].grid(row=0,column=index)
    def update_dimensions(self):
        #Unrounded mouse pos
        ur_x0,ury0 = self.convert_point_to_mm(self.mouse_pos)
        x0,y0 = self.convert_point_to_mm(self.mouse_pos)
        text = f"Position(mm): {(x0,y0)} "
        if self.is_drawing == True:
            #Unrounded mouse pos
            start_mouse_pos = (self.mouse_down_event.x,self.mouse_down_event.y)
            ur_x1,ury1 = self.convert_point_to_mm(start_mouse_pos)
            x1,y1 = self.convert_point_to_mm(start_mouse_pos)
            xy_scale = (ur_x0-ur_x1,ury0-ury1)
            text = text+f"Scale(mm): {(round(x0-x1,2),round(y0-y1,2))} "
            if self.drawing_type == "LINE":
                text = text+f"Length(mm): {round(math.sqrt((xy_scale[0]**2)+(xy_scale[1]**2)),2)}"
        self.dimension_val.set(text)
    
    def convert_point_to_mm(self,point):
        mm_size = AN_SIZES[self.current_paper_size][1]

        pxpmm_x = CANVAS_SIZE[0]/mm_size[0]
        pxpmm_y = CANVAS_SIZE[1]/mm_size[1]
        #Converts pixel coord to mm
        mm_point = (point[0]/pxpmm_x,point[1]/pxpmm_y)
        mm_point = (self.clamp(mm_point[0],0,mm_size[0]),self.clamp(mm_point[1],0,mm_size[1]))
        return mm_point
    #Converts coordinates from each value being its own item to tuples of coords
    def convert_coordinates_format(self,inital_coords):
        #tkinter likes each value as its own item in a list
        #PIL likes tuples of coordinates
        tuple_coords = []
        for i in range(len(inital_coords),2):
            tuple_coords.append((inital_coords[i],inital_coords[i+1]))
        return tuple_coords

    def button_commands(self,command):
        match(command):
            case "CONFIGURE":
                pass
            case _:
                self.drawing_type = command

    def clamp(self,val,lower,upper):
        return round(max(lower,min(val,upper)),2)

            
            

window = Drawer()
window.root.mainloop()