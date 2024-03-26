#DNA Helix simulation

import pygame as pg
import numpy as np
from math import sin, cos

WIDTH = 1920
HEIGHT = 1080

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 191, 255)

pg.init()

clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT))


class Projection:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pg.display.set_mode((width, height))
        self.background = BLACK
        self.surfaces = {}

    def addSurface(self, name, surface):
        self.surfaces[name] = surface

    def drawCircle(self):
        for surface in self.surfaces.values():
            for j, node in enumerate(surface.nodes):
                if j % 4 == 0:
                    pg.draw.circle(self.screen, GREEN, (WIDTH / 2 + int(node[0]), int(node[2])), 5)
                elif j % 4 == 1:
                    pg.draw.circle(self.screen, YELLOW, (WIDTH / 2 + int(node[0]), int(node[2])), 5)
                elif (j + 2) % 4 == 0:
                    pg.draw.circle(self.screen, YELLOW, (WIDTH / 2 + int(node[0]), int(node[2])), 5)
                elif (j + 2) % 4 == 1:
                    pg.draw.circle(self.screen, GREEN, (WIDTH / 2 + int(node[0]), int(node[2])), 5)

    def rotateZ(self, theta):
        for surface in self.surfaces.values():
            center = surface.findCentre()

            c = np.cos(theta)
            s = np.sin(theta)

            matrix = np.array([[c, -s, 0, 0],
                               [s, c, 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])

            surface.rotate(center, matrix)


class Object:
    def __init__(self):
        self.nodes = np.zeros((0, 4))

    def addNodes(self, node_array):
        ones_column = np.ones((len(node_array), 1))
        ones_added = np.hstack((node_array, ones_column))
        self.nodes = np.vstack((self.nodes, ones_added))

    def findCentre(self):
        mean = self.nodes.mean(axis=0)
        return mean

    def rotate(self, center, matrix):
        for i, node in enumerate(self.nodes):
            self.nodes[i] = center + np.matmul(matrix, node - center)

        for m in range(0, 200, 4):
            drawLine(m, m + 1, self.nodes, GREEN, RED)

        for m in range(2, 200, 4):
            drawLine(m, m + 1, self.nodes, YELLOW, BLUE)


def drawLine(i, j, k, color1, color2):
    a = k[i]
    b = k[j]
    c = (a[0] + b[0]) / 2
    pg.draw.line(screen, color1, (WIDTH / 2 + a[0], a[2]), (WIDTH / 2 + c, b[2]), 3)
    pg.draw.line(screen, color2, (WIDTH / 2 + c, a[2]), (WIDTH / 2 + b[0], b[2]), 3)


helix1 = []
helix2 = []

for t in range(200):
    x = round(60 * cos(3 * t), 0)
    y = round(60 * sin(3 * t), 0)
    z = 14 * t
    helix1.append((x, y, z))

for t in range(200):
    x = round(60 * -cos(3 * t), 0)
    y = round(60 * -sin(3 * t), 0)
    z = 14 * t
    helix2.append((x, y, z))

double_helix = [j for i in zip(helix1, helix2) for j in i]

spin = 0

running = True
while running:

    clock.tick(60)

    pv = Projection(WIDTH, HEIGHT)

    dna = Object()
    dna_nodes = [i for i in double_helix]
    dna.addNodes(np.array(dna_nodes))

    pv.addSurface('DNA', dna)
    pv.rotateZ(spin)
    pv.drawCircle()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    pg.display.update()
    spin += 0.02
