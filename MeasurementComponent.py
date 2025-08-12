#Measurement Functionality
#Paired with SchematicDrawer.py
#30/07/2025
#James Burt
import math

#Updates dimensions bar called whenever mouse moved
def update_dimensions(self):
    #Unrounded mouse pos
    x0,y0 = convert_point_to_mm(self,self.mouse_pos)
    text = f"Position(mm): {(x0,y0)} "
    if self.is_drawing == True:
        #Unrounded mouse pos
        start_mouse_pos = (self.mouse_down_pos[0],self.mouse_down_pos[1])

        #Mouse starting position
        x1,y1 = convert_point_to_mm(self,start_mouse_pos)
        #Size of shape
        xy_scale = (x0-x1,y0-y1)
        #if drawing adds the shapes dimensions
        text = text+f"Scale(mm): {(round(x0-x1,2),round(y0-y1,2))} "
        #If specifically a line, gives the lines length by calculating the hypotenuse 
        if self.drawing_type == "LINE":
            text = text+f"Length(mm): {round(math.sqrt((xy_scale[0]**2)+(xy_scale[1]**2)),2)}"
    return text

#Pass a pixel point and converts it into mm
def convert_point_to_mm(self,point):
    #Gets the size of the current paper in mm
    mm_size = self.AN_SIZES[self.current_paper_size][1]

    #See how many pixels are in each mm for the screen
    pxpmm_x = self.CANVAS_SIZE[0]/mm_size[0]
    pxpmm_y = self.CANVAS_SIZE[1]/mm_size[1]
    #Converts pixel coord to mm
    mm_point = (point[0]/pxpmm_x,point[1]/pxpmm_y)
    mm_point = (self.clamp(mm_point[0],0,mm_size[0]),self.clamp(mm_point[1],0,mm_size[1]))
    return mm_point
    
#Does oppisiote of above function, converts mm to pixels
def convert_mm_to_point(self,mm_point):
    #Gets the current paper size in mm
    mm_size = self.AN_SIZES[self.current_paper_size][1]
    #Get how many pixels there are per mm.
    pxpmm_x = self.CANVAS_SIZE[0]/mm_size[0]
    pxpmm_y = self.CANVAS_SIZE[1]/mm_size[1]
    
    #Convert to pixels
    pixel_point = (round(mm_point[0]*pxpmm_x),round(mm_point[1]*pxpmm_y))
    return pixel_point
    