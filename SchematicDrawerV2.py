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
        self.local_aspect_ratio = self.CANVAS_SIZE[0]/self.CANVAS_SIZE[1]

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
        root.grid_rowconfigure(2,weight=1)
        root.grid_rowconfigure(3,weight=1)
        #Establish toolbar to store all of the tools useable
        self.toolbar_frame = Frame(root,bg="grey")
        for i in range(len(TOOLBAR_LAYOUT)):
            self.toolbar_frame.grid_columnconfigure(i,weight=1)
        root.grid_columnconfigure(0,weight=1)
        self.toolbar_frame.grid(row=0,column=0,sticky="news")       
        
        #Establish dimension bar to display the dimensions and mouse position
        self.dimensions_bar_frame = Frame(root,bg="light grey")
        self.dimensions_bar_frame.grid(row=1,column=0,sticky="news")
        
        #Establish design frame where the user will be able to draw on the canvas
        self.design_frame = Frame(root,bg="light grey")
        self.design_frame.grid(row=2,column=0,sticky="news")
        
        #Establish the Tkinter canvas for drawing on
        self.design = Canvas(self.design_frame,width=self.CANVAS_SIZE[0],height=self.CANVAS_SIZE[1],bg="white")
        self.design.pack(expand=True)

        self.canvas_intial_size_ratio = (self.CANVAS_SIZE[0]/root.winfo_width(),self.CANVAS_SIZE[1]/root.winfo_height())
        return root
    
    #Establish information for dimension bar 
    def dimensions_bar_setup(self):
        #Creates variable that will be the text displayed
        self.dimension_val = StringVar()
        #Text widget
        self.dimensions_label = Label(self.dimensions_bar_frame,textvariable=self.dimension_val,bg="light grey")
        #Put it in the frame(Uses pack because it's easy and there is only 1 item in this frame)
        self.dimensions_label.pack(side=LEFT)
        self.dimension_val.set(MeasurementComponent.update_dimensions(self))

    #Called when mouse down
    def mouseDown(self,event):
        #Gets the mouse location where the mouse goes down
        self.mouse_down_pos = (event.x,event.y)

        #Check if i am trying to draw a shape
        if self.drawing_type != "" and self.drawing_type != "DELETE":
            self.is_drawing = True
            self.current_vertices = [0,0,0,0,0,0]
            #Create temp shape for design guide
            self.current_shape = self.design.create_polygon(*self.current_vertices, outline='black', fill='', dash=(4, 2))
            pass
        #if i am deleting
        elif self.drawing_type == "DELETE":

            self.click_delete()

    #Pass rect of shape and returns shape object from self.all_polygons        
    def get_shape_from_rect(self,rect):
        for i in self.all_polygons:
                if i.rect == rect:
                    return i
                
        
    #Called when mouse released
    def mouseUp(self,event):
        #Check if drawing
        if self.is_drawing == True:
            #stop drawing and convert outline shape into final shape
            self.mouse_up_event = event
            self.is_drawing = False
            self.design.itemconfigure(self.current_shape, outline="black",dash=(), width=1)
            #Create shape info to store
            new_shape = Shape(self.drawing_type,self.convert_coordinates_format(self.current_vertices),self.current_shape,"None",self.current_area)
            self.all_polygons.append(new_shape)
            pass    
    #Called when mouse is moved over the canvas
    def mouseDrag(self,event):
        #Get mouse position, make sure it doesn't exceed the bounds of the canvas
        self.mouse_pos = (self.clamp(event.x,0,self.CANVAS_SIZE[0]),self.clamp(event.y,0,self.CANVAS_SIZE[1]))

        #If is drawing
        if self.is_drawing == True:

            #Rectangle from where you've dragged
            x0,y0 = self.mouse_down_pos
            x1,y1 = self.mouse_pos
            shape_vertices = []
            #Set the vertices depending on selected shape
            match(self.drawing_type):
                case "RECTANGLE":
                    #Set vertices as a rectangle configuration
                    shape_vertices = [x0,y0,x1,y0,x1,y1,x0,y1]
                case "TRIANGLE":
                    #Set vertices in a triangle configuration
                    shape_vertices = [x0,y0,x1,y1,x0,y1]
                case "LINE":
                    #Set vertices in a lin configuration
                    shape_vertices = [x0,y0,x1,y1]
                case "ELIPSE":       
                    #Calculate vertex positions              
                    shape_vertices = []
                    #Get the center position and radius
                    center_x = (self.mouse_pos[0]+self.mouse_down_pos[0])/2
                    center_y = (self.mouse_pos[1]+self.mouse_down_pos[1])/2
                    radius_x = abs(self.mouse_pos[0]-self.mouse_down_pos[0])/2
                    radius_y = abs(self.mouse_pos[1]-self.mouse_down_pos[1])/2

                    #Number of vertices to create around shape
                    num_points = 30
                    #Create vertices
                    for i in range(num_points):
                        angle = 2 * math.pi * i / num_points
                        x = center_x + radius_x * math.cos(angle)
                        y = center_y + radius_y * math.sin(angle)
                        shape_vertices.append(x)
                        shape_vertices.append(y)

            #Resize current shape to be new size
            self.design.coords(self.current_shape,*shape_vertices)                    
            self.current_vertices = shape_vertices  
        #Update the dimensions display
        self.dimension_val.set(MeasurementComponent.update_dimensions(self))

        new_size = (self.CANVAS_SIZE[0]*self.root.winfo_width()/self.canvas_intial_size_ratio[0],self.CANVAS_SIZE[1]*self.root.winfo_height()/self.canvas_intial_size_ratio[1])
        print(self.CANVAS_SIZE,self.canvas_intial_size_ratio)
        self.design.config(width=new_size[0],height=new_size[1])

    #Place buttons from dictionary        
    def place_buttons(self,to_be_placed:dict,frame:Frame):
        self.all_buttons = []
        for index,key in enumerate(to_be_placed):
            to_be_placed[key] = (PhotoImage(file=IMAGE_FOLDER_PATH+to_be_placed[key]))
            self.all_buttons.append(Button(frame,image=to_be_placed[key],command=lambda k=key:self.button_commands(k)))
            self.all_buttons[-1].grid(row=0,column=index,sticky="news")

    #Converts coordinates from each value being its own item to tuples of coords
    def convert_coordinates_format(self,inital_coords):
        #tkinter likes each value as its own item in a list
        #PIL likes tuples of coordinates
        tuple_coords = []
        for i in range(0,len(inital_coords),2):
            tuple_coords.append((inital_coords[i],inital_coords[i+1]))
        return tuple_coords

    #Called whenever a button is pressed
    def button_commands(self,command):
        match(command):
            #When configure button pressed
            case "CONFIGURE":
                ConfigurationComponent.create_configure_window(self)
                pass
            case "PRINT":
                #Open print window
                if self.configure_window != None and self.configure_window.winfo_exists() == False:
                    RedrawerComponent.tkinter_to_PIL(self,self.all_polygons,self.CONFIG_SCALE/self.real_scale)
                else:
                    #Creates a black line that is roughly 100mm across
                    config_x,config_y = MeasurementComponent.convert_mm_to_point(self,(self.CONFIG_SCALE,self.CONFIG_SCALE))
                    config_offset = 40
                    config_coords = [(config_offset,config_offset),(config_x+config_offset,config_offset)]
                    config_shape = Shape("LINE",config_coords,0,None)
                    #Open print for line
                    RedrawerComponent.tkinter_to_PIL(self,[config_shape],1)
            case _:
                #Set drawing type to clicked on shape
                self.drawing_type = command
    #Delete shape when clicked on   
    def click_delete(self):
        #Create dictionary for positions where lines intersect shapes
        x_intercepts = {}    
        y_intercepts = {}    
        #Scan length of screen at y point
        for x in range(0,self.CANVAS_SIZE[0]):
            #Find all shapes at point
            point_intercepts = self.design.find_overlapping(x, self.mouse_down_pos[1], x, self.mouse_down_pos[1])
            #See if already found point
            for intercept in point_intercepts:
                #Already discovered
                if intercept in x_intercepts:
                    #Update the shape edges
                    x_intercepts[intercept] = (x_intercepts[intercept][0],x)
                else: 
                    #Just discovered, add to list
                    x_intercepts[intercept] = (x,x)
        #Scan height of screen at x point
                    
        for y in range(0,self.CANVAS_SIZE[1]):
            #Find all shapes at point
            point_intercepts = self.design.find_overlapping(self.mouse_down_pos[0], y, self.mouse_down_pos[0], y)
            #See if already found point
            for intercept in point_intercepts:
                #Already discovered
                if intercept in y_intercepts:
                    #Update the shape edges
                    y_intercepts[intercept] = (y_intercepts[intercept][0],y)
                else: 
                    #Just discovered, add to list
                    y_intercepts[intercept] = (y,y)
        #Get all the shapes that are directly under the mouse
        point_intercepts = self.design.find_overlapping(self.mouse_down_pos[0], self.mouse_down_pos[1], self.mouse_down_pos[0], self.mouse_down_pos[1])

        #Dictionary to store the furthest edges of all shapes from the mouse
        furthest_edges = {}
        for i in x_intercepts:
            #If the shape in x_intercepts was also found in y_intercepts and I clicked on it
            if i in y_intercepts and i in point_intercepts:
                #Add all distance to all edges to list
                edges =[]
                edges.append(abs(x_intercepts[i][0]-self.mouse_down_pos[0]))
                edges.append(abs(x_intercepts[i][1]-self.mouse_down_pos[0]))
                edges.append(abs(y_intercepts[i][0]-self.mouse_down_pos[1]))
                edges.append(abs(y_intercepts[i][1]-self.mouse_down_pos[1]))
                #Find furthest edge
                furthest_edges[i] = max(edges)
                pass
        #If clicked on shape
        if len(furthest_edges)>0:
            closest = None
            distance = math.inf
            for i in furthest_edges:
                #Get nearest shape
                if furthest_edges[i]<distance:
                    closest = i
                    distance = furthest_edges[i]
            #Delete it
            self.delete_shape(self.get_shape_from_rect(closest))

    #Removes shape from self.all_polygons and removes from canvas        
    def delete_shape(self,shape):
        self.all_polygons.remove(shape)
        self.design.delete(shape.rect)    

    #Returns val if val is in between bounds otherwise returns bound
    def clamp(self,val,lower,upper):
        return round(max(lower,min(val,upper)),2)

            
            
#Runs and updates program
window = Drawer()
window.root.mainloop()