# Oyunun çalışması için gerekli modülleri içe aktar
import pygame
import sys
import random

# Pygame motorunu başlat
pygame.init()

# Oyun penceresi ve renkler için sabitler
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GREEN = (0, 128, 0)  # Sahanın rengi (çim)
WHITE = (255, 255, 255)  # Çizgiler, top ve kale çerçeveleri için beyaz
BLACK = (0, 0, 0)  # Oyuncular ve top üzerindeki detaylar için siyah

# Kale boyutları ve file stili (kale çizimi için kullanılır)
GOAL_WIDTH = 10  # Kale direklerinin ve üst direğin kalınlığı
GOAL_HEIGHT = 120  # Kale aralığının yüksekliği
GOAL_DEPTH = 50  # Kale sahaya doğru olan derinliği
NET_COLOR = (200, 200, 200)  # File için açık gri (zeminle kontrast oluşturur)
NET_SPACING = 10  # Filedeki çizgiler arasındaki boşluk

# Oyun penceresini oluştur
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("1v1 Arcade Top-Down Football")

# FPS kontrolü için saat
clock = pygame.time.Clock()

# Oyun süresini hesaplamak için başlangıç zamanı
start_ticks = pygame.time.get_ticks()  # pygame.init()'den bu yana geçen milisaniye

# Oyuncu sınıfı - sadece yukarı-aşağı hareket edebilen kaleci benzeri karakterler
class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 5  # Oyuncunun dikeyde ne kadar hızlı hareket ettiği
        self.direction = 0  # -1 yukarı, 1 aşağı, 0 durma

    def move(self):
        self.y += self.direction * self.speed
        # Ekranın üst ve alt kenarına çıkmasını engelle
        if self.y < 0:
            self.y = 0
        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Top sınıfı - futbol topu gibi davranır: rastgele başlar, duvarlara ve oyunculara çarpar
class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = random.choice([-3, 3])  # Başlangıçta rastgele sola veya sağa
        self.speed_y = random.choice([-3, 3])  # Başlangıçta rastgele yukarı veya aşağı

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Üst ve alt duvara çarparsa dikey yönünü değiştir (zıpla)
        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
            self.speed_y = -self.speed_y

    def check_collision(self, player):
        # Oyuncuyla çarpışma kontrolü (basit AABB çarpışması)
        # Top oyuncuya değerse yatay hızını tersine çevir (topu geri gönder)
        if (self.x - self.radius < player.x + player.width and
            self.x + self.radius > player.x and
            self.y - self.radius < player.y + player.height and
            self.y + self.radius > player.y):
            self.speed_x = -self.speed_x  # Geriye doğru sekiyor

    def draw(self, screen):
        # Futbol topu stili çizim: beyaz daire ve birkaç siyah leke
        # Lekeler basit daireler olarak çizilerek topa futbol topu hissi verilir
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Temsili birkaç 'pentoagon/altıgen' benzeri leke eklendi
        spot_offset = self.radius // 2
        pygame.draw.circle(screen, BLACK, (int(self.x - spot_offset), int(self.y - spot_offset)), self.radius // 3)
        pygame.draw.circle(screen, BLACK, (int(self.x + spot_offset), int(self.y - spot_offset)), self.radius // 3)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y + spot_offset)), self.radius // 3)

# Oyuncu ve top nesnelerini oluştur - sol taraftaki oyuncu W/S tuşlarıyla, sağdaki oyuncu ok tuşlarıyla kontrol edilir
player1 = Player(50, 150, 20, 100, BLACK)  # Sol oyuncu
player2 = Player(730, 150, 20, 100, BLACK)  # Sağ oyuncu
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, WHITE)  # Top oyunun ortasında başlar

# Skor değişkenleri
score1 = 0
score2 = 0
font = pygame.font.Font(None, 36)

# Ana oyun döngüsü - oyun sürekli çalışırken bu döngü devam eder
running = True
while running:
    # 1. Aşama: Olay Toplama - Kullanıcı girişlerini ve pencere olaylarını dinle
    # (W/S tuşları sag/sol kaleciyi, yukarı/aşağı ise diğer kaleciyi hareket ettirir)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1.direction = -1  # Yukarı hareket
            elif event.key == pygame.K_s:
                player1.direction = 1   # Aşağı hareket
            elif event.key == pygame.K_UP:
                player2.direction = -1  # Yukarı hareket
            elif event.key == pygame.K_DOWN:
                player2.direction = 1   # Aşağı hareket
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                player1.direction = 0  # Hareketi durdur
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                player2.direction = 0  # Hareketi durdur

    # 2. Aşama: Oyun mantığı ve durum güncellemesi - pozisyonları güncelle, çarpışmaları kontrol et, skor ve top sıfırlama
    player1.move()
    player2.move()
    ball.move()
    ball.check_collision(player1)
    ball.check_collision(player2)

    # Gol kontrolü - top kalenin arkasına geçerse karşı takım puan alır
    # (Burada basitçe ekran dışına çıkış gol sayılır)
    if ball.x < 0:
        score2 += 1
        ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, WHITE)  # Topu tekrar merkeze koy
        start_ticks = pygame.time.get_ticks()  # Gol oldu, süre sıfırlanmaz ama istersen burada resetleyebilirsin
    elif ball.x > SCREEN_WIDTH:
        score1 += 1
        ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, WHITE)  # Topu tekrar merkeze koy
        start_ticks = pygame.time.get_ticks()  # Gol oldu, süre sıfırlanmaz ama istersen burada resetleyebilirsin

    # 3. Aşama: Görselleştirme - Sahayı, kaleleri, oyuncuları, topu ve skor/tabloyu çiz
    screen.fill(GREEN)  # Sahanın zeminini (çimi) çiz

    # Her iki tarafa da fileli kale çerçevesi çiz (kale direkleri ve üst direk)
    goal_top = (SCREEN_HEIGHT - GOAL_HEIGHT) // 2
    goal_bottom = goal_top + GOAL_HEIGHT

    # Sol kale çerçevesi (direkler ve üst direk)
    pygame.draw.rect(screen, WHITE, (0, goal_top, GOAL_WIDTH, GOAL_HEIGHT))  # Sol direk
    pygame.draw.rect(screen, WHITE, (0, goal_top, GOAL_DEPTH, GOAL_WIDTH))  # Üst direk

    # Sağ kale çerçevesi (direkler ve üst direk)
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - GOAL_WIDTH, goal_top, GOAL_WIDTH, GOAL_HEIGHT))  # Sağ direk
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - GOAL_DEPTH, goal_top, GOAL_DEPTH, GOAL_WIDTH))  # Üst direk

    # File desenini basit bir ızgara şeklinde çiz (dikey ve yatay çizgiler)
    # Sol file: kalenin içindeki alana dikey ve yatay çizgiler çiz
    for x in range(GOAL_WIDTH + NET_SPACING, GOAL_DEPTH, NET_SPACING):
        pygame.draw.line(screen, NET_COLOR, (x, goal_top), (x, goal_bottom), 1)
    for y in range(goal_top + NET_SPACING, goal_bottom, NET_SPACING):
        pygame.draw.line(screen, NET_COLOR, (0, y), (GOAL_DEPTH, y), 1)

    # Sağ file: aynı ızgara desenini sağ tarafa yansıt
    for x in range(SCREEN_WIDTH - GOAL_DEPTH, SCREEN_WIDTH - GOAL_WIDTH, NET_SPACING):
        pygame.draw.line(screen, NET_COLOR, (x, goal_top), (x, goal_bottom), 1)
    for y in range(goal_top + NET_SPACING, goal_bottom, NET_SPACING):
        pygame.draw.line(screen, NET_COLOR, (SCREEN_WIDTH - GOAL_DEPTH, y), (SCREEN_WIDTH, y), 1)

    # Sahadaki çizgiler: orta çizgi ve orta çember
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 2)  # Orta çizgi
    pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 50, 2)  # Orta çember

    # Oyuncuları ve topu çiz
    player1.draw(screen)
    player2.draw(screen)
    ball.draw(screen)

    # Skor tabelası ve oyun süresini üst ortada çiz
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    timer_text = f"{minutes:02}:{seconds:02}"
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    timer_text_surface = font.render(timer_text, True, WHITE)

    # Skor ve süre metinlerini üst ortada hizala
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2 - 40, 20))
    timer_rect = timer_text_surface.get_rect(center=(SCREEN_WIDTH // 2 + 60, 20))
    screen.blit(score_text, score_rect)
    screen.blit(timer_text_surface, timer_rect)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame when the loop ends
pygame.quit()
sys.exit()