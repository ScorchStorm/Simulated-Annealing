# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 21:14:55 2022

Matthew Overton ove18005@byui.edu
"""

from matplotlib import pyplot as plt
from numpy import exp
from math import sqrt
from random import random, seed, randint

N = 500 # number of cities
R = 0.02 
seed(14)

Tmax = 0.250 # starting "temperature" for the anneal
Tmin = 5e-3 # final "temperature" for the anneal
tau = 1e5 # time constant for the anneal

def mag(x):
    return sqrt(x[0]*x[0]+x[1]*x[1]) # a slightly faster way to calculate pythagorean theorem

def distance():
    d = 0.0
    for i in range(N):
        d += A[r[i-1]][r[i]] # uses lookup with the distance array to find distances
    return d

s = []
for _ in range(N): # Choose N city locations
    s.append([random(), random()])
c = s.copy()

A = [] # an array containing the distances from every point to every other point
for i in s:
    B = []
    for n in s:
        x = (i[0]-n[0])
        y = (i[1]-n[1])
        B.append((x*x + y*y) ** 0.5)
    A.append(B)

r = list(range(N))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
# points, = ax.plot([i[0] for i in s], [i[1] for i in s], 'k.', markersize = 5) # Plot little black dots at the city locations if you'd like
line1, = ax.plot([])
line2, = ax.plot([])
line3, = ax.plot([])
text = ax.text(0.1,1.02, "", fontsize=12)
ax.set(xlim=(0,1), ylim=(0,1.1))
ax.set_aspect('equal')
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
fig.canvas.draw()
ax2background = fig.canvas.copy_from_bbox(ax.bbox)
plt.show(block=False)

tpoints = []
Tpoints = []
Dispoints = []

t = 0
T = Tmax

tpoints.append(t)
Tpoints.append(T)
Dispoints.append(distance())

while T>Tmin:
    
    t += 1
    T = Tmax*exp(-t/tau) # cooling step

    i,j = randint(0,N-1), randint(0,N-1)
    while i==j: # retry if they are the same
        i,j = randint(0,N-1), randint(0,N-1)

    deltaD = A[r[i-1]][r[i]] + A[r[j-1]][r[j]] - A[r[i]][r[j]] - A[r[i-1]][r[j-1]] # Calculate the change in distance

    if random()>=exp(-deltaD/T): # If the move is accepted, make the changes
        if i < j:
            r = r[:i]+r[i:j][::-1]+r[j:]
        elif j < i:
            r = r[:j]+r[j:i][::-1]+r[i:]
    if t%1000 == 0: # This plots the function every 1000 attempted moves
        s = [c[r[n-1]] for n in range(N+1)]
        line1.set_data([i[0] for i in s], [i[1] for i in s])
        line2.set_data([s[i-1][0],s[i][0],s[i+1][0]], [s[i-1][1],s[i][1],s[i+1][1]]) # This makes red lines at the location of the last attempted move
        line2.set_color('red')
        line3.set_data([s[j-1][0],s[j][0],s[j+1][0]], [s[j-1][1],s[j][1],s[j+1][1]]) # This makes red lines at the location of the last attempted move
        line3.set_color('red')
        Dis = distance()
        title = f't = {t} D = {Dis:.4f} T = {T:.3f}'
        text.set_text(title)
        fig.canvas.restore_region(ax2background)
        ax.draw_artist(line1)
        ax.draw_artist(line2)
        ax.draw_artist(line3)
        ax.draw_artist(text)
        fig.canvas.blit(ax.bbox)
        fig.canvas.flush_events()
        tpoints.append(t)
        Tpoints.append(T)
        Dispoints.append(Dis)
plt.figure(dpi = 200)
plt.plot(tpoints,Dispoints)
plt.plot(tpoints,Tpoints)
plt.title(f'Simulated Annealing - final D = {Dis:0.4f}')
plt.show()
