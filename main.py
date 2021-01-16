import sys
import pygame
from service import load_image, draw_text
from terrain import Terrain

pygame.init()
size = WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
font = pygame.font.SysFont(None, 20)


def terminate():
    pygame.quit()
    sys.exit()


def main_menu():
    click = False
    while True:

        screen.fill((0, 0, 0))
        draw_text('main menu', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(WIDTH // 2 - 100, 100, 200, 50)
        button_2 = pygame.Rect(WIDTH // 2 - 100, 250, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                main()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(FPS)


def options():
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_text('options', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        pygame.display.update()
        clock.tick(FPS)


def main():
    terrain = Terrain(screen)
    terrain.add_group(all_sprites)
    while True:
        screen.fill((0, 0, 0))
        draw_text('game', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.button == pygame.K_ESCAPE:
                    main_menu()
                    break
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main_menu()