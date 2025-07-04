import pygame
import sys
import random

WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
BROWN = (139, 69, 19)

class GameSettings:
    def __init__(self):
        self.volume = 0.5

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

class Trash(pygame.sprite.Sprite):
    TYPES = [
        ("Banane", BROWN, "Bio"),
        ("Flasche", BLUE, "Wertstoff"),
        ("Papier", WHITE, "Papier"),
    ]

    def __init__(self):
        super().__init__()
        self.kind, color, self.bin = random.choice(self.TYPES)
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect(
            center=(random.randint(20, WIDTH - 20), random.randint(50, HEIGHT // 2))
        )

class Bin(pygame.sprite.Sprite):
    COLORS = {
        "Bio": BROWN,
        "Wertstoff": BLUE,
        "Papier": WHITE,
    }

    def __init__(self, name, x):
        super().__init__()
        self.name = name
        self.image = pygame.Surface((80, 60))
        self.image.fill(self.COLORS[name])
        self.rect = self.image.get_rect(center=(x, HEIGHT - 30))

class WasteSortingGame:
    def __init__(self, settings):
        self.settings = settings
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Nachhaltigkeitsspiel")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)
        self.state = "menu"
        self.player = Player()
        self.trash = pygame.sprite.Group()
        self.bins = pygame.sprite.Group(
            Bin("Bio", WIDTH // 4),
            Bin("Wertstoff", WIDTH // 2),
            Bin("Papier", WIDTH * 3 // 4),
        )
        self.score = 0

    def spawn_trash(self):
        while len(self.trash) < 5:
            self.trash.add(Trash())

    def run(self):
        while True:
            if self.state == "menu":
                self.run_menu()
            elif self.state == "settings":
                self.run_settings()
            elif self.state == "game":
                self.run_game()
            else:
                pygame.quit()
                sys.exit()

    def draw_text_center(self, text, y):
        img = self.font.render(text, True, WHITE)
        rect = img.get_rect(center=(WIDTH // 2, y))
        self.screen.blit(img, rect)

    def run_menu(self):
        while self.state == "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.state = "game"
                    elif event.key == pygame.K_2:
                        self.state = "settings"
                    elif event.key == pygame.K_3:
                        self.state = "quit"
            self.screen.fill(BLACK)
            self.draw_text_center("1. Spiel starten", 200)
            self.draw_text_center("2. Einstellungen", 260)
            self.draw_text_center("3. Beenden", 320)
            pygame.display.flip()
            self.clock.tick(FPS)

    def run_settings(self):
        while self.state == "settings":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu"
            self.screen.fill(BLACK)
            self.draw_text_center("Einstellungen - ESC zum Zurückkehren", HEIGHT // 2)
            pygame.display.flip()
            self.clock.tick(FPS)

    def run_game(self):
        self.player.rect.centerx = WIDTH // 2
        self.trash.empty()
        self.score = 0
        self.spawn_trash()
        while self.state == "game":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "menu"
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            # Collision detection
            for item in list(self.trash):
                if self.player.rect.colliderect(item.rect):
                    # Determine if player is over correct bin
                    for b in self.bins:
                        if b.rect.colliderect(self.player.rect) and b.name == item.bin:
                            self.score += 1
                            self.trash.remove(item)
                            break
            self.spawn_trash()
            self.screen.fill(BLACK)
            self.bins.draw(self.screen)
            self.trash.draw(self.screen)
            self.screen.blit(self.player.image, self.player.rect)
            score_img = self.font.render(f"Punkte: {self.score}", True, WHITE)
            self.screen.blit(score_img, (10, 10))
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = WasteSortingGame(GameSettings())
    game.run()
