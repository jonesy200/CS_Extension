import pygame
import random
import math


pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

running = True

vertices = []
lines = []

class Vertex:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = (255,255,255)

    def draw(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y),6)

class Laser:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.colour = (255,0,0)

    def draw(self):
        pygame.draw.line(screen, self.colour, (self.start.x, self.start.y), (self.end.x, self.end.y), 3)

def leftmost_point(points):
    leftmost = points[0]
    for point in points:
        if point.x < leftmost.x:
            leftmost = point
    return leftmost

def orientation(a, b, c):
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

def gift_wrap(points):
    perimeter = []
    start = leftmost_point(points)
    current = start

    while True:
        perimeter.append(current)
        candidate = points[0]
        if candidate == current:
            candidate = points[1]
        for point in points:
            turn = orientation(current, candidate, point)
            if turn > 0:
                candidate = point
        current = candidate
        if current == start:
            break

    return perimeter

def add_vertex_and_wrap():
    global lines

    vertices.append(
        Vertex(random.randint(50,750),
               random.randint(50,550))
    )

    if len(vertices) >= 3:
        lines = []

        perimeter = gift_wrap(vertices)

        for i in range(len(perimeter)):
            start = perimeter[i]
            end = perimeter[(i + 1) % len(perimeter)]

            lines.append(Laser(start, end))

while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                vertices.append(Vertex(random.randint(50,750), random.randint(50,550)))
            if event.key == pygame.K_q and len(vertices) >= 3:
                lines = []
                perimeter = gift_wrap(vertices)
                for i in range(len(perimeter)):
                    start = perimeter[i]
                    end = perimeter[(i + 1) % len(perimeter)]
                    lines.append(Laser(start, end))
            if event.key == pygame.K_c:
                vertices = []
                lines = []
            if event.key == pygame.K_e:
                for _ in range(100):
                    add_vertex_and_wrap()

    for vertex in vertices:
        vertex.draw()
    for line in lines:
        line.draw()
    pygame.display.update()

    clock.tick(60)

pygame.quit()