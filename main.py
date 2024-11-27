import pygame, sys
import random

pygame.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

WITDH, HEIGHT = 800, 800
TILESIZE = 20
GRIDWIDTH = WITDH // TILESIZE
GRIDHEIGHT = HEIGHT // TILESIZE
FPS = 600

screen = pygame.display.set_mode((WITDH, HEIGHT))

clock = pygame.time.Clock()

def gen(num):
    return set([(random.randrange(0, GRIDHEIGHT), random.randrange(0, GRIDWIDTH))  for _ in range(num)]) #anscheinend ListComprehension

def draw_grid(positions):

    for position in positions:
        col, row = position
        top_left = (col * TILESIZE, row * TILESIZE)
        pygame.draw.rect(screen, YELLOW, (*top_left, TILESIZE, TILESIZE)) # *top_left packt die beiden Werte aus(wierd shit)

    for row in range(GRIDHEIGHT):
        pygame.draw.line(screen, BLACK, (0, row*TILESIZE), (WITDH, row * TILESIZE)) 

    for col in range(GRIDWIDTH):
        pygame.draw.line(screen, BLACK, (col * TILESIZE, 0), (col * TILESIZE, WITDH))  #x und y Koordinate

def adjust_grid(positions):
    all_neighbors = set()
    new_position = set()
    
    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors)) #verstehe ich auch nur halb

        if len(neighbors) in [2, 3]:
            new_position.add(position)

    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors)) #verstehe ich auch nur halb

        if len(neighbors) == 3:
            new_position.add(position)

    return new_position #das mit return hab ich immer noch nicht ganz begriffen

def get_neighbors(pos): #braucht eine fundierte Erklärung
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx > GRIDHEIGHT or x + dx > GRIDWIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy > GRIDHEIGHT or y + dy > GRIDWIDTH:
                continue
            if dx == 0 and dy == 0:
                continue
            neighbors.append((x + dx, y + dy))  

    return neighbors


def main():
    running = True
    playing = False
    count = 0
    update_freq = 120
     

    positions = set() #verstehe ich nicht
    positions.add((10, 10))
    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if count > 120:
            count = 0
            positions = adjust_grid(positions) #check auch das nur sehr wage

        pygame.display.set_caption("Playing along" if playing else "Not Playing right now")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                running = False
                

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILESIZE
                row = y // TILESIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos) #muss das verstehen, soll anscheindend besser als ein Array sein
                else:
                    positions.add(pos)
            
            if event.type == pygame.KEYDOWN: #Was hat dieses Schreibweise und folgende zu tun
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set() #was ist ein Set
                    playing = False

                if event.key == pygame.K_r:
                    positions = gen(random.randrange(1, 10) * GRIDWIDTH)



        screen.fill(GREY)            
        draw_grid(positions)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
