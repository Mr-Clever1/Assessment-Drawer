#RedrawerComponent
#Paired with SchematicDrawer.py
#30/07/2025
#James Burt
from PIL import Image,ImageDraw

def tkinter_to_PIL(self,shapes,scale):
    file = Image.new("RGB",self.CANVAS_SIZE,"white")
    draw = ImageDraw.Draw(file)
    for polygon in shapes:
        for index,vertex in enumerate(polygon.vertices):
            print(vertex,scale)
            polygon.vertices[index] = (vertex[0]*scale,vertex[1]*scale)
        draw.polygon(polygon.vertices,outline="black")
    print(self.AN_SIZES[self.current_paper_size][0])
    file = file.resize(self.AN_SIZES[self.current_paper_size][0])
    file.save("MyImage.png")
    file.show()

