#!/usr/bin/env python
import math
import numpy as np
import matplotlib.pyplot as plt

### Constants ###
g = -9.8  # m/s^2
μ = 0.015
TIME_STEP = 0.001
INIT_VEL = 35
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
            return self.drag() + vector(0, g)
        else:
            return vector(0, g)

    def drag(self):
        drag_mag = μ * (self.vel.mag**2)
        drag_x = -1 * drag_mag * (self.vel.x / self.vel.mag)
        drag_y = -1 * drag_mag * (self.vel.y / self.vel.mag)
        return vector(drag_x, drag_y)

    def accel(self):
        return self.force()

    def move(self, time):
        self.pos += self.vel * time
        self.vel += self.accel() * time


INIT_VEL_45 = INIT_VEL / 2**0.5


def get_points_frictionless_45():
    init_vel = [INIT_VEL_45, INIT_VEL_45]
    ball = object(init_vel, INIT_POS, friction=False)
    xpos = []
    ypos = []
    xpos.append(ball.pos.x)
    ypos.append(ball.pos.y)
    ball.move(TIME_STEP)
    while ball.pos.y >= 0:
        xpos.append(ball.pos.x)
        ypos.append(ball.pos.y)
        ball.move(TIME_STEP)
    return xpos, ypos


def get_points_friction_45():
    init_vel = [INIT_VEL_45, INIT_VEL_45]
    ball = object(init_vel, INIT_POS)
    xpos = []
    ypos = []
    xpos.append(ball.pos.x)
    ypos.append(ball.pos.y)
    ball.move(TIME_STEP)
    while ball.pos.y >= 0:
        xpos.append(ball.pos.x)
        ypos.append(ball.pos.y)
        ball.move(TIME_STEP)
    return xpos, ypos


def get_points_friction_max():
    θ = 0
    max_range = [0, θ]
    while θ < math.pi / 2:
        init_vel = [INIT_VEL * math.cos(θ), INIT_VEL * math.sin(θ)]
        ball = object(init_vel, INIT_POS)
        ball.move(TIME_STEP)
        while ball.pos.y >= 0:
            ball.move(TIME_STEP)
        if ball.pos.x > max_range[0]:
            max_range[0] = ball.pos.x
            max_range[1] = θ
        θ += 0.001

    init_vel = [INIT_VEL * math.cos(max_range[1]), INIT_VEL * math.sin(max_range[1])]
    ball = object(init_vel, INIT_POS)
    xpos = []
    ypos = []
    while ball.pos.y >= 0:
        xpos.append(ball.pos.x)
        ypos.append(ball.pos.y)
        ball.move(TIME_STEP)
    return xpos, ypos, max_range[1]


xpos_wf, ypos_wf = get_points_frictionless_45()
xpos_45, ypos_45 = get_points_friction_45()
xpos, ypos, θ = get_points_friction_max()
print(f"The largest range is achieved at angle: {math.degrees(θ)} degrees")

plt.xlabel("x -->")
plt.ylabel("y -->")
plt.plot(
    xpos,
    ypos,
    ",-g",
    xpos_45,
    ypos_45,
    ",--r",
    xpos_wf,
    ypos_wf,
    ",:b",
    [0, xpos_wf[-1]],
    [0, 0],
    ",--k",
)
plt.show()
