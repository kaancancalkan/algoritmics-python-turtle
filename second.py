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

# Dil seçenekleri: Türkçe, İngilizce, Vietnamca
LANGUAGES = ["TR", "EN", "VI"]
LANGUAGE_LABELS = {"TR": "Türkçe", "EN": "English", "VI": "Tiếng Việt"}

TEXTS = {
    "TR": {
        "start_title": "1v1 Futbol Oyunu",
        "start_info": "Yukarı/Aşağı: seçenek değiştir | Enter: seç | Tıkla: seç",
        "start_options": ["Oyunu Başlat", "Ayarlar", "Çıkış"],
        "settings_title": "AYARLAR",
        "settings_info": "TAB: oyuncu değiştir | Sol/Sağ: renk değiştir | Enter: kaydet | Esc: geri",
        "selected_player": "Seçili oyuncu",
        "left_player_color": "Sol oyuncu rengi",
        "right_player_color": "Sağ oyuncu rengi",
        "pause_title": "Oyun duraklatıldı",
        "pause_options": ["Devam", "Ayarlar", "Ana Menü", "Çıkış"],
        "scoreboard": "Skor",
        "time_text": "Süre",
    },
    "EN": {
        "start_title": "1v1 Football Game",
        "start_info": "Up/Down: change option | Enter: select | Click: choose",
        "start_options": ["Start Game", "Settings", "Quit"],
        "settings_title": "SETTINGS",
        "settings_info": "TAB: switch player | Left/Right: change color | Enter: save | Esc: back",
        "selected_player": "Selected player",
        "left_player_color": "Left player color",
        "right_player_color": "Right player color",
        "pause_title": "Game Paused",
        "pause_options": ["Resume", "Settings", "Main Menu", "Quit"],
        "scoreboard": "Score",
        "time_text": "Time",
    },
    "VI": {
        "start_title": "Trò chơi Bóng đá 1v1",
        "start_info": "Lên/Xuống: chọn | Enter: xác nhận | Nhấn: chọn",
        "start_options": ["Bắt đầu", "Cài đặt", "Thoát"],
        "settings_title": "CÀI ĐẶT",
        "settings_info": "TAB: đổi người | Trái/Phải: đổi màu | Enter: lưu | Esc: trở lại",
        "selected_player": "Người chơi đang chọn",
        "left_player_color": "Màu trái",
        "right_player_color": "Màu phải",
        "pause_title": "Tạm dừng", 
        "pause_options": ["Tiếp tục", "Cài đặt", "Menu chính", "Thoát"],
        "scoreboard": "Điểm",
        "time_text": "Thời gian",
    },
}

# Renk adlarını çeviren liste
COLOR_NAMES = {
    "TR": ["Siyah", "Beyaz", "Kırmızı", "Mavi", "Yeşil", "Sarı"],
    "EN": ["Black", "White", "Red", "Blue", "Green", "Yellow"],
    "VI": ["Đen", "Trắng", "Đỏ", "Xanh dương", "Xanh lá", "Vàng"],
}

# Varsayılan dil
current_language = "EN"

# Renk seçenekleri - menüde forma rengi seçmek için kullanılır
COLOR_OPTIONS = [
    ("Siyah", (0, 0, 0)),
    ("Beyaz", (255, 255, 255)),
    ("Kırmızı", (255, 0, 0)),
    ("Mavi", (0, 0, 255)),
    ("Yeşil", (0, 255, 0)),
    ("Sarı", (255, 255, 0)),
]

# Yardımcı fonksiyonlar - ekrana yazı çizmek ve menüleri yönetmek için
# Türkçe ve Vietnamca karakterleri destekleyen bir font seçmek için SysFont kullan.
preferred_fonts = ["Arial", "Tahoma", "Segoe UI", "Noto Sans", "Noto Sans CJK", "Noto Sans Symbols"]
loaded_font_name = None
for f in preferred_fonts:
    try:
        test_font = pygame.font.SysFont(f, 36)
        if test_font:
            loaded_font_name = f
            break
    except Exception:
        continue

if loaded_font_name is None:
    # Sistem fontu bulunamazsa, varsayılan font
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 28)
else:
    font = pygame.font.SysFont(loaded_font_name, 36)
    small_font = pygame.font.SysFont(loaded_font_name, 28)

def draw_text(text, x, y, font_obj, color=WHITE, center=False):
    """Ekrana metin çizmek için yardımcı fonksiyon."""
    surf = font_obj.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)
    return rect


def run_language_menu(current_language):
    """Language selection screen: TR/EN/VI with keyboard and mouse support."""
    menu_index = LANGUAGES.index(current_language)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    menu_index = (menu_index - 1) % len(LANGUAGES)
                elif event.key == pygame.K_RIGHT:
                    menu_index = (menu_index + 1) % len(LANGUAGES)
                elif event.key == pygame.K_RETURN:
                    return LANGUAGES[menu_index]

        screen.fill(GREEN)
        draw_text("Select Language / Dil Seçimi / Chọn ngôn ngữ", SCREEN_WIDTH // 2, 60, font, WHITE, center=True)

        option_rects = []
        for idx, code in enumerate(LANGUAGES):
            color = WHITE if idx == menu_index else (200, 200, 200)
            rect = draw_text(LANGUAGE_LABELS[code], SCREEN_WIDTH // 2, 150 + idx * 40, font, color, center=True)
            option_rects.append(rect)

        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            for idx, rect in enumerate(option_rects):
                if rect.collidepoint(mouse_pos):
                    return LANGUAGES[idx]
            pygame.time.wait(150)

        pygame.display.flip()
        clock.tick(30)


def run_settings_menu(player1_color_idx, player2_color_idx, current_language):
    """Ayarlar menüsü: Her iki oyuncunun forma rengini seçmek için."""
    menu_text = TEXTS[current_language]
    menu_running = True
    selected_player = 1  # 1 = sol oyuncu, 2 = sağ oyuncu

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None  # Çıkış
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return player1_color_idx, player2_color_idx
                elif event.key == pygame.K_TAB:
                    selected_player = 2 if selected_player == 1 else 1
                elif event.key == pygame.K_LEFT:
                    if selected_player == 1:
                        player1_color_idx = (player1_color_idx - 1) % len(COLOR_OPTIONS)
                    else:
                        player2_color_idx = (player2_color_idx - 1) % len(COLOR_OPTIONS)
                elif event.key == pygame.K_RIGHT:
                    if selected_player == 1:
                        player1_color_idx = (player1_color_idx + 1) % len(COLOR_OPTIONS)
                    else:
                        player2_color_idx = (player2_color_idx + 1) % len(COLOR_OPTIONS)
                elif event.key == pygame.K_RETURN:
                    return player1_color_idx, player2_color_idx

        screen.fill(GREEN)
        draw_text(menu_text["settings_title"], SCREEN_WIDTH // 2, 60, font, WHITE, center=True)
        draw_text(menu_text["settings_info"], SCREEN_WIDTH // 2, 100, small_font, WHITE, center=True)

        # Seçilen oyuncuyu belirt
        draw_text(f"{menu_text['selected_player']}: {'Left' if selected_player == 1 else 'Right'}", SCREEN_WIDTH // 2, 140, font, WHITE, center=True)

        # Renk seçeneklerini göster; metin kendi seçili rengi ile yazılıyor
        p1_color_name = COLOR_OPTIONS[player1_color_idx][0]
        p1_color = COLOR_OPTIONS[player1_color_idx][1]
        p2_color_name = COLOR_OPTIONS[player2_color_idx][0]
        p2_color = COLOR_OPTIONS[player2_color_idx][1]

        p1_rect = draw_text(f"{menu_text['left_player_color']}: {p1_color_name} (click to next)", SCREEN_WIDTH // 2, 190, font, p1_color, center=True)
        p2_rect = draw_text(f"{menu_text['right_player_color']}: {p2_color_name} (click to next)", SCREEN_WIDTH // 2, 230, font, p2_color, center=True)

        pygame.display.flip()
        clock.tick(30)

        # fare tıklamaları
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if p1_rect.collidepoint(mouse_pos):
                player1_color_idx = (player1_color_idx + 1) % len(COLOR_OPTIONS)
                pygame.time.wait(150)
            elif p2_rect.collidepoint(mouse_pos):
                player2_color_idx = (player2_color_idx + 1) % len(COLOR_OPTIONS)
                pygame.time.wait(150)


def run_start_menu(current_language):
    """Başlangıç menüsü: Oyunu başlatma ve ayarlara geçiş."""
    menu_text = TEXTS[current_language]
    menu_index = 0
    options = menu_text["start_options"]
    player1_color_idx = 0
    player2_color_idx = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None, None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if menu_index == 0:  # Start game
                        return player1_color_idx, player2_color_idx, True
                    elif menu_index == 1:  # Settings
                        res = run_settings_menu(player1_color_idx, player2_color_idx, current_language)
                        if res == (None, None):
                            return None, None, None
                        player1_color_idx, player2_color_idx = res
                    else:  # Quit
                        return None, None, None

        screen.fill(GREEN)
        draw_text(menu_text["start_title"], SCREEN_WIDTH // 2, 60, font, WHITE, center=True)
        draw_text(menu_text["start_info"], SCREEN_WIDTH // 2, 100, small_font, WHITE, center=True)

        option_rects = []
        for idx, opt in enumerate(options):
            color = WHITE if idx == menu_index else (200, 200, 200)
            rect = draw_text(opt, SCREEN_WIDTH // 2, 170 + idx * 40, font, color, center=True)
            option_rects.append(rect)

        # Şu anki forma renklerini göster (seçilen renklerle)
        draw_text(f"{menu_text['left_player_color']}: {COLOR_OPTIONS[player1_color_idx][0]}", SCREEN_WIDTH // 2, 300, small_font, COLOR_OPTIONS[player1_color_idx][1], center=True)
        draw_text(f"{menu_text['right_player_color']}: {COLOR_OPTIONS[player2_color_idx][0]}", SCREEN_WIDTH // 2, 330, small_font, COLOR_OPTIONS[player2_color_idx][1], center=True)

        pygame.display.flip()
        clock.tick(30)

        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            for idx, rect in enumerate(option_rects):
                if rect.collidepoint(mouse_pos):
                    menu_index = idx
                    if idx == 0:
                        return player1_color_idx, player2_color_idx, True
                    elif idx == 1:
                        res = run_settings_menu(player1_color_idx, player2_color_idx, current_language)
                        if res == (None, None):
                            return None, None, None
                        player1_color_idx, player2_color_idx = res
                    else:
                        return None, None, None
            pygame.time.wait(150)


def run_pause_menu(current_language, player1_color_idx, player2_color_idx):
    """Oyun duraklatma menüsü; ESC dönerken kullanılır."""
    menu_text = TEXTS[current_language]
    menu_index = 0
    options = menu_text["pause_options"]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", player1_color_idx, player2_color_idx
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if menu_index == 0:
                        return "resume", player1_color_idx, player2_color_idx
                    elif menu_index == 1:
                        res = run_settings_menu(player1_color_idx, player2_color_idx, current_language)
                        if res == (None, None):
                            return "quit", player1_color_idx, player2_color_idx
                        player1_color_idx, player2_color_idx = res
                    elif menu_index == 2:
                        return "main_menu", player1_color_idx, player2_color_idx
                    else:
                        return "quit", player1_color_idx, player2_color_idx

        screen.fill(GREEN)
        draw_text(menu_text["pause_title"], SCREEN_WIDTH // 2, 60, font, WHITE, center=True)
        draw_text(menu_text["start_info"], SCREEN_WIDTH // 2, 100, small_font, WHITE, center=True)

        option_rects = []
        for idx, opt in enumerate(options):
            color = WHITE if idx == menu_index else (200, 200, 200)
            rect = draw_text(opt, SCREEN_WIDTH // 2, 170 + idx * 40, font, color, center=True)
            option_rects.append(rect)

        # Skorboard için renkli oyuncu yazıları burada gösterilmez, oyun devamında ana ekrana yansıtılacak.
        pygame.display.flip()
        clock.tick(30)

        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            for idx, rect in enumerate(option_rects):
                if rect.collidepoint(mouse_pos):
                    menu_index = idx
                    if idx == 0:
                        return "resume", player1_color_idx, player2_color_idx
                    elif idx == 1:
                        res = run_settings_menu(player1_color_idx, player2_color_idx, current_language)
                        if res == (None, None):
                            return "quit", player1_color_idx, player2_color_idx
                        player1_color_idx, player2_color_idx = res
                    elif idx == 2:
                        return "main_menu", player1_color_idx, player2_color_idx
                    else:
                        return "quit", player1_color_idx, player2_color_idx
            pygame.time.wait(150)


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

# Dil seçimi menüsünü çalıştır
selected_language = run_language_menu(current_language)
if selected_language is None:
    pygame.quit()
    sys.exit()
current_language = selected_language

# Başlangıç menüsünü çalıştır: forma renkleri ve ayarları seç
player1_color_idx, player2_color_idx, started = run_start_menu(current_language)
if not started:
    pygame.quit()
    sys.exit()

# Seçilen renkleri kullanarak oyuncuları oluştur
player1_color = COLOR_OPTIONS[player1_color_idx][1]
player2_color = COLOR_OPTIONS[player2_color_idx][1]
player1 = Player(50, 150, 20, 100, player1_color)  # Sol oyuncu
player2 = Player(730, 150, 20, 100, player2_color)  # Sağ oyuncu
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, WHITE)  # Top oyunun ortasında başlar

# Oyunun başlamasıyla birlikte süreyi sıfırla
start_ticks = pygame.time.get_ticks()
paused_time = 0

# Skor değişkenleri
score1 = 0
score2 = 0

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
            elif event.key == pygame.K_ESCAPE:
                pause_start = pygame.time.get_ticks()
                action, player1_color_idx, player2_color_idx = run_pause_menu(current_language, player1_color_idx, player2_color_idx)
                pause_end = pygame.time.get_ticks()
                paused_time += (pause_end - pause_start)

                if action == "quit":
                    running = False
                    break

                if action == "main_menu":
                    start_menu_result = run_start_menu(current_language)
                    if start_menu_result == (None, None, None):
                        running = False
                        break
                    player1_color_idx, player2_color_idx, started = start_menu_result
                    if not started:
                        running = False
                        break
                    # skoru sıfırla
                    score1 = 0
                    score2 = 0
                    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10, WHITE)
                    player1 = Player(50, 150, 20, 100, COLOR_OPTIONS[player1_color_idx][1])
                    player2 = Player(730, 150, 20, 100, COLOR_OPTIONS[player2_color_idx][1])
                    start_ticks = pygame.time.get_ticks()
                    paused_time = 0

                # resume veya settings sonrası renkleri tekrar ata
                player1.color = COLOR_OPTIONS[player1_color_idx][1]
                player2.color = COLOR_OPTIONS[player2_color_idx][1]
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
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks - paused_time) // 1000
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    timer_text = f"{minutes:02}:{seconds:02}"
    score_text = font.render(f"{TEXTS[current_language]['scoreboard']}: {score1} - {score2}", True, WHITE)
    timer_text_surface = font.render(f"{TEXTS[current_language]['time_text']}: {timer_text}", True, WHITE)

    # Skor ve süre metinlerini üst ortada hizala
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2 - 40, 20))
    timer_rect = timer_text_surface.get_rect(center=(SCREEN_WIDTH // 2 + 100, 20))

    # Her iki takımın kullandığı renk isimlerini göster
    draw_text(COLOR_OPTIONS[player1_color_idx][0], SCREEN_WIDTH // 2 - 150, 20, small_font, COLOR_OPTIONS[player1_color_idx][1], center=True)
    draw_text(COLOR_OPTIONS[player2_color_idx][0], SCREEN_WIDTH // 2 + 150, 20, small_font, COLOR_OPTIONS[player2_color_idx][1], center=True)

    screen.blit(score_text, score_rect)
    screen.blit(timer_text_surface, timer_rect)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame when the loop ends
pygame.quit()
sys.exit()