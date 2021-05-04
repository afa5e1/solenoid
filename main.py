import math
#wires[n] = ((xcoord,ycoord),curl); curl is current in/out
wires = [[(70,30), -1],[(85,30), -1],[(100,30), -1],[(115, 30), -1],[(130, 30), -1],[(70,60), 1],[(85,60), 1],[(100,60), 1],[(115, 60), 1],[(130, 60), 1]]

#VF[xcoord,ycoord] = [(delx,dely), mag]
vectorField = [[[(0,0), 0]]*100]*200

#Enter wires into vectorField
for i in range(0,9):
    vectorField[wires[i][0][0]][wires[i][0][1]] = [(0,0), 0]

for xcoord in range(0,200):
    if xcoord not in [70, 85, 100, 115, 130]:
        for ycoord in range(0,100):
            if ycoord not in (30,60):
                print(xcoord,ycoord)
                fieldStrengthVct = []
                for wire in wires:
                    distance = math.sqrt((xcoord-wire[0][0])**2 + (ycoord-wire[0][1])**2)
                    fieldStrength = 0.02/distance
                    try:
                        gradient = -(wire[0][0]-xcoord)/(wire[0][1]-ycoord)
                        theta = math.atan(gradient)
                        x = fieldStrength * wire[1] * math.cos(theta)
                        y = fieldStrength * wire[1] * math.sin(theta)
                    except:
                        x = 0
                        y = fieldStrength
                    fieldStrengthVct.append((x,y))
                xNet, yNet = 0, 0
                for vector in fieldStrengthVct:
                    xNet += vector[0]
                    yNet += vector[0]
                vectorField[xcoord][ycoord] = [(xNet,yNet), 0]
