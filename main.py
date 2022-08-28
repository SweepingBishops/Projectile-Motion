#!/usr/bin/env python
import math
import numpy as np
#from scipy.integrate import odeint
import matplotlib.pyplot as plt

### Constants ###
g = -10  # m/s^2
m = 0.150  # Kg
μ = 0
#################
class vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mag = math.sqrt(self.x**2 + self.y**2) 
    def __add__(self, other):
        return vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return vector(self.x*scalar, self.y*scalar)
    
    def __truediv__(self, scalar):
        return vector(self.x/scalar, self.y/scalar)


class ball():
    def __init__(self, init_vel, init_pos=[0,0]):
        self.pos = vector(init_pos[0], init_pos[1])
        self.vel = vector(init_vel[0], init_vel[1])

    def force(self):
        return self.drag() + vector(0,g)

    def drag(self):
        drag_mag = μ*self.vel.mag**2
        drag_x = -1*drag_mag * (self.vel.x / self.vel.mag)
        drag_y = -1*drag_mag * (self.vel.y / self.vel.mag)
        return vector(drag_x, drag_y)
         
    def accel(self):
        return self.force()/m

    def move(self, time):
        self.pos += self.vel
        self.vel += self.accel() * time

ball1 = ball([5,5]) 
xpos = []
ypos = []
for i in range(50):
    xpos.append(ball1.pos.x)
    ypos.append(ball1.pos.y)
    ball1.move(0.0028)

print(xpos,ypos ,sep="\n"*3)
print("H = ",max(ypos))

plt.xlabel("x")
plt.ylabel("y")
plt.plot(xpos, ypos)
plt.show()
