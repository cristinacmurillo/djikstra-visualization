import sys
import pygame
import time
import csv
import numpy

pygame.init()


class Circle:

    def __init__(self, coords, weight = 0, parent=None, stage=1):
        self.visited = True
        self.coords = coords
        self.weight = weight
        self.parent = parent
        self.stage = stage

    def visualise(self):
        pass



def drawcircles(Q, size = 600, padding = 50,resolution = 0.5 ):
    red = (255, 0, 0)
    screen = pygame.display.set_mode([size, size])
    step_size = int((size - padding * 2)/10)
    for coords in Q:
        for coord in coords:
            coord[0] = int(padding + ((coord[0] / resolution)
                                    * step_size * resolution))
            coord[1] = int((size - padding) -
                        ((coord[1] / resolution) * step_size * resolution))
            coord_i = [coord[0], coord[1]]

            pygame.draw.circle(screen, red, coord_i, 5)
    pygame.display.flip()

def display(Q, obstacles):

    resolution = 0.5

    # color palette
    black = (0, 0, 0)
    white = (255, 255, 255)
    blue = (159, 172, 230)
    red = (255, 0, 0)

    # display
    size = 600
    padding = 50
    step_size = int((size - padding * 2)/10)
    screen = pygame.display.set_mode([size, size])
    pygame.display.set_caption("Title")
    screen.fill(white)

    rect = pygame.draw.rect(
        screen, blue, [padding, padding, (size - padding * 2),  (size - padding * 2)])

    # grid drawin
    i = step_size
    for x in range(round(10 / resolution) + 1):
        pygame.draw.line(screen, black, (padding, i), ((size - padding), i), 2)
        pygame.draw.line(screen, black, (i, padding), (i, (size - padding)), 2)
        i += (step_size * resolution)


    for coord in obstacles:
        coord[0] = int(padding + ((coord[0] / resolution)
                                * step_size * resolution))
        coord[1] = int((size - padding) -
                    ((coord[1] / resolution) * step_size * resolution))
        coord_i = [coord[0], coord[1]]

        pygame.draw.circle(screen, black, coord_i, 5)

    for coord in Q:
        coord[0] = int(padding + ((coord[0] / resolution)
                                * step_size * resolution))
        coord[1] = int((size - padding) -
                    ((coord[1] / resolution) * step_size * resolution))
        coord_i = [coord[0], coord[1]]

        pygame.draw.circle(screen, red, coord_i, 5)
    pygame.display.flip()
    # x_i = [padding, size-padding] # initial position
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def map(file_directory):
    with open(file_directory, 'r') as file:
        map = csv.reader(file)
        obstacles = [r for r in map]
        objects = []
        for x in obstacles:
            coordinates = []
            length = float(x[2])
            height = float(x[3])
            origin = (float(x[0]), float(x[1]))
            heights = numpy.arange(0, height + 0.5, 0.5)
            lengths = numpy.arange(0, length + 0.5, 0.5)
            for h in heights:
                for l in lengths:
                    coordinates.append([origin[0] + l, origin[1] + h])
            objects.append(coordinates)
        return objects


def dijkstra():
    obstacles = map('mapas\map01.csv')
    obstacles_coords = [coords for obstacle in obstacles for coords in obstacle]
    origin = [3.0, 1.0]
    end = [8.0, 5.0]
    operations = [[0, 0.5], [0.5, 0], [0, -0.5], [-0.5, 0]]
    diagonal_operations = [[0.5, 0.5], [0.5, -0.5], [-0.5, -0.5], [-0.5, 0.5]]

    leading_nodes = [Circle(origin)]
    leading_coords = []
    visited = set()
    while(end not in leading_coords):
        next_nodes = []
        next_coords = []
        for leading_node in leading_nodes:
            for op in operations:
                new_coord = [leading_node.coords[0] + op[0], leading_node.coords[1] + op[1]]
                if tuple(new_coord) in visited or new_coord in obstacles_coords or new_coord[0] < 0 or new_coord[0] > 10 or new_coord[1] < 0 or new_coord[1] > 10:
                    pass
                else:
                    node = Circle(new_coord, parent=leading_node, weight = 0.5)
                    next_nodes.append(node)
                    next_coords.append(new_coord)
                visited.add(tuple(new_coord))
            for op in diagonal_operations:
                new_coord = [leading_node.coords[0] + op[0], leading_node.coords[1] + op[1]]
                if tuple(new_coord) in visited or new_coord in obstacles_coords or new_coord[0] < 0 or new_coord[0] > 10 or new_coord[1] < 0 or new_coord[1] > 10:
                    pass
                else:
                    node = Circle(new_coord, parent=leading_node, weight = 0.7)
                    next_nodes.append(node)
                    next_coords.append(new_coord)
                visited.add(tuple(new_coord))
        leading_nodes = next_nodes
        leading_coords = next_coords

    visualised_coords = []
    weight = 0
    node = leading_nodes[leading_coords.index(end)]
    while node.parent:
        visualised_coords.append(node.parent.coords)
        weight += node.weight
        node = node.parent
    
    print(visualised_coords)
    print(weight)
    return visualised_coords, obstacles_coords


d = dijkstra()
display(d[0], d[1])