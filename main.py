from game_class import *

# Initialize the game

# Show coin at the beginning of the game
collected_coin = 0
font = pygame.font.Font(None, 50)
text = font.render("COIN: ", True,  "#f06e4b")
text_rect = text.get_rect(center = (100, 50))

# -----To switch between scence
# 0: Main menu
# 1: Create account
# 2: Login
# 3: Mini game
# 4: Store
# 5: Main game
# -----Each stage has sub stage
# Ex: 11 12 13 14
game_state = 0

pygame.mixer.init()
pygame.mixer.music.load("./Asset/BG-Music-2.mp3")
pygame.mixer.music.play(-1, 0, 2000)

# Main background Grass moving animation
bg_1_x = 0
# Random mouse position in minigame
mg_mouse = (random.random() * 1500, 720)
# Game tick to calculate time in minigame
mg_tick = 0
# Cloud pos x to animate in minigame
bg_cloud_x = 0

x_add = 0
y_add = 0

name = ""
email = ""
password = ""

info = []

# variables for store players info
log_name = ""
log_password = ""
isLogin = False

player = ""
coin = 0

pos = 1

# Default language
# 1: Eng
# 2: Vie
LANG = 1

#-------------------------------
# set of items that bought in Store
prePlayItems = set()
# Language for game
workbook = openpyxl.load_workbook("languages.xlsx")
sheet = workbook.active
rows = []
for row in sheet.iter_rows(values_only=True):
    rows.append(list(row))

lang = dict()
for row in rows:
    lang[row[0]] = row[LANG]
#--------------------------------

# Coin that you want to play
bet_coin = "" 

# Show time result after played
final = {}

# character set
char_set = 1
# level
level = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit

        if event.type == pygame.KEYDOWN and game_state == 1:
            if event.key == pygame.K_RETURN:
                game_state = 11
                break
            if event.key == pygame.K_BACKSPACE: 
                name = name[:-1] 
            else: 
                name += event.unicode

        if event.type == pygame.KEYDOWN and game_state == 11:
            if event.key == pygame.K_RETURN:
                game_state = 12
                break
            if event.key == pygame.K_BACKSPACE: 
                email = email[:-1] 
            else: 
                email += event.unicode
    
        if event.type == pygame.KEYDOWN and game_state == 12:
            if event.key == pygame.K_RETURN:
                game_state = 13
                break
            if event.key == pygame.K_BACKSPACE: 
                password = password[:-1] 
            else: 
                password += event.unicode

        if event.type == pygame.KEYDOWN and game_state == 2:
            if event.key == pygame.K_RETURN:
                game_state = 21
                break
            if event.key == pygame.K_BACKSPACE: 
                log_name = log_name[:-1] 
            else: 
                log_name += event.unicode
        
        if event.type == pygame.KEYDOWN and game_state == 22:
            if event.key == pygame.K_RETURN:
                break
            if event.key == pygame.K_BACKSPACE: 
                log_password = log_password[:-1] 
            else: 
                log_password += event.unicode

        if event.type == pygame.KEYDOWN and game_state == 5:
            if event.key == pygame.K_RETURN:
                game_state = 51
                break
            if event.key == pygame.K_BACKSPACE: 
                bet_coin = bet_coin[:-1] 
            else: 
                bet_coin += event.unicode
    # get game's windows width and height
    w, h = pygame.display.get_surface().get_size()

    # Load main menu
    if game_state == 0:

        bg = Img(0, 0, "./Asset/BG.png", (w, h))
        bg.draw()
        bg_text = Img(w / 2 - 300, h / 5 + 50, "./Asset/" + lang['BG-TITLE'], (700, 125))
        bg_text.draw()

        bg_1_x -= 2
        if bg_1_x <= -1000:
            bg_1_x = 0 
        bg_1 = Img(bg_1_x, h - 250, "./Asset/BG3.png", (4000, 250))
        bg_1.draw()

        btn_exit = Button(w / 2 + 325, 97, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()

        btn_help = Button(w / 2 + 375, 90, "./Asset/Help.png", (60, 60))
        btn_help.draw()
        
        if btn_help.isClick():
            game_state = 6

        if btn_exit.isClick():
            if isLogin:
                wb = load_workbook("players.xlsx")
                sheet = wb.active
                sheet['E' + chr(pos + 48)] = coin
                wb.save("players.xlsx")
            exit()

        btn_create_account = Button(w / 2 + 150, 98, "./Asset/" + lang['CREATE'], (160, 50))
        btn_create_account.draw()
        if btn_create_account.isClick():
            game_state = 1

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            pygame.mixer.music.load("./Asset/BG-Music-1.mp3")
            pygame.mixer.music.play(-1, 0, 2000)

        btn_login = Button(w / 2 - 20, 98, "./Asset/" + lang['LOGIN'], (160, 50))
        btn_login.draw()
        if btn_login.isClick():
            game_state = 2

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            pygame.mixer.music.load("./Asset/BG-Music-1.mp3")
            pygame.mixer.music.play(-1, 0, 2000)

        text = Txt(w / 2 - 300, 100, lang['PLAYER'] + player, "#f06e4b", True)
        text.render()

        text = Txt(w / 2 - 300, 150, lang['COIN'] + str(coin), "#f06e4b", True)
        text.render()

        if isLogin:
            btn_play = Button(w / 2 - 350, h / 2, "./Asset/" + lang['BTN-PLAY'], (160, 50))
            btn_play.draw()

            if btn_play.isClick():
                game_state = 5

                pygame.mixer.music.stop()
                pygame.mixer.music.unload()

                pygame.mixer.music.load("./Minigame/MG-Music-1.mp3")
                pygame.mixer.music.play(-1, 0, 2000)

            btn_minigame = Button(w / 2 - 350, h / 2 + 75 , "./Asset/" + lang['BTN-MINIGAME'], (160, 50))
            btn_minigame.draw()

            if btn_minigame.isClick():
                if coin <= 10:
                    game_state = 3
                    mg_tick = 500

                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()

                    pygame.mixer.music.load("./Minigame/MG-Music-1.mp3")
                    pygame.mixer.music.play(-1, 0, 2000)
                    collected_coin = 0

                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
                else:
                    text = Txt(w / 2 - 400, h - 55, lang['MINIGAME-LIMIT'], "RED", True, True)
                    text.render()

            btn_shop = Button(w / 2 - 350, h / 2 + 150 , "./Asset/" + lang['STORE'], (160, 50))
            btn_shop.draw()

            if btn_shop.isClick():
                game_state = 4

                pygame.mixer.music.stop()
                pygame.mixer.music.unload()

                pygame.mixer.music.load("./Asset/BG-Music-1.mp3")
                pygame.mixer.music.play(-1, 0, 2000)

        text = Txt(w / 2 + 200, 550, lang['LANG'], "WHITE", True, True)
        text.render()

        if text.isClick():
            game_state = -1

    # Change language state
    elif game_state == -1:
        if LANG == 1:
            LANG = 2
        else:
            LANG = 1

        # Language for game
        workbook = openpyxl.load_workbook("languages.xlsx")
        sheet = workbook.active
        rows = []
        for row in sheet.iter_rows(values_only=True):
            rows.append(list(row))

        lang = dict()
        for row in rows:
            lang[row[0]] = row[LANG]
        # End Language for game

        game_state = -2

    elif game_state == -2:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        pygame.mixer.music.load("./Asset/BG-Music-2.mp3")
        pygame.mixer.music.play(-1, 0, 2000)

        game_state = 0

    # Create account state
    elif game_state == 1:
        screen.fill("#96c3d7")

        text = Txt(w / 2 - 450, 200, lang['ENTERYOURNAME'] + name, "WHITE")
        text.render()

        text = Txt(w / 2 + 250, 200, lang['NEXT'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = 11
        
        btn_exit = Button(w / 2 + 275, 250, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = -2
       
    elif game_state == 11:
        screen.fill("#96c3d7")

        text = Txt(w / 2 - 450, 200, lang['ENTERYOUREMAIL'] + email, "WHITE")
        text.render()

        text = Txt(w / 2 + 350, 200, lang['NEXT'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = 12
    
        btn_exit = Button(w / 2 + 275, 250, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = -2

    elif game_state == 12:
        screen.fill("#96c3d7")

        text = Txt(w / 2 - 450, 200, lang['ENTERYOURPASSWORD'] + password, "WHITE")
        text.render()

        text = Txt(w / 2 + 250, 200, lang['NEXT'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = 13

        btn_exit = Button(w / 2 + 275, 250, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = -2

    elif game_state == 13:
        screen.fill("#96c3d7")

        text = Txt(w / 2 - 450, 200, lang['TAKEYOURPICTURE'], "WHITE")
        text.render()

        text = Txt(w / 2 + 350, 260, lang["TAKE"], "WHITE", True, True)
        text.render()

        if text.isClick():
            game_state = -2

            cam_port = 0
            cam = VideoCapture(cam_port)

            result, image = cam.read()
            if result:
                game_state = 14

                imshow("Taken Picture", image)
                imwrite("./player_img/" + name + ".png", image)

                info.append(name)
                info.append(email)
                info.append(name + ".png")
                info.append(password)
                info.append(20) # Give 20 coin to new player

                wb = load_workbook("players.xlsx")
                sheet = wb.active
                sheet.append(info)
                wb.save("players.xlsx")

                sendMail("ltloc05samsunggalaxyj3pro@gmail.com", "rodq twhi tmme gypg", info[1]
                , "Welcome to my game"
                , "Chuc mung ban " + info[0] + " tao tai khoan game ca cuoc thanh cong :)) From Nhom 9 - 23CTT1 - NMCNTT - HCMUS with love")

        btn_exit = Button(w / 2 + 275, 250, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = -2

    elif game_state == 14:
        screen.fill("#96c3d7")

        text = Txt(w / 2 - 450, 200, lang['CREATESUCCESSFULLY'], "WHITE")
        text.render()

        text = Txt(w / 2 + 250, 200, lang['NEXT'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = -2

    elif game_state == 2:
        screen.fill("#96c3d7")

        text = Txt(w / 2 - 450, 200, lang['ENTERYOURNAME'] + log_name, "WHITE")
        text.render()

        text = Txt(w / 2 + 250, 200, lang['NEXT'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = 21 

        btn_exit = Button(w / 2 + 350, 190, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = -2

    elif game_state == 21:
        screen.fill("#96c3d7")

        text = Txt(w / 2 - 450, 200, lang['USERANDPASSWORD'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = 22

        text = Txt(w / 2 - 450, 250, lang['FACERECOGNITION'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = 25

        btn_exit = Button(w / 2 + 350, 190, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = -2

    elif game_state == 22:
        screen.fill("#96c3d7")

        text = Txt(w / 2 - 450, 200, lang["ENTERYOURPASSWORD"] + log_password, "WHITE")
        text.render()

        text = Txt(w / 2 + 250, 200, lang['NEXT'], "WHITE", True, True)
        text.render()

        if text.isClick():
            workbook = openpyxl.load_workbook("players.xlsx")
            sheet = workbook.active
            rows = []
            for row in sheet.iter_rows(values_only=True):
                rows.append(list(row))
            
            game_state = 24

            i = 0
            for row in rows:
                i += 1
                if (row[0] == log_name and row[3] == log_password):
                    game_state = 23

                    isLogin = True
                    player = log_name
                    coin = row[4]
                    pos = i
                    break
            workbook.close()
    
        btn_exit = Button(w / 2 + 350, 190, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = -2

    elif game_state == 23:
        screen.fill("#96c3d7")

        text = Txt(w / 2 - 450, 200, lang['LOGINSUCCESSFULLY'], "WHITE")
        text.render()

        text = Txt(w / 2 + 100, 200, lang['NEXT'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = -2 

    elif game_state == 24:
        screen.fill("#96c3d7")

        text = Txt(w / 2 - 450, 200, lang['LOGINFAIL'], "WHITE")
        text.render()

        text = Txt(w / 2 + 100, 200, lang['NEXT'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = -2 

    elif game_state == 25:
        screen.fill("#96c3d7")

        text = Txt(w / 2 - 450, 200, "CHECKING YOUR FACE", "WHITE")
        text.render()

        # Load player image path to check
        known_image_path = "./player_img/" + log_name + ".png"
        known_image = face_recognition.load_image_file(known_image_path)
        known_face_encoding = face_recognition.face_encodings(known_image)[0]

        # Open the video capture
        cam_port = 0
        cam = cv2.VideoCapture(cam_port)  # Use 0 for default camera

        founded = False
        while True:
            result, image = cam.read()

            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            # Loop through each face found in the frame
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Check if the face matches the known face
                matches = face_recognition.compare_faces([known_face_encoding], face_encoding)

                detected_name = "Cannot verified"
                if matches[0]:
                    detected_name = "Hi " + log_name +" welcome back to game. Please close this window"


                    workbook = openpyxl.load_workbook("players.xlsx")
                    sheet = workbook.active
                    rows = []
                    for row in sheet.iter_rows(values_only=True):
                        rows.append(list(row))

                    game_state = 23

                    i = 0
                    for row in rows:
                        i += 1
                        if row[0] == log_name:
                            isLogin = True
                            player = log_name
                            coin = row[4]
                            pos = i

                    founded = True
                # Draw rectangle around the face
                cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

                # Display the name of the person
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(image, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            # Display the resulting frame
            cv2.imshow('Checking face', image)
            
            if founded:
                break

        btn_exit = Button(w / 2 + 350, 190, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = -2

    # Minigame
    elif game_state == 3:
        mg_tick -= 1

        # change mouse pos after 0.5s
        if mg_tick % 15 == 0:
            x_add = random.random() * 40 - 20
            y_add = random.random() * 40 - 20
        mg_mouse_x = mg_mouse[0]
        mg_mouse_x += x_add
        # when mouse go to screen border
        if mg_mouse_x <= 200:
            mg_mouse_x = w - 200
        if mg_mouse_x >= w - 200:
            mg_mouse_x = 200
        mg_mouse_y = mg_mouse[1]
        mg_mouse_y += y_add
        # when mouse go to screen border
        if mg_mouse_y <= h - 500:
            mg_mouse_y = h - 200
        if mg_mouse_y >= h - 200:
            mg_mouse_y = h - 500
        mg_mouse = (mg_mouse_x, mg_mouse_y)

        # time went off
        if (mg_tick == 0):
            game_state = -2
            pygame.mixer.Sound("./Minigame/MG-Win.mp3").play()

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            pygame.mixer.music.load("./Asset/BG-Music-1.mp3")
            pygame.mixer.music.play(-1, 0, 2000)

            # plus gameplay coin to player's coin
            coin += collected_coin

        screen.fill("#96c3d7")
        btn_exit = Button(w / 2 + 350, 150, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = -2

        bg_grass = Img(0, 0, "./Minigame/MG-Background.png", (2000, 800))
        bg_grass.draw()

        bg_sun = Img(150, 50, "./Minigame/MG-Sun.png", (100, 100))
        bg_sun.draw()

        bg_cloud_x += 1
        if bg_cloud_x >= h:
            bg_cloud_x = 0
        bg_cloud = Img(bg_cloud_x, 100, "./Minigame/MG-Cloud.png", (1200, 100))
        bg_cloud.draw()
        
        text = Txt(300, 100, lang['COLLECTEDCOIN'] + str(collected_coin), "#f06e4b", True, True)
        text.render()

        text = Txt(300, 50, lang['TIME'] + str(int(mg_tick / 30)), "#f06e4b", True, True)
        text.render()

        bg_1 = Player(mg_mouse[0], mg_mouse[1], "./Minigame/MG-Mouse.png", (250, 250))
        bg_1.dir_animate(x_add)
        bg_1.draw()

        mouse_input = pygame.mouse.get_pos()

        mg_hammer = Img(mouse_input[0] - 50, mouse_input[1] - 50, "./Minigame/MG-Hammer.png", (100, 100))
        mg_hammer.draw()

        # The hammer hit the mouse then plus coin and play sound
        if bg_1.isCollide(mouse_input[0], mouse_input[1]):
            if pygame.mouse.get_pressed()[0]:
                collected_coin += 1
                pygame.mixer.Sound("./Minigame/MG-Coin.mp3").play()

                mg_mouse = (random.random() * (w - 200), h - 500 + random.random() * 300)
    # Store 
    elif game_state == 4:
        screen.fill("#96c3d7")

        bg_store = Img(0, 0, "./Asset/BG1.png", (w, h))
        bg_store.draw()

        text = Txt(w / 2 - 300, 100, lang['PLAYER'] + player, "#f06e4b", True)
        text.render()

        text = Txt(w / 2 - 300, 150, lang['COIN'] + str(coin), "#f06e4b", True)
        text.render()

        text = Txt(w / 2 - 300, 200, lang['BOUGHT'] + str(len(prePlayItems)), "WHITE", True)
        text.render()

        item_table = Img(w / 2 - 325, 250, "./Asset/ITEM-Table.png", (700, 300))
        item_table.draw()

        # buy ITEM-1
        if lang['ITEM-1'] not in prePlayItems:
            item_1 = Item(w / 2 - 300, 300, "./Asset/" + lang['ITEM-1'], (100, 100), 10)
            item_1.draw()
            if item_1.isClick():
                value = item_1.getValue()
                if coin >= value:
                    coin -= value
                    prePlayItems.add(lang['ITEM-1'])

        # buy ITEM-2
        if lang['ITEM-2'] not in prePlayItems:
            item_2 = Item(w / 2 - 50, 300, "./Asset/" + lang['ITEM-2'], (100, 100), 10)
            item_2.draw()
            if item_2.isClick():
                value = item_2.getValue()
                if coin >= value:
                    coin -= value
                    prePlayItems.add(lang['ITEM-2'])

        # buy ITEM-3
        if lang['ITEM-3'] not in prePlayItems:
            item_2 = Item(w / 2 + 175, 300, "./Asset/" + lang['ITEM-3'], (100, 100), 10)
            item_2.draw()
            if item_2.isClick():
                value = item_2.getValue()
                if coin >= value:
                    coin -= value
                    prePlayItems.add(lang['ITEM-3'])

        btn_exit = Button(w / 2 + 400, h / 2 + 130, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = -2

    elif game_state == 5:
        screen.fill("#96c3d7")
        text = Txt(300, 50, lang['COIN'] + str(coin), "WHITE", True, True)
        text.render()
        text = Txt(300, 100, lang['BOUGHT'], "GREEN", True, True)
        text.render()
        text = Txt(300, 610, lang['BETCOIN'] + bet_coin, "WHITE", False, True)
        text.render()

        text = Txt(300, 200, lang['CHARSET'] + str(char_set), "WHITE", False, True)
        text.render()
        for i in range(1, 6):
            set_i = Button(i * 150 + 200, 250, "./Asset/char_set_" + str(i) + "/set.png", (100, 100))
            if set_i.isClick():
                char_set = i
            set_i.draw()

        text = Txt(300, 400, lang['LEVEL'] + str(level), "WHITE", False, True)
        text.render()
        for i in range(1, 4):
            set_i = Button(i * 150 + 200, 450, "./Asset/level_" + str(i) + ".png", (100, 100))
            if set_i.isClick():
                level = i
            set_i.draw()

        btn_play = Button(700, 600, "./Asset/" + lang['BTN-PLAY'], (160, 50))
        btn_play.draw()
        btn_exit = Button(w / 2 + 240, 600, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = -2

        if btn_play.isClick():
            if bet_coin == "":
                text = Txt(450, 675, lang['NOT-NULL'], "RED", True, True)
                text.render()
            else:
                if int(bet_coin) * level <= int(coin):
                    game_state = 51
                    minus = int(coin) - int(bet_coin)
                else:
                    text = Txt(450, 90, lang['NOT-ENOUGH'], "RED", True, True)
                    text.render()
                

        for item in enumerate(prePlayItems):
            item = Item(item[0] * 100 + 525, 50, "./Asset/" + item[1], (100, 100), 10)
            item.draw()

    # Main game
    elif game_state == 51:
        # 5 cars
        car_1 = Car(100, 175, "./Asset/char_set_" + str(char_set) + "/background.png", (100, 100), 1, level)
        car_2 = Car(100, 275, "./Asset/char_set_" + str(char_set) + "/player_1_1.png", (100, 100), 1, level)
        car_3 = Car(100, 375, "./Asset/char_set_" + str(char_set) + "/player_1_1.png", (100, 100), 1, level)
        car_4 = Car(100, 475, "./Asset/char_set_" + str(char_set) + "/player_1_1.png", (100, 100), 1, level)
        car_5 = Car(100, 575, "./Asset/char_set_" + str(char_set) + "/player_1_1.png", (100, 100), 1, level)

        # random position of mystery box
        random.seed(time.time())
        pos_x = random.random() * 500 + 500
        pos_y = random.choice([car_1.rect.y, car_2.rect.y, car_3.rect.y, car_4.rect.y, car_5.rect.y]) + 20
        box_1 = Box(pos_x, pos_y, "./Asset/MAIN-MYSTERY.png", (80, 80))
        pos_x = random.random() * 500 + 500
        pos_y = random.choice([car_1.rect.y, car_2.rect.y, car_3.rect.y, car_4.rect.y, car_5.rect.y]) + 20
        box_2 = Box(pos_x, pos_y, "./Asset/MAIN-MYSTERY.png", (80, 80))
        pos_x = random.random() * 500 + 500
        pos_y = random.choice([car_1.rect.y, car_2.rect.y, car_3.rect.y, car_4.rect.y, car_5.rect.y]) + 20
        box_3 = Box(pos_x, pos_y, "./Asset/MAIN-MYSTERY.png", (80, 80))
        game_state = 52
        mg_tick = 0

        # Use items bought in Store
        # Items that bought in store are in prePlayItems
        for value in prePlayItems:
            if value == "ITEM-1.png":
                car_1.itemSpeed(0.2)
            elif value == "ITEM-2.png":
                car_1.rect.x = 200
            elif value == "ITEM-3.png":
                car_1.ignoreSlow = True
        # Win effect
        eff = Eff(w - 200, car_1.rect.y - 100, "./Asset/MAIN-EFFECT.png", (100, 100))

    elif game_state == 52:
        bg_race = Img(0, 0, "./Asset/char_set_" + str(char_set) + "/background.png", (w, h))
        bg_race.draw()

        # Racing lanes
        lane_1 = Img(100, car_1.rect.y + 30, "./Asset/RoadTop.png", (w - 200, 100))
        lane_1.draw()
        lane_2 = Img(100, car_2.rect.y + 30, "./Asset/Road.png", (w - 200, 100))
        lane_2.draw()
        lane_3 = Img(100, car_3.rect.y + 30, "./Asset/Road.png", (w - 200, 100))
        lane_3.draw()
        lane_4 = Img(100, car_4.rect.y + 30, "./Asset/Road.png", (w - 200, 100))
        lane_4.draw()
        lane_5 = Img(100, car_5.rect.y + 30, "./Asset/RoadBot.png", (w - 200, 100))
        lane_5.draw()

        # 5 cars in a race
        car_1.draw(car_1.isWin(w), "./Asset/char_set_" + str(char_set) + "/player_1_1.png", "./Asset/char_set_" + str(char_set) + "/player_1_2.png")
        car_2.draw(car_2.isWin(w), "./Asset/char_set_" + str(char_set) + "/player_2_1.png", "./Asset/char_set_" + str(char_set) + "/player_2_2.png")
        car_3.draw(car_3.isWin(w), "./Asset/char_set_" + str(char_set) + "/player_3_1.png", "./Asset/char_set_" + str(char_set) + "/player_3_2.png")
        car_4.draw(car_4.isWin(w), "./Asset/char_set_" + str(char_set) + "/player_4_1.png", "./Asset/char_set_" + str(char_set) + "/player_4_2.png")
        car_5.draw(car_5.isWin(w), "./Asset/char_set_" + str(char_set) + "/player_5_1.png", "./Asset/char_set_" + str(char_set) + "/player_5_2.png")

        # Lap of players
        text = Txt(car_1.rect.x, car_1.rect.y, "LAP remaining " + str(car_1.lap), "WHITE", True, False, 10)
        text.render()
        text = Txt(car_2.rect.x, car_2.rect.y, "LAP remaining " + str(car_2.lap), "WHITE", True, False, 10)
        text.render()
        text = Txt(car_3.rect.x, car_3.rect.y, "LAP remaining " + str(car_3.lap), "WHITE", True, False, 10)
        text.render()
        text = Txt(car_4.rect.x, car_4.rect.y, "LAP remaining " + str(car_4.lap), "WHITE", True, False, 10)
        text.render()
        text = Txt(car_5.rect.x, car_5.rect.y, "LAP remaining " + str(car_5.lap), "WHITE", True, False, 10)
        text.render()

        # 3 mysteries box
        box_1.draw()
        box_2.draw()
        box_3.draw()

        # Player name && Time
        text = Txt(300, 70, lang['PLAYER'] + player, "#f06e4b", True)
        text.render()

        mg_tick += 1
        text = Txt(300, 120, lang['TIME'] + str(int(mg_tick / 30)), "#f06e4b", True, True)
        text.render()

        # 5 cars hit box_1
        if car_1.isCollide(box_1.getRect()) and box_1.isShow():
            car_1.hitBox(1) # Object take effect
            box_1.disable() # Hide the box
            pygame.mixer.Sound("./Asset/Buy.mp3").play() # Play sound effect
            boost = Img(car_1.rect.x, car_1.rect.y, "./Asset/MAIN-Boost.png", (200, 200))
            boost.draw()
        if car_2.isCollide(box_1.getRect()) and box_1.isShow():
            car_2.hitBox(1)
            box_1.disable()
            pygame.mixer.Sound("./Asset/Buy.mp3").play()
            boost = Img(car_2.rect.x, car_2.rect.y, "./Asset/MAIN-Boost.png", (200, 200))
            boost.draw()
        if car_3.isCollide(box_1.getRect()) and box_1.isShow():
            car_3.hitBox(1)
            box_1.disable()
            pygame.mixer.Sound("./Asset/Buy.mp3").play()
            boost = Img(car_3.rect.x, car_3.rect.y, "./Asset/MAIN-Boost.png", (200, 200))
            boost.draw()
        if car_4.isCollide(box_1.getRect()) and box_1.isShow():
            car_4.hitBox(1)
            box_1.disable()
            pygame.mixer.Sound("./Asset/Buy.mp3").play()
            boost = Img(car_4.rect.x, car_4.rect.y, "./Asset/MAIN-Boost.png", (200, 200))
            boost.draw()
        if car_5.isCollide(box_1.getRect()) and box_1.isShow():
            car_4.hitBox(1)
            box_1.disable()
            pygame.mixer.Sound("./Asset/Buy.mp3").play()
            boost = Img(car_5.rect.x, car_5.rect.y, "./Asset/MAIN-Boost.png", (200, 200))
            boost.draw()

        # 5 cars hit box_2 
        if car_1.isCollide(box_2.getRect()) and box_2.isShow():
            car_1.hitBox(2)
            box_2.disable()
            pygame.mixer.Sound("./Asset/Buy.mp3").play()
            unboost = Img(car_1.rect.x, car_1.rect.y, "./Asset/MAIN-UnBoost.png", (200, 200))
            unboost.draw()
        if car_2.isCollide(box_2.getRect()) and box_2.isShow():
            car_2.hitBox(2)
            box_2.disable()
            pygame.mixer.Sound("./Asset/Buy.mp3").play()
            unboost = Img(car_2.rect.x, car_2.rect.y, "./Asset/MAIN-UnBoost.png", (200, 200))
            unboost.draw()
        if car_3.isCollide(box_2.getRect()) and box_2.isShow():
            car_3.hitBox(2)
            box_2.disable()
            pygame.mixer.Sound("./Asset/Buy.mp3").play()
            unboost = Img(car_3.rect.x, car_3.rect.y, "./Asset/MAIN-UnBoost.png", (200, 200))
            unboost.draw()
        if car_4.isCollide(box_2.getRect()) and box_2.isShow():
            car_4.hitBox(2)
            box_2.disable()
            pygame.mixer.Sound("./Asset/Buy.mp3").play()
            unboost = Img(car_4.rect.x, car_4.rect.y, "./Asset/MAIN-UnBoost.png", (200, 200))
            unboost.draw()
        if car_5.isCollide(box_2.getRect()) and box_2.isShow():
            car_4.hitBox(2)
            box_2.disable()
            pygame.mixer.Sound("./Asset/Buy.mp3").play()
            unboost = Img(car_5.rect.x, car_5.rect.y, "./Asset/MAIN-UnBoost.png", (200, 200))
            unboost.draw()

        # 5 cars hit box_3 
        if car_1.isCollide(box_3.getRect()) and box_3.isShow():
            car_1.hitBox(3)
            box_3.disable()
            pygame.mixer.Sound("./Asset/Buy.mp3").play()
        if car_2.isCollide(box_3.getRect()) and box_3.isShow():
            car_2.hitBox(3)
            box_3.disable()
            pygame.mixer.Sound("./Asset/Buy.mp3").play()
        if car_3.isCollide(box_3.getRect()) and box_3.isShow():
            car_3.hitBox(3)
            box_3.disable()
            pygame.mixer.Sound("./Asset/Buy.mp3").play()
        if car_4.isCollide(box_3.getRect()) and box_3.isShow():
            car_4.hitBox(3)
            box_3.disable()
            pygame.mixer.Sound("./Asset/Buy.mp3").play()
        if car_5.isCollide(box_3.getRect()) and box_3.isShow():
            car_4.hitBox(3)
            box_3.disable()
            pygame.mixer.Sound("./Asset/Buy.mp3").play()

        # if car_n win
        # plus coin
        # stop play game and go to state 52 to show result
        if car_1.won and len(final) == 1:
            eff.draw()
        if car_1.isWin(w):
            if log_name not in final:
                final[log_name] = mg_tick / 30
        if car_2.isWin(w):
            if 'player 2' not in final:
                final['player 2'] = mg_tick / 30
        if car_3.isWin(w):
            if 'player 3' not in final:
                final['player 3'] = mg_tick / 30
        if car_4.isWin(w):
            if 'player 4' not in final:
                final['player 4'] = mg_tick / 30
        if car_5.isWin(w):
            if 'player 5' not in final:
                final['player 5'] = mg_tick / 30

        if len(final) == 5:
            for val in enumerate(final.items()):
                played_time = float("{:.2f}".format(val[1][1]))
                text = Txt(w - 350, 30 * val[0] + 45, str(val[1][0]) + ": " + str(played_time) + " s", "BLACK", False)
                text.render()

            game_state = 53

        keys = [car_1.getPos(), car_2.getPos(), car_3.getPos(), car_4.getPos(), car_5.getPos()]
        values = [log_name, "player 2", "player 3", "player 4", "player 5"]
        top = dict(zip(keys, values))
        top = sorted(top.items(), key=lambda x: x[0], reverse = True)

        rank = Img(w - 400, -10, "./Asset/MAIN-Rank.png", (230, 230))
        rank.draw()

        if len(final) == 0:
            for val in enumerate(top):
                text = Txt(w - 350, 30 * val[0] + 45, str(val[1][1]) + "---" + str(val[1][0]), "BLACK", False)
                text.render()

    # Show result at the end game stage then go to stage 53
    elif game_state == 53:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        pygame.mixer.music.load("./Asset/BG-Music-2.mp3")
        pygame.mixer.music.play(-1, 0, 2000)

        pygame.mixer.Sound("./Minigame/MG-Win.mp3").play()
        text = Txt(w / 2 - 200, 30, lang['WIN'], "WHITE", False)
        text.render()
        # calculate coin
        key = min(final, key=final.get)
        if key == log_name:
            coin += 5 * int(bet_coin) * level
        else:
            coin -= int(bet_coin) * level

        # Save result's image and xlsx file to result folder at main directory
        img_name = str(time.ctime(time.time()))
        img_name = img_name.replace(":", "_")
        pygame.image.save(screen, "./result/" + img_name + ".png")
        wb = load_workbook("./result/results.xlsx")
        sheet = wb.active
        sheet.append([img_name, player, ])
        wb.save("./result/results.xlsx")

        game_state = 54

    # Go to main menu
    elif game_state == 54:
        prePlayItems.clear()
        final.clear()

        btn_exit = Button(w / 2 + 200, 60, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()

        # Stage -2 will jump to stage 0 (Main menu)
        if btn_exit.isClick():
            game_state = -2

    elif game_state == 6:
        bg = Img(0, 0, "./Asset/BG.png", (w, h))
        bg.draw()
        bg_text = Img(w / 2 - 300, h / 5 + 50, "./Asset/" + lang['BG-TITLE'], (700, 125))
        bg_text.draw()
        btn_exit = Button(w / 2 + 400, 400, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()

        bg_text = Img(w / 2 - 300, 100, "./Asset/" + lang['HELP'], (600, 600))
        bg_text.draw()

        if btn_exit.isClick():
            game_state = -2

    pygame.display.update()
    clock.tick(30)