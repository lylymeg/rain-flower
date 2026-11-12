import pygame
import random
import math
import sys

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 950, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kawaii Cloud & Flower Garden Simulator")
clock = pygame.time.Clock()

# Couleurs (Thème Nuit Douce / Pastel Cozy)
BG_COLOR = (18, 22, 35)
GROUND_COLOR = (30, 38, 52)
CLOUD_COLOR = (235, 242, 255)
RAIN_COLOR = (100, 210, 255)
TEXT_COLOR = (240, 245, 255)
GRAY = (120, 130, 150)
FLOWER_COLORS = [
    (255, 105, 180),  # Rose Kawaii
    (255, 200, 80),   # Jaune soleil
    (180, 120, 255),  # Violet lavande
    (0, 230, 180)     # Menthe éclatante
]

# Polices
font_medium = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 14)

class Cloud:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 100

    def update(self, mouse_pos):
        # Le nuage suit doucement les mouvements horizontaux de la souris
        target_x = mouse_pos[0]
        self.x += (target_x - self.x) * 0.08
        self.x = max(80, min(WIDTH - 80, self.x))

    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        # Forme fluffy du nuage (cercles et ovale combinés)
        pygame.draw.circle(surface, CLOUD_COLOR, (cx - 30, cy + 5), 22)
        pygame.draw.circle(surface, CLOUD_COLOR, (cx + 30, cy + 5), 22)
        pygame.draw.circle(surface, CLOUD_COLOR, (cx, cy - 10), 28)
        pygame.draw.ellipse(surface, CLOUD_COLOR, (cx - 45, cy - 5, 90, 30))

class Raindrop:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(4.5, 7.5)

    def update(self):
        self.y += self.speed

class Flower:
    def __init__(self, x):
        self.x = x
        self.y = HEIGHT - 70
        self.growth = 0.0  # De 0.0 (graine/pousse) à 1.0 (pleine floraison)
        self.max_growth = random.uniform(0.85, 1.25)
        self.color = random.choice(FLOWER_COLORS)
        self.petals = random.randint(5, 7)

    def update(self):
        if self.growth < self.max_growth:
            self.growth += 0.012

    def draw(self, surface):
        stem_height = int(45 * self.growth)
        if stem_height < 3:
            return
        
        # Tige de la fleur
        pygame.draw.line(surface, (90, 190, 110), (self.x, self.y), (self.x, self.y - stem_height), 3)
        
        # Éclosion de la fleur
        if self.growth > 0.35:
            bloom_radius = int(14 * self.growth)
            bloom_y = self.y - stem_height
            
            # Pétales colorés
            for i in range(self.petals):
                angle = i * (2 * math.pi / self.petals)
                px = self.x + math.cos(angle) * (bloom_radius * 0.7)
                py = bloom_y + math.sin(angle) * (bloom_radius * 0.7)
                pygame.draw.circle(surface, self.color, (int(px), int(py)), bloom_radius // 2)
            
            # Cœur de la fleur
            pygame.draw.circle(surface, (255, 255, 200), (int(self.x), int(bloom_y)), bloom_radius // 3)

# Initialisation
cloud = Cloud()
raindrops = []
flowers = []

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                flowers = []
                raindrops = []
            elif event.key == pygame.K_SPACE:
                # Planter directement une fleur sous le nuage
                flowers.append(Flower(cloud.x + random.randint(-40, 40)))

    # Si on clique ou maintient la souris, le nuage pleut
    if mouse_pressed[0] and mouse_pos[1] > 80:
        for _ in range(2):
            raindrops.append(Raindrop(cloud.x + random.uniform(-45, 45), cloud.y + 20))

    # Mettre à jour les gouttes de pluie
    for drop in raindrops[:]:
        drop.update()
        # Si la goutte touche le sol
        if drop.y >= HEIGHT - 70:
            raindrops.remove(drop)
            # 35% de chance de faire pousser une nouvelle fleur à l'impact
            if random.random() < 0.35:
                flowers.append(Flower(drop.x))
        else:
            # Si une goutte touche une fleur en train de pousser, elle accélère sa croissance !
            for flower in flowers:
                if abs(drop.x - flower.x) < 16 and abs(drop.y - flower.y) < 50:
                    flower.growth = min(flower.max_growth, flower.growth + 0.3)
                    if drop in raindrops:
                        raindrops.remove(drop)
                    break

    # Mettre à jour les fleurs
    for flower in flowers:
        flower.update()

    # --- RENDU GRAPHIQUE ---
    screen.fill(BG_COLOR)

    # Dessiner le sol fertile
    ground_rect = pygame.Rect(0, HEIGHT - 70, WIDTH, 70)
    pygame.draw.rect(screen, GROUND_COLOR, ground_rect)
    pygame.draw.line(screen, (50, 70, 95), (0, HEIGHT - 70), (WIDTH, HEIGHT - 70), 2)

    # Dessiner toutes les fleurs
    for flower in flowers:
        flower.draw(screen)

    # Dessiner les gouttes de pluie
    for drop in raindrops:
        pygame.draw.line(screen, RAIN_COLOR, (drop.x, drop.y), (drop.x, drop.y + 10), 2)

    # Mettre à jour et dessiner le nuage kawaii
    cloud.update(mouse_pos)
    cloud.draw(screen)

    # --- HUD ET INSTRUCTIONS ---
    title_txt = font_medium.render("KAWAII CLOUD & FLOWER GARDEN — JARDIN MAGIQUE", True, TEXT_COLOR)
    screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 12))

    stats_txt = font_small.render(f"Fleurs dans le jardin : {len(flowers)} | Gouttes : {len(raindrops)}", True, (255, 175, 50))
    screen.blit(stats_txt, (40, 42))

    inst_txt = font_small.render("SOURIS : Déplacer le nuage | CLIC GAUCHE : Faire pleuvoir | ESPACE : Planter | R : Reset", True, GRAY)
    screen.blit(inst_txt, (WIDTH - inst_txt.get_width() - 40, 42))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()