# Python code for 2D deseas spread.
"""
Created on Mar 17 2020

authors: Paulo Moura and Joel A. Pinheiro
"""

from scipy import signal
import numpy as np
import pylab 
import random
import pygame
import math
import timeit

background_colour = (255,255,255)
(width, height) = (520,420)
probinf=0.5

from Dynamic import addVectors, findParticle, collide, Particle

clock = pygame.time.Clock()
#clock.tick(60)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 8')

pygame.init()

number_of_particles = 200
number_of_particles_infected = 3
susceptible = number_of_particles - number_of_particles_infected

#difine how many particles will be isolate:
if number_of_particles %4==0:
    number_of_particles_isolated = 0.85*number_of_particles
else:
    number_of_particles_isolated = number_of_particles//(4)

my_particles = []

time=0
Number_death=0
Number_heal = 0

for n in range(number_of_particles):
    size = 2 #random.randint(10, 20)
    x = random.randint(size, width-size)
    y = random.randint(size, height-size)

    particle = Particle((x, y), size)
    particle.speed = 20*abs(np.random.normal(0,0.35, size=1)) #*random.randrange(1, 2, number_of_particles)
    particle.angle = random.uniform(0, math.pi*2)
    particle.age = abs(np.random.normal(0,0.25, size=1))
    particle.probdeath = particle.age + abs(np.random.normal(0,0.25, size=1))
    if (n<number_of_particles_isolated):
       particle.obeydecree = True
    
    if (n<number_of_particles_infected):
        particle.infected = True
        particle.colour = (255 , 0 ,0)
    my_particles.append(particle)


selected_particle = None
running = True
start = timeit.timeit()
while running:
    for particle in my_particles:
        if particle.infected == False and particle.immunity == False:
            particle.probinfected = abs(np.random.normal(0.5, 0.1, size=1))
           

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.1

    screen.fill(background_colour)

    
    Total_Number_infected = 0
    Number_infected = 0
 
    for i, particle in enumerate(my_particles):
        particle.move()
        particle.bounce()
        for particle2 in my_particles[i+1:]:
             collide(particle, particle2)
        particle.display()
    

#Counting the number of infected and infection days: 
    for particle in my_particles:
        if particle.infected == True:
            Number_infected += 1
            particle.timeinfection += 1
            Total_Number_infected += 1
            

#Know if the particle will recover or die within (particle.timeinfection) days:
    for particle in my_particles:
        if particle.infected == True and particle.timeinfection==14:
            if (particle.probdeath>=0.5):
                particle.colour = (255,255,255)
                particle.live = False
                particle.immunity = False
                particle.probinf = 0
                particle.infected = False
                particle.speed = 0
                Number_death += 1
                Number_infected -= 1

            elif (particle.probdeath<0.5):
               particle.live = True
               particle.immunity = True
               particle.probinf = 0
               particle.infected = False
               particle.colour = (0,255,0)
               Number_heal += 1
               Number_infected -= 1
               

        if time==20000:
            # probinf=0.5
           if particle.obeydecree==True:
             particle.isolation= False
             particle.probinf = 0
             particle.colour = (255 , 0,255)
           elif particle.obeydecree==False:
             particle.isolation= False
             particle.probinf = 0.6
              #particle.colour = (255 , 0,255)


        if susceptible>0:
           susceptible = number_of_particles - Number_infected - Number_heal - Number_death

     
#scale of time:
    if time%1==0:
        print(time,Number_infected, Number_death,Number_heal, susceptible, Total_Number_infected)
       
 
#Stop when all particles are infected
    if time==150:       
       running = False
       
    time+= 1
    
    pygame.display.flip()




#Output
last=pygame.time.get_ticks()

t = int(last)/1000
t_min = t/60

f= open("Run_Time","w+")
f.write("Time to run in seconds was %d\r" % t)
f.write("Time to run in minutes was %d\r" % t_min)

f.close()  

#Unidade de tempo Time to run / 

""" 2000 partículas a densidade é 7396 km² 
para a simulação fizemos 1pxs = m²
a área paras as 6000 partículas tem que ser  811.249 pxs
aproximadamente 852 x 952""" 
