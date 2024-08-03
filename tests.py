from numpy import ones,vstack,arctan,arctan2,rad2deg
from numpy.linalg import lstsq
from sympy import symbols,Eq,solve,Point, Line
import matplotlib.pyplot as plt
import time
import math

points = [(789,526),(759,554)]
x_coords, y_coords = zip(*points)
A = vstack([x_coords,ones(len(x_coords))]).T
m, c = lstsq(A, y_coords)[0]
print("Line Solution is y = {m}x + {c}".format(m=m,c=c))
x, y = symbols('x y')
eq1=Eq(y, m*x+c)
y_values = [solve(eq1)[0] for x in range(765,822)]

x1, y1 = points[0]
x2, y2 = points[1]
slope = (y2-y1)/(x2-x1)
angle = rad2deg(arctan2((y2-y1),(x2-x1)))
angle = (angle + 360) % 360; 
distance = math.sqrt(abs((points[0][0]-points[1][0])*(points[0][0]-points[1][0])) +abs((points[0][1]-points[1][1])*(points[0][1]-points[1][1])))

print(angle, distance)

endx = distance * math.cos(math.radians(angle))
endy = y1 + distance * math.sin(math.radians(angle))

print(([x1,endx], [y1,endy]))
#plt.plot([x1,endx], [y1,endy])
#plt.show()

asilx1 = x1 * math.cos(math.degrees(7*math.pi/4))
asily1 = y1 * math.sin(math.degrees(7*math.pi/4))

asilx2 = x2 * math.cos(math.degrees(7*math.pi/4))
asily2 = y2 * math.sin(math.degrees(7*math.pi/4))
print(f'asilx: {[asilx1,asily1]} , asily : {[asilx2,asily2]}')
x_lerkare = (asilx1-asilx2)*(asilx1-asilx2)
y_lerkare = (asily1-asily2)*(asily1-asily2)
asildistance = math.sqrt(abs(x_lerkare) + abs(y_lerkare))
asilangle = rad2deg(arctan2((asily2-asily1),(asilx2-asilx1)))
asilangle = (asilangle+360)%360;
print(asilangle , asildistance)
endx = asildistance * math.cos(math.radians(asilangle))
endy = asily1 + asildistance * math.sin(math.radians(asilangle))

print(([asilx1,endx], [asily1,endy]))
#plt.plot([asilx1,endx], [asily1,endy])
#plt.show()


x3,y3 = (34.5,14.5)

asilx3 =x3+ x3 * math.cos(math.degrees(math.pi/4))
asily3 =y3+ y3 * math.sin(math.degrees(math.pi/4))

print(asilx3,asily3)
