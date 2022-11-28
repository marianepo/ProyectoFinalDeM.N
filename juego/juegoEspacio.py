import pygame
import os

pygame.font

#Tamaño de pantalla
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#Titulo del juego
pygame.display.set_caption("guerra en el espacio")

WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

#Fotograma por segundo
FPS = 60

#Funcion principal
def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        #se encarga de que este bucle se repita  60 veces por segundo (para que no se ejecute la veces que quiera) 
        clock.tick(FPS)
        
        #pygame.event.get() es una lista con todos los eventos
        #de pygame
        #esto guarda eventos como tocar una tecla
        #comproba un solo evento
        #pygame.quit()termina el juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
    #main para que se pueda seguir el juego depues que una jugador pierda
    main()

#Este if comprueba si el fichero se llama main
if __name__ == "__main__":
    main()


