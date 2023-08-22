from pygame import (
    image, init, time, USEREVENT, Rect,
    display, font as pygame_font, event, quit,
    KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN,
    QUIT, K_SPACE
)
from typing import Optional, Tuple
import random

WIDTH = 600
HEIGHT = 800

BOMB_FALL_SPEED = 5
BOMB_SPAWN_TIME = 500  # ms
BOMB_RADIUS = 1.5  # Default: 1.5


class Entity:
    def __init__(self, img_name):
        self.img = image.load("assets/" + img_name)
        self.rect = self.img.get_rect()

    def blit(self, awesome_screen):
        awesome_screen.blit(self.img, self.rect)


class Girl(Entity):
    def change_img(self, img_name):
        self.img = image.load("assets/" + img_name)


class Bomb(Entity):
    def fall(self, speed):
        self.rect.top += speed


class DrawText:
    @staticmethod
    def draw_text(
            text: str,
            color: Tuple[int, int, int],
            height: int | float,
            size: Optional[int] = 50
    ) -> Rect:
        font = pygame_font.SysFont('', size)
        text_surface = font.render(text, False, color)
        text_rect = text_surface.get_rect(midtop=(WIDTH // 2, height))
        screen.blit(text_surface, text_rect)
        return text_rect  # useful to determine positioning information

    @staticmethod
    def draw_big_text(
            text: str,
            color: Tuple[int, int, int],
            height: int | float,
            size: Optional[int] = 100
    ) -> Rect:
        return DrawText.draw_text(text, color, height, size)


init()
time.set_timer(USEREVENT + 1, BOMB_SPAWN_TIME)  # Set timer for spawning bombs

screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
score = 0
game_over = False

girl = Girl("girl.png")
girl.rect.centerx = 300
girl.rect.bottom = 800

bombs = [Bomb("bomb.png")]
bombs[0].rect.left = random.randint(girl.rect.centerx - WIDTH // BOMB_RADIUS, girl.rect.centerx + WIDTH // BOMB_RADIUS)

while True:
    screen.fill((200, 200, 200))

    for e in event.get():
        if e.type == QUIT:
            quit()

        if e.type == USEREVENT + 1 and not game_over:
            new_bomb = Bomb("bomb.png")
            new_bomb.rect.left = random.randint(girl.rect.centerx - WIDTH // BOMB_RADIUS,
                                                girl.rect.centerx + WIDTH // BOMB_RADIUS)
            bombs.append(new_bomb)

        if game_over and e.type == KEYDOWN and e.key == K_SPACE:
            girl.change_img("girl.png")
            girl.rect.centerx = 300
            girl.rect.bottom = 800
            bombs = [Bomb("bomb.png")]
            bombs[0].rect.left = random.randrange(WIDTH)
            score = 0
            game_over = False
            continue

        if game_over:
            continue

        if e.type == KEYDOWN:
            SPEED = 15
            if e.key == K_LEFT:
                girl.rect.left -= SPEED
            if e.key == K_RIGHT:
                girl.rect.right += SPEED
            if e.key == K_UP:
                girl.rect.top -= SPEED
            if e.key == K_DOWN:
                girl.rect.bottom += SPEED

            if girl.rect.left < 0:
                girl.rect.left = 0
            elif girl.rect.right > WIDTH:
                girl.rect.right = WIDTH

    for bomb in bombs:
        bomb.fall(BOMB_FALL_SPEED)
        if girl.rect.colliderect(bomb.rect):
            girl.change_img("girl_dead.png")
            bombs.remove(bomb)
            game_over = True
        elif bomb.rect.top > HEIGHT:
            bombs.remove(bomb)
            if not game_over:
                score += 1

        bomb.blit(screen)

    girl.blit(screen)

    if not game_over:
        DrawText.draw_text(f'Score: {score}', (0, 0, 0), 0)
    else:
        for bomb in bombs:
            bombs.remove(bomb)
        DrawText.draw_text(f'Your Score is {score}', (100, 100, 100), HEIGHT // 3.9, 35)
        DrawText.draw_big_text('GAME OVER', (255, 0, 0), HEIGHT // 3.3)
        if time.get_ticks() % 1000 < 500:
            DrawText.draw_text('Press Space to Restart', (255, 0, 0), HEIGHT // 2.2, 40)
        if time.get_ticks() % 1000 > 500:
            DrawText.draw_text('Press Space to Restart', (164, 0, 0), HEIGHT // 2.2, 40)

    display.update()
    clock.tick(142)
