import math
from colour import Color
from PIL import Image
import numpy
#wires[n] = ((xcoord,ycoord),curl); curl is current in/out
wires = [[(140,60), -1],[(170,60), -1],[(200,60), -1],[(230, 60), -1],[(260, 60), -1],[(140,120), 1],[(170,120), 1],[(200,120), 1],[(230,120), 1],[(260, 120), 1]]
wireCoords = [(140,60),(170,60),(200,60),(230,60),(260,60),(140,120),(170,120),(200,120),(230,120),(260,120)]
maxMag = 0.02454394350541714

#VF[xcoord,ycoord] = [(modulus,argument)]
vectorField = [[[(0,0)]]*180]*400
colourField = numpy.zeros((400,180,3), dtype=numpy.uint8)

#Enter wires into vectorField
for i in range(0,9):
    vectorField[wires[i][0][0]][wires[i][0][1]] = [(0,0)]

for xcoord in range(0,400):
    for ycoord in range(0,180):
        coord = (xcoord, ycoord)
        if coord not in wireCoords:
            fieldStrengthVct = []
            for wire in wires:
                distance = math.sqrt((xcoord-wire[0][0])**2 + (ycoord-wire[0][1])**2)
                fieldStrength = 0.02/distance
                try:
                    gradient = -(wire[0][0]-xcoord)/(wire[0][1]-ycoord)
                    #gradient = (wire[0][1]-ycoord)/(wire[0][0]-xcoord)
                    theta = math.degrees(math.atan(gradient))
                    x = fieldStrength * wire[1] * math.cos(math.radians(theta))
                    y = fieldStrength * wire[1] * math.sin(math.radians(theta))
                except:
                    #x = 0
                    #y = wire[1] * fieldStrength
                    x = wire[1] * fieldStrength
                    y = 0
                fieldStrengthVct.append((x,y))
            xNet, yNet = 0, 0
            for vector in fieldStrengthVct:
                xNet += vector[0]
                yNet += vector[1]
            modulus = math.sqrt(xNet**2+yNet**2)
            try:
                argument = math.degrees(math.atan(yNet/xNet))/360
            except:
                if yNet > 0:
                    argument = 0.25
                else:
                    argument = 0.75
            vectorField[xcoord][ycoord] = [(modulus,argument)]
            saturation = modulus/maxMag
            colour = Color(hsl=(argument,saturation,0.5))
        else:
            colour = Color("Black")
        colourField[xcoord,ycoord] = [colour.red*255, colour.green*255, colour.blue*255]
image = Image.fromarray(colourField)
image.save("output.png")
