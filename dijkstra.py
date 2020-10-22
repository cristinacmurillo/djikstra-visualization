import sys, pygame, time, csv, numpy

pygame.init()

def display(Q):

    resolution = 0.5

    #color palette 
    black = (0, 0, 0)
    white = (255, 255, 255)
    blue =  (159, 172, 230)
    red =   (255, 0, 0)

    #display
    size = 600
    padding = 50
    step_size = int((size - padding * 2)/10)
    screen = pygame.display.set_mode([size,size])
    pygame.display.set_caption("Title")
    screen.fill(white)

    rect = pygame.draw.rect(screen, blue, [padding, padding, (size - padding * 2),  (size - padding * 2)])

    #grid drawin
    i = step_size
    for x in range (round(10 / resolution) + 1):
        pygame.draw.line(screen, black, (padding,i), ((size - padding), i), 2)
        pygame.draw.line(screen, black, (i,padding), (i, (size - padding)), 2)
        i += (step_size * resolution)

    #x_i = [padding, size-padding] # initial position

    for coords in Q:
        for coord in coords:
            coord[0] = int(padding + ((coord[0] / resolution) * step_size * resolution))
            coord[1] = int((size - padding) - ((coord[1] / resolution) * step_size * resolution))
            coord_i = [coord[0], coord[1]]
            
            pygame.draw.circle(screen, red, coord_i, 5)
            pygame.display.flip()
            #time.sleep(.5)
    
    pygame.display.flip()

    while(True):  
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

def map(file_directory):
     with open (file_directory,'r') as file:
        map = csv.reader(file)
        obstacles = [r for r in map]
        objects = []
        for x in obstacles:
            coordinates = []
            length = float(x[2])
            height = float(x[3])
            origin = (float(x[0]), float(x[1]))
            heights = numpy.arange(0, height + 0.5 , 0.5)
            lengths = numpy.arange(0, length + 0.5, 0.5)
            for h in heights:
                for l in lengths:
                    coordinates.append([origin[0] + l, origin[1] + h])
            objects.append(coordinates)
        return objects

def djikstra():
    obstacles = map('mapas\map02.csv')

    

    return obstacles
    


Q = djikstra()
display(Q)