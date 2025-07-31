#Measurement Functionality
#Paired with SchematicDrawer.py
#30/07/2025
#James Burt
import math

def update_dimensions(self):
    self.canvas_size = self.CANVAS_SIZE
    #Unrounded mouse pos
    ur_x0,ury0 = convert_point_to_mm(self,self.mouse_down_pos)
    x0,y0 = convert_point_to_mm(self,self.mouse_pos)
    text = f"Position(mm): {(x0,y0)} "
    if self.is_drawing == True:
        #Unrounded mouse pos
        start_mouse_pos = (self.mouse_down_pos[0],self.mouse_down_pos[1])
        ur_x1,ury1 = convert_point_to_mm(self,start_mouse_pos)
        x1,y1 = convert_point_to_mm(self,start_mouse_pos)
        xy_scale = (ur_x0-ur_x1,ury0-ury1)
        text = text+f"Scale(mm): {(round(x0-x1,2),round(y0-y1,2))} "
        if self.drawing_type == "LINE":
            text = text+f"Length(mm): {round(math.sqrt((xy_scale[0]**2)+(xy_scale[1]**2)),2)}"
    return text

def convert_point_to_mm(self,point):
    mm_size = self.AN_SIZES[self.current_paper_size][1]

    pxpmm_x = self.CANVAS_SIZE[0]/mm_size[0]
    pxpmm_y = self.CANVAS_SIZE[1]/mm_size[1]
    #Converts pixel coord to mm
    mm_point = (point[0]/pxpmm_x,point[1]/pxpmm_y)
    mm_point = (self.clamp(mm_point[0],0,mm_size[0]),self.clamp(mm_point[1],0,mm_size[1]))
    return mm_point
    
def convert_mm_to_point(self,mm_point):
    mm_size = self.AN_SIZES[self.current_paper_size][1]
    pxpmm_x = self.CANVAS_SIZE[0]/mm_size[0]
    pxpmm_y = self.CANVAS_SIZE[1]/mm_size[1]
    
    pixel_point = (round(mm_point[0]*pxpmm_x),round(mm_point[1]*pxpmm_y))
    return pixel_point
    