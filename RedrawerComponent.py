#RedrawerComponent
#Paired with SchematicDrawer.py
#30/07/2025
#James Burt
from PIL import Image,ImageDraw

#Called when attempting to print an image
def tkinter_to_PIL(self,shapes,scale):
    #Creates a new file and canvas
    file = Image.new("RGB",self.canvas_size,"white")
    draw = ImageDraw.Draw(file)
    #Loops through every existing shape and redraws them onto the new canvas
    for polygon in shapes:
        for index,vertex in enumerate(polygon.vertices):
            #Creates a adjusts the list item to be scaled correctly
            polygon.vertices[index] = (vertex[0]*scale,vertex[1]*scale)

        if polygon.colour == "":
            polygon.colour = None
        #Draws onto new canvas
        draw.polygon(polygon.vertices,outline="black",fill=polygon.colour)
    #Scales drawing to be desired paper size
    file = file.resize(self.AN_SIZES[self.current_paper_size][0])

    #Saves and opens image
    file.save("MyImage.png")
    file.show()

