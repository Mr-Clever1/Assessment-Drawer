#RedrawerComponent
#Paired with SchematicDrawer.py
#30/07/2025
#James Burt
from PIL import Image,ImageDraw

def tkinter_to_PIL(self,shapes):
    file = Image.new("RGB",self.CANVAS_SIZE,"white")
    draw = ImageDraw.Draw(file)
    for polygon in shapes:
        draw.polygon(polygon.vertices,outline="black")
    file.save("MyImage.png")
    file.show()

