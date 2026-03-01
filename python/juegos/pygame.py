import pygame

pygame.init()
screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Test pygame")

running= True
blue = (34, 75, 145)
white = (250, 230, 176)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((blue))
    pygame.draw.rect(screen, white, (200, 200, 100, 50))
    #superficie, color, (x, y, ancho, alto))
    pygame.display.flip()
    
    pygame.quit()
