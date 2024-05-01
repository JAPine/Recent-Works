import numpy as np
import pylab 
import random
import pygame
import math

background_colour = (255,255,255)
(width, height) = (760, 620)
drag = 1.0
elasticity = 1.0
gravity = (math.pi, 0.00000)
probinf=0.75

def addVectors(anglen1, anglen2):
    (angle1, length1) = anglen1
    (angle2, length2) = anglen2
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None


def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if p1.isolation == False and p2.isolation == False:
            if p1.live== True and p2.live==True:    
                if dist < p1.size + p2.size:
                   tangent = math.atan2(dy, dx)
                   angle = 0.5 * math.pi + tangent

                   angle1 = 2*tangent - p1.angle
                   angle2 = 2*tangent - p2.angle
                   speed1 = p2.speed*elasticity
                   speed2 = p1.speed*elasticity

                   (p1.angle, p1.speed) = (angle1, speed1)
                   (p2.angle, p2.speed) = (angle2, speed2)

                   p1.x += math.sin(angle)
                   p1.y -= math.cos(angle)
                   p2.x -= math.sin(angle)
                   p2.y += math.cos(angle)

        
                   if p1.infected==True and p2.immunity==False:
                       if p2.probinfected<=probinf:
                           if p2.probdeath<=0.1:
                              p2.infected = True
                              p2.colour = (255, 0, 0)
                           else:
                              p2.infected = True
                              p2.colour = (255, 0, 0)
                   elif p2.infected == True and p1.immunity ==False:
                       if p1.probinfected<=probinf:  
                            if p1.probdeath<=0.1:
                               p1.infected = True
                               p1.colour = (255, 0, 0)
                            else:
                               p1.infected = True
                               p1.colour = (255, 0, 0)


class Particle():
    def __init__(self, xxx, size):
        (x, y) = xxx
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 1
        self.speed = 1
        self.angle = 0
        self.infected = False
        self.probdeath = 0
        self.probinfected = 0
        self.timeinfection = 0
        self.live = True
        self.immunity = False
        self.isolation = False
        self.dayquarentine = 0
        self.obeydecree = False
        self.age = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 8')


