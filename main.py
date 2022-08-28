#!/usr/bin/env python
import math
import numpy as np
import matplotlib.pyplot as plt

### Constants ###
g = -9.8  # m/s^2
m = 0.150  # Kg
μ = 0.003
TIME_STEP = 0.00001
INIT_VEL = [4, 3]
INIT_POS = [0, 0]
#################
class vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mag = math.sqrt(self.x**2 + self.y**2)

    def __add__(self, other):
        return vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return vector(self.x / scalar, self.y / scalar)


class object:
    def __init__(self, init_vel, init_pos=[0, 0], friction=True):
        self.pos = vector(init_pos[0], init_pos[1])
        self.vel = vector(init_vel[0], init_vel[1])
        self.friction = friction

    def force(self):
        if self.friction:
            return self.drag() + vector(0, m * g)
        else:
            return vector(0, m * g)

    def drag(self):
        drag_mag = μ * (self.vel.mag**2)
        drag_x = -1 * drag_mag * (self.vel.x / self.vel.mag)
        drag_y = -1 * drag_mag * (self.vel.y / self.vel.mag)
        return vector(drag_x, drag_y)

    def accel(self):
        return self.force() / m

    def move(self, time):
        self.pos += self.vel * time
        self.vel += self.accel() * time


def get_points(init_vel, init_pos=[0, 0]):
    ball = object(init_vel, init_pos)
    xpos = []
    ypos = []
    xpos.append(ball.pos.x)
    ypos.append(ball.pos.y)
    ball.move(TIME_STEP)
    while ball.pos.y >= 0:
        xpos.append(ball.pos.x)
        ypos.append(ball.pos.y)
        ball.move(TIME_STEP)

    ball1 = object(init_vel, init_pos, friction=False)
    xpos1 = []
    ypos1 = []
    xpos1.append(ball1.pos.x)
    ypos1.append(ball1.pos.y)
    ball1.move(TIME_STEP)
    while ball1.pos.y >= 0:
        xpos1.append(ball1.pos.x)
        ypos1.append(ball1.pos.y)
        ball1.move(TIME_STEP)
    return xpos, ypos, xpos1, ypos1


xpos, ypos, xpos1, ypos1 = get_points(INIT_VEL, INIT_POS)

plt.xlabel("x -->")
plt.ylabel("y -->")
plt.plot(xpos, ypos, ",-k", xpos1, ypos1, ",--k")
plt.show()
