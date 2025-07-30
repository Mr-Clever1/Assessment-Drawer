#RedrawerComponent
#Paired with SchematicDrawer.py
#30/07/2025
#James Burt
from PIL import Image,ImageDraw
def tkinter_to_PIL(self):
    print(self.all_polygons)
    if self.configure_window != None:
        if self.configure_window.winfo_exists() == False:
            file = Image.new("RGB",self.CANVAS_SIZE,"white")
            draw = ImageDraw.Draw(file)
            print(self.all_polygons[0].vertices)
            for polygon in self.all_polygons:
                print(polygon.vertices)
                draw.polygon(polygon.vertices,outline="black")
            file.save("MyImage.png")
            file.show()
        else:
            print("Open")
        pass