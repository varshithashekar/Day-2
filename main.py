import pygame
import pygame_gui
import math
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((800, 600))
button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((150,50), (100, 50)),
    text='Tetrahedron',
    manager=manager
)
draw_tetrahedron = False
def draw_2d_tetrahedron(surface):
    points = [
        (400, 300),  
        (350, 400), 
        (450, 400),  
        (400, 200)  
    ]

    pygame.draw.line(surface, (255, 0, 0), points[0], points[1], 2)  
    pygame.draw.line(surface, (0, 255, 0), points[1], points[2], 2)  
    pygame.draw.line(surface, (0, 255, 0), points[2], points[0], 2) 
    pygame.draw.line(surface, (0, 0, 255), points[0], points[3], 2)  
    pygame.draw.line(surface, (255, 0, 255), points[1], points[3], 2)  
    pygame.draw.line(surface, (255, 0, 0), points[2], points[3], 2)  

running = True
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button:
                draw_tetrahedron = not draw_tetrahedron  

    manager.update(time_delta)

    screen.fill((0, 0, 0))
    if draw_tetrahedron:
        draw_2d_tetrahedron(screen)
    
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()