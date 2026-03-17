# Oyunun çalışması için gerekli modülleri içe aktar / Import required modules for the game to run
# [TÜYO]: Burada 'import' kısmını farenle göster. Çocuklara modüllerin bir "alet çantası" (toolbox) gibi olduğunu ve Pygame'in bize şekiller çizmek için gerekli aletleri verdiğini anlattığını söyle.
import pygame
import sys
import random

# Pygame motorunu başlat / Initialize the Pygame engine
pygame.init()

# Oyun penceresi ve renkler için sabitler / Constants for game window and colors
DEFAULT_SCREEN_WIDTH = 1024
DEFAULT_SCREEN_HEIGHT = 520
screen_width = DEFAULT_SCREEN_WIDTH
screen_height = DEFAULT_SCREEN_HEIGHT

GREEN = (0, 128, 0)  # Sahanın rengi (çim) / Pitch color (grass)
WHITE = (255, 255, 255)  # Çizgiler, top ve kale çerçeveleri için beyaz / White for lines, ball, and goal frames
BLACK = (0, 0, 0)  # Oyuncular ve top üzerindeki detaylar için siyah / Black for player and ball details

# Kale boyutları ve file stili (kale çizimi için kullanılır) / Goal dimensions and net style (used for drawing goals)
GOAL_WIDTH = 10  # Kale direklerinin ve üst direğin kalınlığı / Thickness of goalposts and crossbar
GOAL_HEIGHT = 120  # Kale aralığının yüksekliği / Height of the goal opening
GOAL_DEPTH = 50  # Kale sahaya doğru olan derinliği / Depth of the goal towards the pitch
NET_COLOR = (200, 200, 200)  # File için açık gri / Light gray for the net 
NET_SPACING = 10  # Filedeki çizgiler arasındaki boşluk / Spacing between lines in the net

# Oyun penceresini oluştur (responsive, yeniden boyutlandırılabilir) / Create game window (responsive, resizable)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("1v1 Arcade Top-Down Football")

# FPS kontrolü için saat / Clock for FPS control
clock = pygame.time.Clock()

# Dil seçenekleri: Türkçe, İngilizce, Vietnamca / Language options: Turkish, English, Vietnamese
LANGUAGES = ["TR", "EN", "VI"]
LANGUAGE_LABELS = {"TR": "Türkçe", "EN": "English", "VI": "Tiếng Việt"}

TEXTS = {
    "TR": {
        "start_title": "1v1 Futbol Oyunu",
        "start_info": "Yukarı/Aşağı: seçenek değiştir | Enter: seç | Tıkla: seç",
        "start_options": ["Oyunu Başlat", "Ayarlar", "Dil Seçimi", "Çıkış"],
        "settings_title": "AYARLAR",
        "settings_info": "TAB: oyuncu değiştir | Sol/Sağ: renk değiştir | Enter: kaydet | Esc: geri",
        "selected_player": "Seçili oyuncu",
        "left_player_color": "Sol oyuncu rengi",
        "right_player_color": "Sağ oyuncu rengi",
        "pause_title": "Oyun duraklatıldı",
        "pause_info": "Yukarı/Aşağı: seçenek değiştir | Enter: seç | Esc: devam",
        "pause_options": ["Devam", "Ayarlar", "Ana Menü", "Çıkış"],
        "scoreboard": "Skor",
        "time_text": "Süre",
    },
    "EN": {
        "start_title": "1v1 Football Game",
        "start_info": "Up/Down: change option | Enter: select | Click: choose",
        "start_options": ["Start Game", "Settings", "Language", "Quit"],
        "settings_title": "SETTINGS",
        "settings_info": "TAB: switch player | Left/Right: change color | Enter: save | Esc: back",
        "selected_player": "Selected player",
        "left_player_color": "Left player color",
        "right_player_color": "Right player color",
        "pause_title": "Game Paused",
        "pause_info": "Up/Down: change option | Enter: select | Esc: resume",
        "pause_options": ["Resume", "Settings", "Main Menu", "Quit"],
        "scoreboard": "Score",
        "time_text": "Time",
    },
    "VI": {
        "start_title": "Trò chơi Bóng đá 1v1",
        "start_info": "Lên/Xuống: chọn | Enter: xác nhận | Nhấn: chọn",
        "start_options": ["Bắt đầu", "Cài đặt", "Ngôn ngữ", "Thoát"],
        "settings_title": "CÀI ĐẶT",
        "settings_info": "TAB: đổi người | Trái/Phải: đổi màu | Enter: lưu | Esc: trở lại",
        "selected_player": "Người chơi đang chọn",
        "left_player_color": "Màu trái",
        "right_player_color": "Màu phải",
        "pause_title": "Tạm dừng", 
        "pause_info": "Lên/Xuống: chọn | Enter: xác nhận | Esc: tiếp tục",
        "pause_options": ["Tiếp tục", "Cài đặt", "Menu chính", "Thoát"],
        "scoreboard": "Điểm",
        "time_text": "Thời gian",
    },
}

# Renk adlarını çeviren liste / List translating color names
COLOR_NAMES = {
    "TR": ["Siyah", "Beyaz", "Kırmızı", "Mavi", "Yeşil", "Sarı"],
    "EN": ["Black", "White", "Red", "Blue", "Green", "Yellow"],
    "VI": ["Đen", "Trắng", "Đỏ", "Xanh dương", "Xanh lá", "Vàng"],
}

current_language = "EN"

COLOR_OPTIONS = [
    ("Siyah", (0, 0, 0)),
    ("Beyaz", (255, 255, 255)),
    ("Kırmızı", (255, 0, 0)),
    ("Mavi", (0, 0, 255)),
    ("Yeşil", (0, 255, 0)),
    ("Sarı", (255, 255, 0)),
]

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
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 28)
else:
    font = pygame.font.SysFont(loaded_font_name, 36)
    small_font = pygame.font.SysFont(loaded_font_name, 28)

# [TÜYO]: Burada fonksiyonları (def) göster. Fonksiyonların kod tekrarını önlediğini, örneğin 'draw_text' fonksiyonunu defalarca kullanarak kodu nasıl daha temiz hale getirdiğimizi vurgula.
def get_screen_size():
    # Mevcut ekran boyutunu döndürür / Returns the current screen size
    return screen.get_size()

def handle_resize_event(event):
    # Pencere yeniden boyutlandırıldığında global viewport güncellemesi / Global viewport update on window resize
    global screen_width, screen_height, screen
    if event.type in (pygame.VIDEORESIZE, pygame.WINDOWRESIZED):
        screen_width, screen_height = event.w, event.h
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

def draw_text(text, x, y, font_obj, color=WHITE, center=False):
    # Ekrana metin çizmek için yardımcı fonksiyon / Helper function to draw text on the screen
    surf = font_obj.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)
    return rect

def run_language_menu(current_language):
    # Dil seçimi menüsü / Language selection menu
    menu_index = LANGUAGES.index(current_language)
    while True:
        for event in pygame.event.get():
            handle_resize_event(event)
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
        sw, sh = get_screen_size()
        draw_text("Select Language / Dil Seçimi / Chọn ngôn ngữ", sw * 0.5, sh * 0.15, font, WHITE, center=True)

        option_rects = []
        for idx, code in enumerate(LANGUAGES):
            color = WHITE if idx == menu_index else (200, 200, 200)
            rect = draw_text(LANGUAGE_LABELS[code], sw * 0.5, sh * (0.30 + idx * 0.08), font, color, center=True)
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
    # Ayarlar menüsü: Renk seçimi / Settings menu: Color selection
    menu_text = TEXTS[current_language]
    menu_running = True
    selected_player = 1 

    while menu_running:
        for event in pygame.event.get():
            handle_resize_event(event)
            if event.type == pygame.QUIT:
                return None, None 
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
        sw, sh = get_screen_size()
        draw_text(menu_text["settings_title"], sw * 0.5, sh * 0.15, font, WHITE, center=True)
        draw_text(menu_text["settings_info"], sw * 0.5, sh * 0.22, small_font, WHITE, center=True)

        draw_text(f"{menu_text['selected_player']}: {'Left' if selected_player == 1 else 'Right'}", sw * 0.5, sh * 0.30, font, WHITE, center=True)

        p1_color_name = COLOR_NAMES[current_language][player1_color_idx]
        p1_color = COLOR_OPTIONS[player1_color_idx][1]
        p2_color_name = COLOR_NAMES[current_language][player2_color_idx]
        p2_color = COLOR_OPTIONS[player2_color_idx][1]

        p1_rect = draw_text(f"{menu_text['left_player_color']} - {p1_color_name} (click)", sw * 0.5, sh * 0.42, small_font, p1_color, center=True)
        p2_rect = draw_text(f"{menu_text['right_player_color']} - {p2_color_name} (click)", sw * 0.5, sh * 0.52, small_font, p2_color, center=True)

        pygame.display.flip()
        clock.tick(30)

        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if p1_rect.collidepoint(mouse_pos):
                player1_color_idx = (player1_color_idx + 1) % len(COLOR_OPTIONS)
                pygame.time.wait(150)
            elif p2_rect.collidepoint(mouse_pos):
                player2_color_idx = (player2_color_idx + 1) % len(COLOR_OPTIONS)
                pygame.time.wait(150)

def run_start_menu(current_language):
    # Başlangıç menüsü / Start menu
    menu_text = TEXTS[current_language]
    menu_index = 0
    options = menu_text["start_options"]
    player1_color_idx = 0
    player2_color_idx = 1

    while True:
        for event in pygame.event.get():
            handle_resize_event(event)
            if event.type == pygame.QUIT:
                return None, None, None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if menu_index == 0:  
                        return player1_color_idx, player2_color_idx, True
                    elif menu_index == 1:  
                        res = run_settings_menu(player1_color_idx, player2_color_idx, current_language)
                        if res == (None, None):
                            return None, None, None
                        player1_color_idx, player2_color_idx = res
                    elif menu_index == 2:  
                        selected_language = run_language_menu(current_language)
                        if selected_language is not None:
                            current_language = selected_language
                            menu_text = TEXTS[current_language]
                            options = menu_text["start_options"]
                    else:  
                        return None, None, None

        screen.fill(GREEN)
        sw, sh = get_screen_size()
        draw_text(menu_text["start_title"], sw * 0.5, sh * 0.15, font, WHITE, center=True)
        draw_text(menu_text["start_info"], sw * 0.5, sh * 0.22, small_font, WHITE, center=True)

        option_rects = []
        for idx, opt in enumerate(options):
            color = WHITE if idx == menu_index else (200, 200, 200)
            rect = draw_text(opt, sw * 0.5, sh * (0.34 + idx * 0.08), font, color, center=True)
            option_rects.append(rect)

        left_summary = f"{menu_text['left_player_color']} - {COLOR_NAMES[current_language][player1_color_idx]}"
        right_summary = f"{menu_text['right_player_color']} - {COLOR_NAMES[current_language][player2_color_idx]}"
        draw_text(left_summary, sw * 0.5, sh * 0.78, small_font, COLOR_OPTIONS[player1_color_idx][1], center=True)
        draw_text(right_summary, sw * 0.5, sh * 0.85, small_font, COLOR_OPTIONS[player2_color_idx][1], center=True)

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
                    elif idx == 2:
                        selected_language = run_language_menu(current_language)
                        if selected_language is not None:
                            current_language = selected_language
                            menu_text = TEXTS[current_language]
                            options = menu_text["start_options"]
                    else:
                        return None, None, None
            pygame.time.wait(150)

def run_pause_menu(current_language, player1_color_idx, player2_color_idx):
    # Duraklatma menüsü / Pause menu
    menu_text = TEXTS[current_language]
    menu_index = 0
    options = menu_text["pause_options"]

    while True:
        for event in pygame.event.get():
            handle_resize_event(event)
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
        sw, sh = get_screen_size()
        draw_text(menu_text["pause_title"], sw * 0.5, sh * 0.15, font, WHITE, center=True)
        draw_text(menu_text["pause_info"], sw * 0.5, sh * 0.22, small_font, WHITE, center=True)

        option_rects = []
        for idx, opt in enumerate(options):
            color = WHITE if idx == menu_index else (200, 200, 200)
            rect = draw_text(opt, sw * 0.5, sh * (0.34 + idx * 0.07), font, color, center=True)
            option_rects.append(rect)

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

# Oyuncu sınıfı - sadece yukarı-aşağı hareket edebilen kaleci benzeri karakterler / Player class - goalkeeper-like characters moving only up and down
# [TÜYO]: 'class Player:' satırını seç. Sınıfları (Classes) çocuklara bir fabrika veya şablon (blueprint) gibi anlattığını söyle. Tek bir şablon yazıp hem Oyuncu 1 hem de Oyuncu 2'yi kolayca oluşturduğumuzu belirt.
class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 5  # Oyuncunun dikeyde ne kadar hızlı hareket ettiği / Vertical movement speed of the player
        self.direction = 0  # -1 yukarı, 1 aşağı, 0 durma / -1 up, 1 down, 0 stop

    def move(self):
        self.y += self.direction * self.speed
        # Ekranın üst ve alt kenarına çıkmasını engelle / Prevent moving out of top and bottom screen edges
        _, sh = get_screen_size()
        if self.y < 0:
            self.y = 0
        if self.y > sh - self.height:
            self.y = sh - self.height

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Top sınıfı - futbol topu gibi davranır: rastgele başlar, duvarlara ve oyunculara çarpar / Ball class - acts like a football: starts randomly, bounces off walls and players
# [TÜYO]: 'self.speed_y' kısmını seç. Burada çocuklara temel fizik öğrettiğini, top üst duvara çarptığında sadece Y eksenindeki hızını tersine çevirerek sekmesini sağladığımızı anlat.
class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = random.choice([-3, 3])  
        self.speed_y = random.choice([-3, 3])  

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Üst ve alt duvara çarparsa dikey yönünü değiştir (zıpla) / Reverse vertical direction (bounce) if hitting top or bottom wall
        _, sh = get_screen_size()
        if self.y - self.radius <= 0 or self.y + self.radius >= sh:
            self.speed_y = -self.speed_y

    def check_collision(self, player):
        # Oyuncuyla çarpışma kontrolü / Collision check with the player
        # Top oyuncuya değerse yatay hızını tersine çevir (topu geri gönder) / Reverse horizontal speed if ball hits player (bounce back)
        if (self.x - self.radius < player.x + player.width and
            self.x + self.radius > player.x and
            self.y - self.radius < player.y + player.height and
            self.y + self.radius > player.y):
            self.speed_x = -self.speed_x  

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        spot_offset = self.radius // 2
        pygame.draw.circle(screen, BLACK, (int(self.x - spot_offset), int(self.y - spot_offset)), self.radius // 3)
        pygame.draw.circle(screen, BLACK, (int(self.x + spot_offset), int(self.y - spot_offset)), self.radius // 3)
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y + spot_offset)), self.radius // 3)

selected_language = run_language_menu(current_language)
if selected_language is None:
    pygame.quit()
    sys.exit()
current_language = selected_language

player1_color_idx, player2_color_idx, started = run_start_menu(current_language)
if not started:
    pygame.quit()
    sys.exit()

player1_color = COLOR_OPTIONS[player1_color_idx][1]
player2_color = COLOR_OPTIONS[player2_color_idx][1]
sw, sh = get_screen_size()
player1 = Player(50, sh // 3, 20, 100, player1_color)  
player2 = Player(sw - 70, sh // 3, 20, 100, player2_color)  
ball = Ball(sw // 2, sh // 2, 10, WHITE)  

start_ticks = pygame.time.get_ticks()
paused_time = 0

score1 = 0
score2 = 0

# Ana oyun döngüsü - oyun sürekli çalışırken bu döngü devam eder / Main game loop - continues while the game is running
# [TÜYO]: 'while running:' satırını seç. Bu döngünün oyunun kalbi olduğunu (Game Loop) ve saniyede 60 kez atarak oyunu canlı tuttuğunu çocuklara nasıl açıkladığını belirt.
running = True
while running:
    # 1. Aşama: Olay Toplama - Kullanıcı girişlerini ve pencere olaylarını dinle / Phase 1: Event Handling - Listen for user inputs and window events
    # [TÜYO]: 'for event in pygame.event.get():' kısmını seç. Buranın 'Olay Dinleme' (Event Handling) kısmı olduğunu, klavyeyi dinlediğini ve öğrenci 'W' tuşuna bastığında oyunun anında nasıl tepki verdiğini anlat.
    for event in pygame.event.get():
        handle_resize_event(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1.direction = -1  
            elif event.key == pygame.K_s:
                player1.direction = 1   
            elif event.key == pygame.K_UP:
                player2.direction = -1  
            elif event.key == pygame.K_DOWN:
                player2.direction = 1   
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
                    score1 = 0
                    score2 = 0
                    sw, sh = get_screen_size()
                    ball = Ball(sw // 2, sh // 2, 10, WHITE)
                    sw, sh = get_screen_size()
                    player1 = Player(50, sh // 3, 20, 100, COLOR_OPTIONS[player1_color_idx][1])
                    player2 = Player(sw - 70, sh // 3, 20, 100, COLOR_OPTIONS[player2_color_idx][1])
                    start_ticks = pygame.time.get_ticks()
                    paused_time = 0

                player1.color = COLOR_OPTIONS[player1_color_idx][1]
                player2.color = COLOR_OPTIONS[player2_color_idx][1]
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                player1.direction = 0  
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                player2.direction = 0  

    # 2. Aşama: Oyun mantığı ve durum güncellemesi - pozisyonları güncelle, çarpışmaları kontrol et / Phase 2: Game logic and state update - update positions, check collisions
    # [TÜYO]: 'ball.check_collision(player1)' kısmını seç. Burada oyun mantığını güncellediğimizi, topun ve oyuncunun koordinatları üst üste bindiğinde topun geri sektiğini söyle.
    player1.move()
    player2.move()
    ball.move()
    ball.check_collision(player1)
    ball.check_collision(player2)

    # Gol kontrolü - top kalenin arkasına geçerse karşı takım puan alır / Goal check - opponent scores if the ball passes behind the goal
    sw, sh = get_screen_size()
    goal_top = (sh - GOAL_HEIGHT) // 2
    goal_bottom = goal_top + GOAL_HEIGHT

    in_vertical_range = (ball.y - ball.radius) >= goal_top and (ball.y + ball.radius) <= goal_bottom

    if ball.x - ball.radius <= 0:
        if in_vertical_range:
            score2 += 1
            ball = Ball(sw // 2, sh // 2, 10, WHITE)
            start_ticks = pygame.time.get_ticks()
        else:
            ball.x = ball.radius
            ball.speed_x = -ball.speed_x
    elif ball.x + ball.radius >= sw:
        if in_vertical_range:
            score1 += 1
            ball = Ball(sw // 2, sh // 2, 10, WHITE)
            start_ticks = pygame.time.get_ticks()
        else:
            ball.x = sw - ball.radius
            ball.speed_x = -ball.speed_x

    # 3. Aşama: Görselleştirme - Sahayı, kaleleri, oyuncuları, topu ve skor tabelasını çiz / Phase 3: Rendering - Draw the pitch, goals, players, ball, and scoreboard
    # [TÜYO]: 'screen.fill(GREEN)' kısmını seç. Son olarak çizim (rendering) aşamasına geçtiğimizi; sahayı, fileleri ve oyuncuları tıpkı yaprakları hızlıca çevrilen bir çizgi roman (flipbook) gibi kare kare çizdiğimizi anlat.
    screen.fill(GREEN)  

    goal_top = (sh - GOAL_HEIGHT) // 2
    goal_bottom = goal_top + GOAL_HEIGHT

    pygame.draw.rect(screen, WHITE, (0, goal_top, GOAL_WIDTH, GOAL_HEIGHT))  
    pygame.draw.rect(screen, WHITE, (0, goal_top, GOAL_DEPTH, GOAL_WIDTH))  
    pygame.draw.rect(screen, WHITE, (sw - GOAL_WIDTH, goal_top, GOAL_WIDTH, GOAL_HEIGHT))  
    pygame.draw.rect(screen, WHITE, (sw - GOAL_DEPTH, goal_top, GOAL_DEPTH, GOAL_WIDTH))  

    for x in range(GOAL_WIDTH + NET_SPACING, GOAL_DEPTH, NET_SPACING):
        pygame.draw.line(screen, NET_COLOR, (x, goal_top), (x, goal_bottom), 1)
    for y in range(goal_top + NET_SPACING, goal_bottom, NET_SPACING):
        pygame.draw.line(screen, NET_COLOR, (0, y), (GOAL_DEPTH, y), 1)

    for x in range(sw - GOAL_DEPTH, sw - GOAL_WIDTH, NET_SPACING):
        pygame.draw.line(screen, NET_COLOR, (x, goal_top), (x, goal_bottom), 1)
    for y in range(goal_top + NET_SPACING, goal_bottom, NET_SPACING):
        pygame.draw.line(screen, NET_COLOR, (sw - GOAL_DEPTH, y), (sw, y), 1)

    pygame.draw.line(screen, WHITE, (sw // 2, 0), (sw // 2, sh), 2)  
    pygame.draw.circle(screen, WHITE, (sw // 2, sh // 2), 50, 2)  

    player1.draw(screen)
    player2.draw(screen)
    ball.draw(screen)

    elapsed_seconds = (pygame.time.get_ticks() - start_ticks - paused_time) // 1000
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    timer_text = f"{minutes:02}:{seconds:02}"
    timer_text_surface = small_font.render(f"{TEXTS[current_language]['time_text']}: {timer_text}", True, WHITE)

    score_label = f"{TEXTS[current_language]['scoreboard']}"
    score_label_surf = small_font.render(score_label, True, WHITE)
    score_label_rect = score_label_surf.get_rect(center=(sw * 0.5, 12))
    screen.blit(score_label_surf, score_label_rect)

    left_score_surf = small_font.render(str(score1), True, COLOR_OPTIONS[player1_color_idx][1])
    right_score_surf = small_font.render(str(score2), True, COLOR_OPTIONS[player2_color_idx][1])

    padding = 40
    left_score_rect = left_score_surf.get_rect(center=(sw * 0.5 - padding, 35))
    right_score_rect = right_score_surf.get_rect(center=(sw * 0.5 + padding, 35))

    screen.blit(left_score_surf, left_score_rect)
    screen.blit(right_score_surf, right_score_rect)

    screen.blit(timer_text_surface, (sw - timer_text_surface.get_width() - 10, 10))

    p1_color_name = COLOR_NAMES[current_language][player1_color_idx]
    p2_color_name = COLOR_NAMES[current_language][player2_color_idx]
    draw_text(f"{TEXTS[current_language]['left_player_color']}: {p1_color_name}", 10, 40, small_font, COLOR_OPTIONS[player1_color_idx][1], center=False)

    right_label = f"{TEXTS[current_language]['right_player_color']}: {p2_color_name}"
    right_surf = small_font.render(right_label, True, COLOR_OPTIONS[player2_color_idx][1])
    right_rect = right_surf.get_rect()
    right_rect.topright = (sw - 10, 40)
    screen.blit(right_surf, right_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()