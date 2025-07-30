#16/07/2025
#Schematic Drawer
#James Burt
from tkinter import *
from tkinter import messagebox
import math
import RedrawerComponent 
import MeasurementComponent 
#Define program constants

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

        #How big the canvas will be in the program, has to maintain this ratio of 1:√2
        self.CANVAS_SIZE = (437, 614)
        self.mouse_pos = (0,0)
        self.mouse_down_pos = (0,0)
        #Create the main window
        self.root = self.createMainWindow()
        self.place_buttons(TOOLBAR_LAYOUT,self.toolbar_frame)
        self.dimensions_bar_setup()

        #Create configure window and then hide it away
        self.configure_window = Toplevel(self.root)
        self.configure_window.destroy()

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
        self.design = Canvas(self.design_frame,width=self.CANVAS_SIZE[0],height=self.CANVAS_SIZE[1],bg="white")
        self.design.grid(row=1,column=0)
        return root
    

    def dimensions_bar_setup(self):
        self.dimension_val = StringVar()
        self.dimensions_label = Label(self.dimensions_bar_frame,textvariable=self.dimension_val,bg="light grey")
        self.dimensions_label.pack(side=LEFT)
        self.dimension_val.set(MeasurementComponent.update_dimensions(self))

    #Called when mouse down
    def mouseDown(self,event):
        if self.drawing_type != "":
            self.mouse_down_pos = (event.x,event.y)
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
            #Create shape info to store
            print(self.convert_coordinates_format(self.current_vertices))
            new_shape = Shape(self.drawing_type,self.convert_coordinates_format(self.current_vertices),rect,"None")
            self.all_polygons.append(new_shape)
            pass    
    #Called when mouse is moved over the canvas
    def mouseDrag(self,event):
        self.mouse_pos = (self.clamp(event.x,0,self.CANVAS_SIZE[0]),self.clamp(event.y,0,self.CANVAS_SIZE[1]))
        if self.is_drawing == True:
            x0,y0 = self.mouse_down_pos
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

        self.dimension_val.set(MeasurementComponent.update_dimensions(self))
    #Place buttons from dictionary        
    def place_buttons(self,to_be_placed:dict,frame:Frame):
        self.all_buttons = []
        for index,key in enumerate(to_be_placed):
            to_be_placed[key] = (PhotoImage(file=IMAGE_FOLDER_PATH+to_be_placed[key]))
            self.all_buttons.append(Button(frame,image=to_be_placed[key],command=lambda k=key:self.button_commands(k)))
            self.all_buttons[-1].grid(row=0,column=index)

    #Converts coordinates from each value being its own item to tuples of coords
    def convert_coordinates_format(self,inital_coords):
        #tkinter likes each value as its own item in a list
        #PIL likes tuples of coordinates
        tuple_coords = []
        for i in range(0,len(inital_coords),2):
            tuple_coords.append((inital_coords[i],inital_coords[i+1]))
            print("t",tuple_coords)
        return tuple_coords

    #Called whenever a button is pressed
    def button_commands(self,command):
        match(command):
            #When configure button pressed
            case "CONFIGURE":
                #Create secondary window at make it always at the top
                self.configure_window = Toplevel(self.root)
                self.configure_window.attributes('-topmost', True)

                #Create entry box to take in the paper size value
                self.paper_size_val  =  StringVar()
                self.paper_size_entry = Entry(self.configure_window,textvariable=self.paper_size_val)
                self.paper_size_entry.insert("0",f"{self.current_paper_size}")

                #Call function whenever you click off of the entry box
                self.paper_size_entry.bind("<FocusOut>", self.entry_edited)
                self.paper_size_entry.grid(row=0,column=0)

                self.configure_print_button = Button(self.configure_window,command=lambda:self.button_commands("PRINT"))
                self.configure_print_button.grid(row=0,column=1)
                pass
            case "PRINT":
                print("f",self.all_polygons[0].vertices)
                RedrawerComponent.tkinter_to_PIL(self)
            case _:
                self.drawing_type = command
    def entry_edited(self,event):
        try:         
            if self.paper_size_val.get()=="":
                raise ValueError
            else:
                size = int(self.paper_size_val.get())
                if (size < 0 or size > len(AN_SIZES)-1):
                    raise ValueError
        except ValueError:            
            messagebox.showerror("Invalid Paper Size", f"Please enter a value between 0 and {len(AN_SIZES)-1}")
            self.paper_size_val.set(f"{self.current_paper_size}")
            return None
        self.current_paper_size = size            
        
    def clamp(self,val,lower,upper):
        return round(max(lower,min(val,upper)),2)

            
            

window = Drawer()
window.root.mainloop()