import math
from colour import Color
from PIL import Image
import numpy
#wires[n] = ((xcoord,ycoord),curl); curl is current in/out
wires = [[(672,360), -1],[(816,360), -1],[(960,360), -1],[(1104, 360), -1],[(1248, 360), -1],[(672,720), 1],[(816,720), 1],[(960,720), 1],[(1104,720), 1],[(1248, 720), 1]]
wireCoords = [(672,360),(816,360),(960,360),(1104,360),(1248,360),(672,720),(816,720),(960,720),(1104,720),(1248,720)]
maxMag = 0.02454394350541714 / 10

#VF[xcoord,ycoord] = [(modulus,argument)]
vectorField = [[[(0,0)]]*1080]*1920
colourField = numpy.zeros((1920,1080,3), dtype=numpy.uint8)

#Enter wires into vectorField
for i in range(0,9):
    vectorField[wires[i][0][0]][wires[i][0][1]] = [(0,0)]

for xcoord in range(0,1920):
    for ycoord in range(0,1080):
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
            #print(xcoord, ycoord, argument*360, xNet, yNet)
            saturation = modulus/maxMag
            if saturation > 1:
                saturation = 1
            colour = Color(hsl=(argument, saturation, saturation))
        else:
            colour = Color("Black")
        colourField[xcoord,ycoord] = [colour.red*255, colour.green*255, colour.blue*255]
image = Image.fromarray(colourField)
image.save("output.png")
