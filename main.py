import sys
import os
import pygame

pygame.init()
size = WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


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


all_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
terrain_spite = pygame.sprite.GroupSingle()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением \'{fullname}\' не найден')
        sys.exit()
    image = pygame.image.load(fullname)

    if color_key:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Terrain(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, terrain_spite)
        self.image = load_image('terrain.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        x, y = screen.get_size()
        self.rect.bottom = y
        self.spawnpoint1 = (220, 300)
        self.spawnpoint2 = (1500, 300)



terrain = Terrain()


class Player(pygame.sprite.Sprite):
    image = load_image('player.png')

    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites, player_sprites)
        self.image = Player.image
        self.pos = pos_x, pos_y
        self.rect = self.image.get_rect().move(self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.turn = True
        self.speed = 2

    def update(self):
        if not pygame.sprite.collide_mask(self, terrain):
            self.rect = self.rect.move(0, 4)

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.move(-1)
        elif keystate[pygame.K_d]:
            self.move(1)

    def move(self, v):
        if self.turn:
            if v > 0:
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.rect.move(self.speed * v, 0)


def main():
    global terrain
    player1 = Player(*terrain.spawnpoint1)
    player2 = Player(*terrain.spawnpoint2)
    player2.turn = False
    while True:
        screen.fill((0, 0, 0))
        draw_text('game', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                    break
                elif event.key == pygame.K_d:
                    player1.move(1)
                    player2.move(1)
        all_sprites.draw(screen)
        all_sprites.update()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main_menu()
