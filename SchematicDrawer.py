#16/07/2025
#Schematic Drawer
#James Burt
from tkinter import *
import RedrawerComponent 
import MeasurementComponent 
import ConfigurationComponent
import math
#Define program constants

#Defines image names and folder that they're in
IMAGE_FOLDER_PATH = r"Toolbar_Icons/"
TOOLBAR_LAYOUT = {
    "CONFIGURE":"SETTINGS.png",
    "PRINT":"PRINT.png",
    "RECTANGLE":"RECTANGLE.png",
    "ELIPSE":"ELIPSE.png",
    "TRIANGLE":"TRIANGLE.png",
    "LINE":"LINE.png",
    "DELETE":"DELETE.png"

}



#Stores all of the information I require about each polygon on the canvas
class Shape:
    def __init__(self,type,vertices,rect,colour,area) -> None:
        self.type = type
        self.vertices = vertices
        self.rect = rect
        self.colour = colour
        self.area = area
        pass


class Drawer:
    def __init__(self) -> None:
        #Establish basic drawing information
        self.current_shape = None
        self.drawing_type = ""
        self.current_vertices = []
        self.is_drawing = False
        self.current_paper_size = 4
        self.real_scale = 100
        self.CONFIG_SCALE = 100
        self.all_polygons = []
        self.all_coordinates = []
        self.current_area = 0
        #Paper Sizes, sizes in pixles then mm
        self.AN_SIZES = {
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
        print("click")
        if self.drawing_type != "" and self.drawing_type != "DELETE":
            self.mouse_down_pos = (event.x,event.y)
            self.is_drawing = True
            self.current_vertices = [0,0,0,0,0,0]
            #Create temp shape for design guide
            self.current_shape = self.design.create_polygon(*self.current_vertices, outline='black', fill='', dash=(4, 2))
            pass
        elif self.drawing_type == "DELETE":

            # self.find_bounding(event.x,event.y)
            overlapping = self.design.find_overlapping(event.x, event.y,event.x, event.y)
            for overlap_shape in overlapping:
                bounding = self.design.coords(overlap_shape)
                inside_check = self.design.find_overlapping(bounding[0], bounding[1],bounding[2], bounding[3])
                for other_shapes in overlapping:
                    if other_shapes in inside_check:
                        pass
                    else:
                        print(f"Topmost rect is: {other_shapes}")

            # smallest = Shape("RECTANGLE",[0,0,self.CANVAS_SIZE[0],self.CANVAS_SIZE[1]],0,None,math.inf)
            # for shape in self.all_polygons:
            #     if shape.rect in overlapping and shape.area < smallest.area:
            #         smallest = shape
            # if smallest.area != math.inf:
            #     self.delete_shape(smallest)
            #     print("Deleted")
            
            

    #Called when mouse released
    def mouseUp(self,event):
        if self.is_drawing == True:
            self.mouse_up_event = event
            self.is_drawing = False
            self.design.itemconfigure(self.current_shape, outline="black",dash=(), width=1)
            #Create shape info to store
            print(self.convert_coordinates_format(self.current_vertices))
            new_shape = Shape(self.drawing_type,self.convert_coordinates_format(self.current_vertices),self.current_shape,"None",self.current_area)
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
                    self.current_area = abs(x1*y1)
                case "TRIANGLE":
                    shape_vertices = [x0,y0,x1,y1,x0,y1]
                    self.current_area = abs(0.5*x1*y1)
                case "LINE":
                    shape_vertices = [x0,y0,x1,y1]
                case "ELIPSE":                    

                    shape_vertices = []
                    center_x = (self.mouse_pos[0]+self.mouse_down_pos[0])/2
                    center_y = (self.mouse_pos[1]+self.mouse_down_pos[1])/2
                    radius_x = abs(self.mouse_pos[0]-self.mouse_down_pos[0])/2
                    radius_y = abs(self.mouse_pos[1]-self.mouse_down_pos[1])/2
                    self.current_area = abs(radius_y*radius_x*math.pi)
                    num_points = 30
                    for i in range(num_points):
                        angle = 2 * math.pi * i / num_points
                        x = center_x + radius_x * math.cos(angle)
                        y = center_y + radius_y * math.sin(angle)
                        shape_vertices.append(x)
                        shape_vertices.append(y)

            #Resize current shape to be new size
            self.design.coords(self.current_shape,*shape_vertices)                    
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
                ConfigurationComponent.create_configure_window(self)
                pass
            case "PRINT":
                if self.configure_window != None and self.configure_window.winfo_exists() == False:
                    RedrawerComponent.tkinter_to_PIL(self,self.all_polygons,self.CONFIG_SCALE/self.real_scale)
                else:
                    #Creates a black line that is roughly 100mm across
                    config_x,config_y = MeasurementComponent.convert_mm_to_point(self,(self.CONFIG_SCALE,self.CONFIG_SCALE))
                    config_offset = 40
                    config_coords = [(config_offset,config_offset),(config_x+config_offset,config_offset)]
                    config_shape = Shape("LINE",config_coords,0,None)
                    RedrawerComponent.tkinter_to_PIL(self,[config_shape],1)
            case _:
                self.drawing_type = command
        

    def delete_shape(self,shape):
        self.all_polygons.remove(shape)
        self.design.delete(shape.rect)    
    def clamp(self,val,lower,upper):
        return round(max(lower,min(val,upper)),2)

            
            

window = Drawer()
window.root.mainloop()