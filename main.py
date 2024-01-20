from game_class import *

# Initialize the game
# Show coin at the beginning of the game
collected_coin = 0
font = pygame.font.Font(None, 50)
text = font.render("COIN: ", True,  "#f06e4b")
text_rect = text.get_rect(center = (100, 50))

# Main background Grass moving animation
bg_1_x = 0
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
EMAIL = ""
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
# win lost ration
win = 0
lost = 0
# sound
mute = False
# online players list
online_players = {}
TICK = 0
# effect
hittedType = 0
hittedTime = 0
# init game_state
game_state = "MAINMENU"
# init sound
SOUND = soundClass()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit

        if event.type == pygame.KEYDOWN and game_state == "CREATE":
            if event.key == pygame.K_RETURN:
                game_state = "CREATE_1" 
                break
            if event.key == pygame.K_BACKSPACE: 
                name = name[:-1] 
            else: 
                name += event.unicode

        if event.type == pygame.KEYDOWN and game_state == "CREATE_1":
            if event.key == pygame.K_RETURN:
                game_state = "CREATE_2" 
                break
            if event.key == pygame.K_BACKSPACE: 
                email = email[:-1] 
            else: 
                email += event.unicode
    
        if event.type == pygame.KEYDOWN and game_state == "CREATE_2":
            if event.key == pygame.K_RETURN:
                game_state = "CREATE_3" 
                break
            if event.key == pygame.K_BACKSPACE: 
                password = password[:-1] 
            else: 
                password += event.unicode

        if event.type == pygame.KEYDOWN and game_state == "LOGIN":
            if event.key == pygame.K_RETURN:
                game_state = "LOGIN_1" 
                break
            if event.key == pygame.K_BACKSPACE: 
                log_name = log_name[:-1] 
            else: 
                log_name += event.unicode
        
        if event.type == pygame.KEYDOWN and game_state == "LOGIN_2":
            if event.key == pygame.K_RETURN:
                break
            if event.key == pygame.K_BACKSPACE: 
                log_password = log_password[:-1] 
            else: 
                log_password += event.unicode

        if event.type == pygame.KEYDOWN and game_state == "MAINGAME":
            if event.key == pygame.K_RETURN:
                game_state = "MAINGAME_1" 
                break
            if event.key == pygame.K_BACKSPACE: 
                bet_coin = bet_coin[:-1] 
            else: 
                bet_coin += event.unicode
    # get game's windows width and height
    w, h = pygame.display.get_surface().get_size()

    # Load main menu
    if game_state == "MAINMENU":

        bg = Img(0, 0, "./Asset/BG.png", (w, h))
        bg.draw()
        bg_text = Img(w / 2 - 300, h / 5 + 50, "./Asset/" + lang['BG-TITLE'], (700, 125))
        bg_text.draw()

        bg_1_x -= 2
        if bg_1_x <= -1000:
            bg_1_x = 0 
        bg_1 = Img(bg_1_x, h - 250, "./Asset/BG3.png", (4000, 250))
        bg_1.draw()

        btn_exit = Button(w / 2 + 275, 97, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        btn_help = Button(w / 2 + 325, 90, "./Asset/Help.png", (60, 60))
        btn_help.draw()
        btn_rank = Button(w / 2 + 385, 100, "./Asset/Rank.png", (45, 45))
        btn_rank.draw()

        btn_sound_mute = soundState(w / 2 + 340, 540, "./Asset/Mute.png", (45, 45))
        btn_sound_mute.draw()
        btn_sound_unmute = soundState(w / 2 + 400, 540, "./Asset/UnMute.png", (45, 45))
        btn_sound_unmute.draw()
        if btn_sound_mute.isClick():
            SOUND.setMute()
        if btn_sound_unmute.isClick():
            SOUND.setUnMute()


        if btn_help.isClick():
            game_state = "HELP"

        if btn_rank.isClick():
            game_state = "RANK" 

        if btn_exit.isClick():
            exit()

        btn_create_account = Button(w / 2 + 100, 98, "./Asset/" + lang['CREATE'], (160, 50))
        btn_create_account.draw()
        if btn_create_account.isClick():
            game_state = "CREATE" 
            SOUND.changeSound("./Asset/BG-Music-1.mp3")

        if isLogin:
            avata = Button(w / 2 - 305, 85, "./player_img/" + log_name + ".png", (50, 50))
            avata.draw()
            if avata.isClick():
                game_state = "PROFILE" 

            text = Txt(w / 2 - 240, 100, player, "#f06e4b", True)
            text.render()
            text = Txt(w / 2 - 300, 150, lang['COIN'] + str(coin), "#f06e4b")
            text.render()
            btn_play = Button(w / 2 - 350, h / 2, "./Asset/" + lang['BTN-PLAY'], (160, 50))
            btn_play.draw()
            if btn_play.isClick():
                game_state = "MAINGAME" 
                SOUND.changeSound("./Asset/BG-Music-1.mp3")

            btn_minigame = Button(w / 2 - 350, h / 2 + 75 , "./Asset/" + lang['BTN-MINIGAME'], (160, 50))
            btn_minigame.draw()
            if btn_minigame.isClick():
                if coin <= 10:
                    game_state = "MINIGAME" 
                    mg_tick = 300
                    collected_coin = 0
                    SOUND.changeSound("./Asset/BG-Music-1.mp3")
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
                else:
                    text = Txt(w / 2 - 400, h - 55, lang['MINIGAME-LIMIT'], "RED", True, True)
                    text.render()

            btn_shop = Button(w / 2 - 350, h / 2 + 150 , "./Asset/" + lang['STORE'], (160, 50))
            btn_shop.draw()
            if btn_shop.isClick():
                game_state = "STORE" 
                SOUND.changeSound("./Asset/BG-Music-1.mp3")
        else:
            btn_login = Button(w / 2 - 70, 98, "./Asset/" + lang['LOGIN'], (160, 50))
            btn_login.draw()
            if btn_login.isClick():
                game_state = "LOGIN" 
                SOUND.changeSound("./Asset/BG-Music-1.mp3")

        # refresh online status in 5s
        if (isLogin):
            text = Txt(w / 2 + 100, 150, lang['ONLINE'], False, False)
            text.render()
            try:
                if TICK % 300 == 0:
                    response = requests.get(online_url + 'get_online_players')
                    if response.status_code == 200:
                        online_players = response.json()
                if TICK % 300 == 150:
                    timestamp = time.time()
                    data = {'player_id': log_name, 'timestamp': timestamp}
                    response = requests.post(online_url + 'check_online', json=data, timeout=1)
            except:
                print("Error connecting to server")

        for online_player in enumerate(online_players.items()):
            text = Txt(w / 2 + 100, 180 + 30 * online_player[0], str(online_player[1][0]), "WHITE")
            text.render()
        #----------------------------------------------------

        text = Txt(w / 2 + 175, 550, lang['LANG'], "WHITE", True, True)
        text.render()

        if text.isClick():
            game_state = "REFRESH"  # -1

    # Change language state
    elif game_state == "REFRESH":
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

        game_state = "EXIT" 

    elif game_state == "EXIT": # -2
        game_state = "MAINMENU" 
        SOUND.changeSound("./Asset/BG-Music-2.mp3")

    # Create account state
    elif game_state == "CREATE":
        bg = Img(0, 0, "./Asset/BGRace.png", (w, h))
        bg.draw()
        text = Txt(w / 2 - 450, 200, lang['ENTERYOURNAME'] + name, "WHITE")
        text.render()
        text = Txt(w / 2 + 250, 200, lang['NEXT'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = "CREATE_1" 
        
        btn_exit = Button(w / 2 + 275, 250, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = "EXIT"
       
    elif game_state == "CREATE_1":
        bg = Img(0, 0, "./Asset/BGRace.png", (w, h))
        bg.draw()
        text = Txt(w / 2 - 450, 200, lang['ENTERYOUREMAIL'] + email, "WHITE")
        text.render()
        text = Txt(w / 2 + 350, 200, lang['NEXT'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = "CREATE_2" 
    
        btn_exit = Button(w / 2 + 275, 250, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = "EXIT" 

    elif game_state == "CREATE_2":
        bg = Img(0, 0, "./Asset/BGRace.png", (w, h))
        bg.draw()
        text = Txt(w / 2 - 450, 200, lang['ENTERYOURPASSWORD'] + password, "WHITE")
        text.render()
        text = Txt(w / 2 + 250, 200, lang['NEXT'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = "CREATE_3" 

        btn_exit = Button(w / 2 + 275, 250, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = "EXIT" 

    elif game_state == "CREATE_3":
        bg = Img(0, 0, "./Asset/BGRace.png", (w, h))
        bg.draw()
        text = Txt(w / 2 - 450, 200, lang['TAKEYOURPICTURE'], "WHITE")
        text.render()
        text = Txt(w / 2 + 350, 260, lang["TAKE"], "WHITE", True, True)
        text.render()

        if text.isClick():
            game_state = "EXIT"
            cam_port = 0
            cam = VideoCapture(cam_port)

            result, image = cam.read()
            if result:
                game_state = "CREATE_4" 
                imshow("Taken Picture", image)
                imwrite("./player_img/" + name + ".png", image)
                info.append(name)
                info.append(email)
                info.append(name + ".png")
                info.append(password)
                info.append(10) # Give 10 coin to new player
                info.append(0)
                info.append(0)

                wb = load_workbook("players.xlsx")
                sheet = wb.active
                sheet.append(info)
                wb.save("players.xlsx")

                sendMail(GAME_EMAIL, GAME_TOKEN, info[1], GAME_SUBJECT , GAME_CONTENT) 

        btn_exit = Button(w / 2 + 275, 250, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = "EXIT" 

    elif game_state == "CREATE_4":
        bg = Img(0, 0, "./Asset/BGRace.png", (w, h))
        bg.draw()
        text = Txt(w / 2 - 450, 200, lang['CREATESUCCESSFULLY'], "WHITE")
        text.render()
        text = Txt(w / 2 + 250, 200, lang['NEXT'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = "EXIT"

    elif game_state == "LOGIN":
        bg = Img(0, 0, "./Asset/BGRace.png", (w, h))
        bg.draw()
        text = Txt(w / 2 - 450, 200, lang['ENTERYOURNAME'] + log_name, "WHITE")
        text.render()
        text = Txt(w / 2 + 250, 200, lang['NEXT'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = "LOGIN_1" 

        btn_exit = Button(w / 2 + 350, 190, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = "EXIT" 

    elif game_state == "LOGIN_1":
        bg = Img(0, 0, "./Asset/BGRace.png", (w, h))
        bg.draw()
        text = Txt(w / 2 - 450, 200, lang['USERANDPASSWORD'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = "LOGIN_2"

        text = Txt(w / 2 - 450, 250, lang['FACERECOGNITION'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = "LOGIN_3" 

        btn_exit = Button(w / 2 + 350, 190, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = "EXIT" 

    elif game_state == "LOGIN_2":
        bg = Img(0, 0, "./Asset/BGRace.png", (w, h))
        bg.draw()

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
            game_state = "LOGIN_4"
            i = 0
            for row in rows:
                i += 1
                if (row[0] == log_name and row[3] == log_password):
                    game_state = "LOGIN_3" 
                    isLogin = True
                    EMAIL = row[1]
                    player = log_name
                    coin = row[4]
                    win = row[5]
                    lost = row[6]
                    pos = i
                    break
            workbook.close()
    
        btn_exit = Button(w / 2 + 350, 190, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = "EXIT" 

    elif game_state == "LOGIN_3":
        bg = Img(0, 0, "./Asset/BGRace.png", (w, h))
        bg.draw()
        text = Txt(w / 2 - 450, 200, lang['LOGINSUCCESSFULLY'], "WHITE")
        text.render()
        text = Txt(w / 2 + 100, 200, lang['NEXT'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = "EXIT" 

    elif game_state == "LOGIN_4":
        bg = Img(0, 0, "./Asset/BGRace.png", (w, h))
        bg.draw()
        text = Txt(w / 2 - 450, 200, lang['LOGINFAIL'], "WHITE")
        text.render()
        text = Txt(w / 2 + 100, 200, lang['NEXT'], "WHITE", True, True)
        text.render()
        if text.isClick():
            game_state = "EXIT"

    elif game_state == "LOGIN_5":
        g = Img(0, 0, "./Asset/BGRace.png", (w, h))
        bg.draw()
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

                    game_state = "LOGIN_3"

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
            game_state = "EXIT"

    # Minigame
    elif game_state == "MINIGAME":
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
        if (mg_tick == 0 or collected_coin == 20):
            game_state = "EXIT"
            SOUND.changeSound("./Asset/BG-Music-1.mp3")

            # plus gameplay coin to player's coin
            coin += collected_coin

        screen.fill("#96c3d7")
        btn_exit = Button(w / 2 + 350, 150, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = "EXIT"

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
                if not SOUND.isMute:
                    SOUND.playeEffect("./Minigame/MG-Coin.mp3")

                mg_mouse = (random.random() * (w - 200), h - 500 + random.random() * 300)
    # Store 
    elif game_state == "STORE":
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
            item_1 = Item(w / 2 - 300, 300, "./Asset/" + lang['ITEM-1'], (100, 100), 40)
            item_1.draw()
            if item_1.isClick():
                value = item_1.getValue()
                if coin >= value:
                    coin -= value
                    prePlayItems.add(lang['ITEM-1'])

        # buy ITEM-2
        if lang['ITEM-2'] not in prePlayItems:
            item_2 = Item(w / 2 - 50, 300, "./Asset/" + lang['ITEM-2'], (100, 100), 30)
            item_2.draw()
            if item_2.isClick():
                value = item_2.getValue()
                if coin >= value:
                    coin -= value
                    prePlayItems.add(lang['ITEM-2'])

        # buy ITEM-3
        if lang['ITEM-3'] not in prePlayItems:
            item_2 = Item(w / 2 + 175, 300, "./Asset/" + lang['ITEM-3'], (100, 100), 20)
            item_2.draw()
            if item_2.isClick():
                value = item_2.getValue()
                if coin >= value:
                    coin -= value
                    prePlayItems.add(lang['ITEM-3'])

        btn_exit = Button(w / 2 + 400, h / 2 + 130, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()
        if btn_exit.isClick():
            game_state = "EXIT"

    elif game_state == "MAINGAME":
        screen.fill("#96c3d7")
        bg = Img(0, 0, "./Asset/BG1.png", (w, h))
        bg.draw()
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
            game_state = "EXIT"

        if btn_play.isClick():
            try:
                bet_coin_int = int(bet_coin)
                if bet_coin_int < 10:
                    text = Txt(w / 2 - 340, h - 50, lang['NOT-VALID'], "RED", True, True)
                    text.render()
                elif (bet_coin_int >= 0) and (bet_coin_int < int(coin)):
                    game_state = "MAINGAME_1" 
                else:
                    text = Txt(w / 2 - 340, h - 50, lang['NOT-ENOUGH'], "RED", True, True)
                    text.render()
            except:
                text = Txt(w / 2 - 340, h - 50, lang['NOT-NULL'], "RED", True, True)
                text.render()
                

        for item in enumerate(prePlayItems):
            item = Item(item[0] * 100 + 525, 50, "./Asset/" + item[1], (100, 100), 10)
            item.draw()

    # Main game
    elif game_state == "MAINGAME_1":
        # 5 cars
        car_1 = Car(100, 175, "./Asset/char_set_" + str(char_set) + "/background.png", (100, 100), 1, level)
        car_2 = Car(100, 275, "./Asset/char_set_" + str(char_set) + "/player_1_1.png", (100, 100), 1, level)
        car_3 = Car(100, 375, "./Asset/char_set_" + str(char_set) + "/player_1_1.png", (100, 100), 1, level)
        car_4 = Car(100, 475, "./Asset/char_set_" + str(char_set) + "/player_1_1.png", (100, 100), 1, level)
        car_5 = Car(100, 575, "./Asset/char_set_" + str(char_set) + "/player_1_1.png", (100, 100), 1, level)

        # random position of mystery boxes
        pos_x = random.random() * 600 + 200
        pos_y = random.choice([car_1.rect.y, car_2.rect.y, car_3.rect.y, car_4.rect.y, car_5.rect.y]) + 20
        box_1 = Box(pos_x, pos_y, "./Asset/MAIN-MYSTERY.png", (80, 80))
        pos_x = random.random() * 600 + 200
        pos_y = random.choice([car_1.rect.y, car_2.rect.y, car_3.rect.y, car_4.rect.y, car_5.rect.y]) + 20
        box_2 = Box(pos_x, pos_y, "./Asset/MAIN-MYSTERY.png", (80, 80))
        pos_x = random.random() * 600 + 200
        pos_y = random.choice([car_1.rect.y, car_2.rect.y, car_3.rect.y, car_4.rect.y, car_5.rect.y]) + 20
        box_3 = Box(pos_x, pos_y, "./Asset/MAIN-MYSTERY.png", (80, 80))
        game_state = "MAINGAME_2" 
        mg_tick = 0

        # random position of rocks
        pos_x = random.random() * 600 + 200
        pos_y = random.choice([car_1.rect.y, car_2.rect.y, car_3.rect.y, car_4.rect.y, car_5.rect.y]) + 20
        rock_1 = Obstacle(pos_x, pos_y, "./Asset/MAIN-Rock.png", (100, 100))
        pos_x = random.random() * 600 + 200
        pos_y = random.choice([car_1.rect.y, car_2.rect.y, car_3.rect.y, car_4.rect.y, car_5.rect.y]) + 20
        rock_2 = Obstacle(pos_x, pos_y, "./Asset/MAIN-Rock.png", (100, 100))
        pos_x = random.random() * 600 + 200
        pos_y = random.choice([car_1.rect.y, car_2.rect.y, car_3.rect.y, car_4.rect.y, car_5.rect.y]) + 20
        rock_3 = Obstacle(pos_x, pos_y, "./Asset/MAIN-Rock.png", (100, 100))

        # Use items bought in Store
        # Items that bought in store are in prePlayItems
        for value in prePlayItems:
            if value == "ITEM-1.png":
                car_1.itemSpeed(0.15)
            elif value == "ITEM-2.png":
                car_1.rect.x = 200
            elif value == "ITEM-3.png":
                car_1.ignoreSlow = True
        # Win effect
        eff = Eff(w - 200, car_1.rect.y - 100, "./Asset/MAIN-EFFECT.png", (100, 100))

    elif game_state == "MAINGAME_2":
        bg_race = Img(0, 0, "./Asset/char_set_" + str(char_set) + "/background.png", (w, h))
        bg_race.draw()

        # Player name && Time
        text = Txt(300, 70, lang['PLAYER'] + player, "#f06e4b", True)
        text.render()

        mg_tick += 1
        text = Txt(300, 120, lang['TIME'] + str(int(mg_tick / 30)), "#f06e4b", True, True)
        text.render()

        players_list = [car_1, car_2, car_3, car_4, car_5]
        boxes = [box_1, box_2, box_3]
        obstacles = [rock_1, rock_2, rock_3]
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
        for i in enumerate(players_list):
            i[1].draw(i[1].isWin(w), "./Asset/char_set_" + str(char_set) + "/player_" + str(i[0] + 1) + "_1.png", "./Asset/char_set_" + str(char_set) + "/player_" + str(i[0] + 1) + "_2.png")

        # Lap of players
        for i in players_list:
            text = Txt(i.rect.x, i.rect.y, "LAP remaining " + str(i.lap), "WHITE", True, False, 10)
            text.render()

        # 3 mysterie boxes
        for i in boxes:
            i.draw()

        # 5 cars hit boxs
        for i in players_list:
            for j in enumerate(boxes):
                if i.isCollide(j[1].rect) and j[1].isActive:
                    i.hitBox(j[0] + 1)
                    j[1].disable()
                    if not SOUND.isMute:
                        SOUND.playEffect("./Asset/Buy.mp3")

                    hittedType = j[0] + 1
                    hittedTime = 50

        if hittedTime > 0:
            hittedTime -= 1
            boost = Eff(i.rect.x, i.rect.y, "./Asset/MAIN-MYSTERY-" + str(hittedType) + ".png", (200, 200))
            boost.draw()

        # 3 rocks
        for i in obstacles:
            i.draw()

        # 5 cars hit boxs
        for i in players_list:
            for j in enumerate(obstacles):
                if i.isCollide(j[1].rect) and j[1].isActive:
                    i.hitObs(j[0] + 1)
                    j[1].disable()
                    pygame.mixer.Sound("./Asset/HitObs.mp3").play() # Play sound effect

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
            rank = Img(w / 2 - 200, 180, "./Asset/MAIN-RANK.png", (440, 230))
            rank.draw()
            for val in enumerate(final.items()):
                played_time = float("{:.2f}".format(val[1][1]))
                text = Txt(w / 2 - 140, 30 * val[0] + 240, str(val[1][0]) + ": " + str(played_time) + " s", "BLACK", False)
                text.render()

            game_state = "MAINGAME_3" 

        keys = [car_1.getPos(), car_2.getPos(), car_3.getPos(), car_4.getPos(), car_5.getPos()]
        values = [log_name, "player 2", "player 3", "player 4", "player 5"]
        top = dict(zip(keys, values))
        top = sorted(top.items(), key=lambda x: x[0], reverse = True)

        rank = Img(w - 400, -10, "./Asset/MAIN-Rank.png", (290, 230))
        rank.draw()

        if len(final) == 0:
            for val in enumerate(top):
                text = Txt(w - 350, 30 * val[0] + 45, str(val[1][1]) + "---" + str(val[1][0]), "BLACK", False)
                text.render()

    # Show result at the end game stage then go to stage 53
    elif game_state == "MAINGAME_3":
        SOUND.changeSound("./Asset/BG-Music-1.mp3")
        text = Txt(300, 30, lang['WIN'], "WHITE", False)
        text.render()
        # calculate coin
        key = min(final, key=final.get)
        gain_coin = 0
        if key == log_name:
            win += 1
            gain_coin = 5 * int(bet_coin)
        else:
            lost += 1
            gain_coin = -int(bet_coin)
        # Sync with server
        coin += gain_coin
        # Save result's image and xlsx file to result folder at main directory
        img_name = str(time.ctime(time.time()))
        img_name = img_name.replace(":", "_")
        pygame.image.save(screen, "./result/" + img_name + ".png")
        wb = load_workbook("./result/results.xlsx")
        sheet = wb.active
        sheet.append([img_name, player, gain_coin])
        wb.save("./result/results.xlsx")

        game_state = "MAINGAME_4" 

    # Go to main menu
    elif game_state == "MAINGAME_4":
        prePlayItems.clear()
        final.clear()

        if isLogin:
            wb = load_workbook("players.xlsx")
            sheet = wb.active
            sheet['A' + chr(pos + 48)] = log_name 
            sheet['B' + chr(pos + 48)] = EMAIL
            sheet['C' + chr(pos + 48)] = log_name + '.png'
            sheet['D' + chr(pos + 48)] = log_password
            sheet['E' + chr(pos + 48)] = coin
            sheet['F' + chr(pos + 48)] = win
            sheet['G' + chr(pos + 48)] = lost
            if int(lost):
                ratio = int(win) / int(lost)
                f_ratio = float("{:.2f}".format(ratio))
                sheet['H' + chr(pos + 48)] = f_ratio
            wb.save("players.xlsx")

        btn_exit = Button(w / 2 + 100, 400, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()

        # Stage -2 will jump to stage 0 (Main menu)
        if btn_exit.isClick():
            game_state = "EXIT"
    # help
    elif game_state == "HELP":
        bg = Img(0, 0, "./Asset/BGRace.png", (w, h))
        bg.draw()
        copyr = Txt(w - 450, h - 35, "Copyright G9-23CTT1-HCMUS", "WHITE")
        copyr.render()
        btn_exit = Button(w / 2 + 400, 400, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()

        bg_text = Img(w / 2 - 300, 100, "./Asset/" + lang['HELP'], (600, 600))
        bg_text.draw()

        if btn_exit.isClick():
            game_state = "EXIT"
    # profile
    elif game_state == "PROFILE":
        bg = Img(0, 0, "./Asset/BG.png", (w, h))
        bg.draw()
        btn_exit = Button(w / 2 + 400, 400, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()

        text = Txt(w / 2 - 300, 120, log_name, "WHITE")
        text.render()
        text = Txt(w / 2 - 300, 160, lang['COIN'] + str(coin), "WHITE")
        text.render()
        text = Txt(w / 2 - 300, 200, "WIN: " + str(win), "GREEN")
        text.render()
        text = Txt(w / 2 - 300, 240, "LOST: " + str(lost), "RED")
        text.render()
        if lost:
            ratio = float("{:.2f}".format(win / lost))
            text = Txt(w / 2 - 300, 280, "K/D RATIO: " + str(ratio), "ORANGE")
            text.render()

        if btn_exit.isClick():
            game_state = "EXIT"

    elif game_state == "RANK":
        bg = Img(0, 0, "./Asset/BG.png", (w, h))
        bg.draw()
        btn_exit = Button(w / 2 + 400, 400, "./Asset/ExitGame.png", (50, 50))
        btn_exit.draw()

        workbook = openpyxl.load_workbook("players.xlsx")
        sheet = workbook.active
        rows = []
        for row in sheet.iter_rows(values_only=True):
            rows.append(list(row))

        rows.pop(0)
        new_rows = sorted(rows, key=lambda x : x[4], reverse=True)
        for row in enumerate(new_rows):
            r_name = row[1][0]
            r_coin = row[1][4]
            r_win = row[1][5]
            r_lost = row[1][6]
            r_ratio = row[1][7]

            text = Txt(w / 2 - 450, 50 * row[0] + 100, str(row[0] + 1), "GREEN")
            text.render()
            text = Txt(w / 2 - 420, 50 * row[0] + 100, r_name, "WHITE")
            text.render()
            text = Txt(w / 2 - 240, 50 * row[0] + 100, lang['COIN'] + str(r_coin), "WHITE")
            text.render()
            text = Txt(w / 2 - 80, 50 * row[0] + 100, "WIN: " + str(r_win), "GREEN")
            text.render()
            text = Txt(w / 2 + 45, 50 * row[0] + 100, "LOST: " + str(r_lost), "RED")
            text.render()

            if int(r_lost):
                text = Txt(w / 2 + 200, 50 * row[0] + 100, "K/D ratio: " + str(r_ratio), "ORANGE")
                text.render()

        workbook.close()

        if btn_exit.isClick():
            game_state = "EXIT"
            
    TICK += 1
    pygame.display.update()
    clock.tick(30)