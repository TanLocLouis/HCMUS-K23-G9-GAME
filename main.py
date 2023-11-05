import pygame
import random

# Khoi tao chuong trinh
pygame.init()
screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
pygame.display.set_caption("Et Bi 99 - NHA CAI DEN TU CHAU A")
clock = pygame.time.Clock()

# Hien thi Coin hien co
coin = 0
collected_coin = 0
font = pygame.font.Font(None, 50)
text = font.render("COIN: ", True,  "#f06e4b")
text_rect = text.get_rect(center = (100, 50))

# Trang thai cua game 0: tai man hinh dang nhap 2: minigame 1, 3, 4 ... chua co :))
game_state = 0

# Class nhan vat
class Player():
    def __init__(self, x, y, image, scale):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def isCollide(self, x, y):
        return self.rect.collidepoint(x, y)

# Class hien thi chu
class Txt():
    def __init__(self, x, y, content, color):
        font = pygame.font.Font(None, 50)
        self.text = font.render(content, True, color)
        self.rect = self.text.get_rect()
        self.rect.topleft = (x, y)

    def render(self):
        screen.blit(self.text, self.rect)

# Class hien thi hinh anh
class Img():
    def __init__(self, x, y, image, scale):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Class hien thi nut
class Button():
    def __init__(self, x, y, image, scale):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def isClick(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            return True
        else:
            return False  

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

pygame.mixer.init()
pygame.mixer.music.load("./Asset/BG-Music.mp3")
pygame.mixer.music.play(-1, 0, 10000)

# Animation cho background chinh
bg_1_x = 0
# Random vi tri mouse trong minigame
mg_mouse = (random.random() * 1500, 720)
# Dem so luong tick de tinh thoi gian choi minigame sau mot thoi gian tu don thoat
mg_tick = 0
# Animation cho cloud trong minigame
bg_sun_x = 0

x_add = 0
y_add = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit
            
    w, h = pygame.display.get_surface().get_size()

    # Tai main menu
    if game_state == 0:
        bg = Img(0, 0, "./Asset/BG.png", (w, h))
        bg.draw()
        bg_text = Img(w / 2 - 500, h / 5, "./Asset/BG-Title.png", (1000, 200))
        bg_text.draw()

        bg_1_x -= 2
        if bg_1_x <= -1000:
            bg_1_x = 0 
        bg_1 = Img(bg_1_x, h - 250, "./Asset/BG3.png", (4000, 250))
        bg_1.draw()

        btn_exit = Button(w - 500, 80, "./Asset/ExitGame.png", (100, 100))
        btn_exit.draw()
        if btn_exit.isClick():
            exit()

        btn_play = Button(w / 2 - 150, h / 2 - 20, "./Asset/BTN-Play.png", (300, 100))
        btn_play.draw()

        btn_minigame = Button(w / 2 - 150, h / 2 + 100 , "./Asset/BTN-Minigame.png", (300, 100))
        btn_minigame.draw()

        data_file = open("Inventory.txt", "r")
        data = data_file.readline()
        coin = data
        data_file.close()

        text = Txt(300, 100, "COIN: " + str(coin), "#f06e4b")
        text.render()

        if (btn_minigame.isClick()):
            game_state = 2
            mg_tick = 460

            screen.fill("#96c3d7")
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            pygame.mixer.music.load("./Minigame/MG-Music.mp3")
            pygame.mixer.music.play(-1, 0, 10000)
            collected_coin = 0

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

    # Minigame
    elif game_state == 2:
        mg_tick -= 1

        if mg_tick % 30 == 0:
            x_add = random.random() * 40 - 20
            y_add = random.random() * 40 - 20
        mg_mouse_x = mg_mouse[0]
        mg_mouse_x += x_add
        # xu li khi chuot chay ra bien
        if mg_mouse_x <= 0:
            mg_mouse_x = w
        if mg_mouse_x >= w:
            mg_mouse_x = 0
        mg_mouse_y = mg_mouse[1]
        mg_mouse_y += y_add
        # xu li khi chuot chay ra bien
        if mg_mouse_y <= h - 400:
            mg_mouse_y = h
        if mg_mouse_y >= h:
            mg_mouse_y = h - 400
        mg_mouse = (mg_mouse_x, mg_mouse_y)

        # Het thoi gian choi game
        if (mg_tick == 0):
            game_state = 0
            pygame.mixer.Sound("./Minigame/MG-Win.mp3").play()

            # Doc du lieu coin tu file           
            data_file = open("Inventory.txt", "r")
            cur_coin = int(data_file.readline())
            data_file.close()

            # Cong voi diem roi luu vo file
            cur_coin += collected_coin

            data_file = open("Inventory.txt", "w")
            data = data_file.write(str(cur_coin))
            data_file.close()

        screen.fill("#96c3d7")
        text = Txt(300, 100, "COLLECTED COIN: " + str(collected_coin), "#f06e4b")
        text.render()

        text = Txt(300, 50, "TIME: " + str(int(mg_tick / 30)), "#f06e4b")
        text.render()

        bg_grass = Img(0, h - 1000, "./Minigame/MG-Grass.png", (5000, 1000))
        bg_grass.draw()

        bg_sun = Img(300, 200, "./Minigame/MG-Sun.png", (100, 100))
        bg_sun.draw()

        bg_sun_x += 1
        if bg_sun_x >= h:
            bg_sun_x = 0
        bg_sun = Img(bg_sun_x, 300, "./Minigame/MG-Cloud.png", (1600, 100))
        bg_sun.draw()
        
        bg_1 = Player(mg_mouse[0], mg_mouse[1], "./Minigame/MG-Mouse.png", (250, 250))
        bg_1.draw()

        mouse_input = pygame.mouse.get_pos()

        mg_hammer = Img(mouse_input[0] - 50, mouse_input[1] - 50, "./Minigame/MG-Hammer.png", (100, 100))
        mg_hammer.draw()

        if bg_1.isCollide(mouse_input[0], mouse_input[1]):
            if pygame.mouse.get_pressed()[0]:
                collected_coin += 1
                pygame.mixer.Sound("./Minigame/MG-Coin.mp3").play()

                mg_mouse = (random.random() * (w - 200), h - 500 + random.random() * 300)

    pygame.display.update()
    clock.tick(30)