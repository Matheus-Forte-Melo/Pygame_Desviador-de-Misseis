import pygame
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Desviador de Mísseis')

# Carregando imagens para utilização posterior
player_img = pygame.image.load("Jato.png").convert()
player_img.set_colorkey((0, 0, 0), RLEACCEL)
player_img = pygame.transform.scale(player_img, (100, 100))

enemy_img = pygame.image.load("Missel vermelho.png").convert()
enemy_img.set_colorkey((0, 0, 0), RLEACCEL)
enemy_img = pygame.transform.scale(enemy_img, (120, 40))

cloud_img_1 = pygame.image.load("Nuvem1.png").convert()
cloud_img_1.set_colorkey((0, 0, 0), RLEACCEL)
cloud_img_1 = pygame.transform.scale(cloud_img_1, (100, 40))

cloud_img_2 = pygame.image.load("Nuvem2.png").convert()
cloud_img_2.set_colorkey((0, 0, 0), RLEACCEL)
cloud_img_2 = pygame.transform.scale(cloud_img_2, (100, 40))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = random.randint(8, 15)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.speed = random.randint(1, 5)
        self.load_random()

    def load_random(self):
        random_cloud = random.randint(0, 1)

        if random_cloud == 0:
            self.image = cloud_img_1
        else:
            self.image = cloud_img_2

        self.rect = self.image.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Cria um grupo para todos os sprites e inimigos
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 350)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 2000)

# Variável para manter o loop principal funcionando
FPS = 60
clock = pygame.time.Clock()
running = True

# Loop principal
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    screen.fill((100, 148, 255))

    # Obtém todas as teclas pressionadas no momento
    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    enemies.update()
    clouds.update()

    # Verifica colisão entre jogador e inimigos
    if pygame.sprite.spritecollideany(player, enemies, collided=pygame.sprite.collide_mask):
        player.kill()
        running = False

    # Desenha todos os sprites na tela
    for entity in all_sprites:
        if entity != player:
            screen.blit(entity.image, entity.rect)

    screen.blit(player.image, player.rect)

    # Atualiza a tela
    pygame.display.flip()

pygame.quit()
