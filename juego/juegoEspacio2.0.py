import pygame
import os

#para la vida
pygame.font.init()
#para le ruido
pygame.mixer.init()

#Tamaño de pantalla
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#Titulo del juego
pygame.display.set_caption("guerra en el espacio")

WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

#bordes del jeugo
BORDER = pygame.Rect(WIDTH/2 -5, 0, 5, HEIGHT)

#sonido cuando balas choquen
BULLET_HIT_SOUND = pygame.mixer.Sound('Grenade+1.wav')
#sonido cuando una nave dispare
BULLET_FIRE_SOUND = pygame.mixer.Sound('Shot.wav')

#darle vida a las naves
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)

#mostar quien gana
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

#Fotograma por segundo
FPS = 60
#velocidad de la nave
VEL = 5
#disparo y numero de balas max
MAX_BULLETS = 3
#velocidad balas
BALLET_VEL = 7
#


#Imagen de las naves
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 90, 70

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


#Imagen de fondo y su tamaño
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('space.png')), (WIDTH, HEIGHT))


#'x' aumenta para la derecha 'y' aumenta para abajo
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, WHITE, BORDER)
    WIN.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    red_health_text = HEALTH_FONT.render("vida: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("vida: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #izquierda (para que no te vallas del mapa)
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #derecha
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #arriba
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT -15: #abajo
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #izquierda
        red.x -= VEL 
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #derecha
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #arriba
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT -15: #abajo
        red.y += VEL


def handle_bullets(red_bullets, yellow_bullets, red, yellow):

    for bullet in yellow_bullets:
        bullet.x += BALLET_VEL
        #Comprobar si las balas se chocaron
        if red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)


    for bullet in red_bullets:
        bullet.x -= BALLET_VEL
        if yellow.colliderect(bullet):
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))

        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)





#Funcion principal
def main():

    #la nave/disparo se va a dibujar donde este el rectangulos
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300,SPACESHIP_WIDTH, SPACESHIP_HEIGHT)


    red_bullets = []
    yellow_bullets = []

    #vida de nave
    red_health = 10
    yellow_health = 10

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

            #comprueba si se dispararon balas y ver si hay menos de 3 balas generar nuevas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 +5, 10, 5 )
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 +5, 10, 5 )
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            #comprobar si la bala le pego a la nave para sacar vida
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        #cuando tenga menos de 0 una de las dos naves salga la otra como ganadora
        winner_text = ""
        if red_health <= 0:
            winner_text = "Amarilla Gana!"

        if yellow_health <= 0:
            winner_text = "Roja Gana!"

        if winner_text != "":
            draw_winner(winner_text)
            break



        #ver que teclas se tocan con pygame.key.get_pressed()
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(red_bullets, yellow_bullets, red, yellow)


        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    #main para que se pueda seguir el juego depues que una jugador pierda
    main()

#al tocar x se termina de ejecutar el programa

#Este if comprueba si el fichero se llama main
if __name__ == "__main__":
    main()


