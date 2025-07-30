#Measurement Functionality
#Paired with SchematicDrawer.py
#30/07/2025
#James Burt
import math

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
    mm_size = AN_SIZES[self.current_paper_size][1]

    pxpmm_x = self.CANVAS_SIZE[0]/mm_size[0]
    pxpmm_y = self.CANVAS_SIZE[1]/mm_size[1]
    #Converts pixel coord to mm
    mm_point = (point[0]/pxpmm_x,point[1]/pxpmm_y)
    mm_point = (self.clamp(mm_point[0],0,mm_size[0]),self.clamp(mm_point[1],0,mm_size[1]))
    return mm_point
    
def convert_mm_to_px(self,mm):
    pass