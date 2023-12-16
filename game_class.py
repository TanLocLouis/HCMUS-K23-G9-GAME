import pygame

import random

from cv2 import VideoCapture
from cv2 import imshow
from cv2 import imwrite

from openpyxl import Workbook
from openpyxl import load_workbook
import openpyxl

from email.message import EmailMessage
import ssl
import smtplib

import cv2
import face_recognition

import time

import requests
import socket
# for testing
# server_url = 'http://192.168.10.9:80/'

# for product
server_url = 'http://game.tltech.asia/'
online_url = 'http://online.tltech.asia/'

pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("BET69 - NHA CAI DEN TU CHAU A")
pygame.display.set_icon(pygame.image.load("./Asset/BG-Title.png"))
clock = pygame.time.Clock()

class Eff():
    def __init__(self, x, y, image, scale):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.frame = 150

    def draw(self):
        if self.frame > 0:
            self.rect.topleft = (self.rect.topleft[0], self.rect.topleft[1] + 1)
            screen.blit(self.image, self.rect)
            self.frame -= 1

class Car():
    """
    Game's players class
    """
    def __init__(self, x, y, image, scale, speed = 0, lap = 1):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.startPos = (x, y)
        self.rect.topleft = (x, y)
        self.speed = speed
        self.ani = 0
        self.lap = lap - 1
        self.won = False
        self.ignoreSlow = False
        self.isFreeze = False
        self.Freeze = 90

        random.seed(time.time())

    def isWin(self, border):
        if self.rect.topleft[0] >= border - 200:
            if (self.lap > 0):
                self.rect.x = self.startPos[0]
                self.lap -= 1
                return False
            else:
                self.won = True
                return True

    def draw(self, isWin, img_1, img_2):
        if not self.isFreeze:
            if not self.won:
                if int(self.ani / 10) % 2 == 0:
                    self.image = pygame.image.load(img_1)
                    self.image = pygame.transform.scale(self.image, (100, 100))
                else:
                    self.image = pygame.image.load(img_2)
                    self.image = pygame.transform.scale(self.image, (100, 100))
                self.ani += 1
            else:
                self.image = pygame.image.load(img_1)
                self.image = pygame.transform.scale(self.image, (100, 100))

            if not isWin:
                self.rect.topleft = (self.rect.topleft[0] + self.speed + random.random() * 2, self.rect.topleft[1])
            screen.blit(self.image, self.rect)
        else:
            self.Freeze -= 1
            self.image = pygame.image.load("./Asset/Glacier.png")
            self.image = pygame.transform.scale(self.image, (100, 100))

            self.rect.topleft = (self.rect.topleft[0], self.rect.topleft[1])
            screen.blit(self.image, self.rect)

        if self.Freeze == 0:
            self.isFreeze = False
            self.Freeze = 90

    def getPos(self):
        return self.rect.x

    def isCollide(self, rect):
        return self.rect.collidepoint(rect.topleft[0], rect.topleft[1])

    def itemSpeed(self, speed):
        self.speed += speed

    def hitBox(self, option):
        if option == 1:
            self.speed += 0.2 # increase 0.2 speed
        elif option == 2 and self.speed > 0.5:
            self.speed -= 0.5 # slow down 0.5 speed
        elif option == 3:
            self.rect.x = 650 # go to end
    
    def hitObs(self, option):
        if option == 1: 
            self.rect.x -= 20 # go back 20
        elif option == 2 and not self.ignoreSlow: 
            self.rect.x -= 50 # go back 50, but NOT EFFECT WHEN USED IGNORE ITEM 3 IN STORE
        elif option == 3: 
            self.isFreeze = True # Freeze 3 seconds
         
class Box():
    """
    Mystery Box to gain valuable items class
    """
    def __init__(self, x, y, image, scale):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.isActive = False
        self.fallPos = 50
        random.seed(time.time())

    def draw(self):
        if not self.isActive:
            if random.random() * 1000 <= 5:
                self.isActive = True
                self.fallPos = 50
        
        if self.isActive:
            if self.fallPos:
                self.fallPos -= 1
            screen.blit(self.image, (self.rect.x, self.rect.y - self.fallPos))

    def getRect(self):
        return self.rect
    
    def disable(self):
        self.rect.y = random.random() * 450 + 180
        self.isActive = False

    def isShow(self):
        return self.isActive

class Obstacle():
    """
    Obstacle to slow player class
    """
    def __init__(self, x, y, image, scale):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.isActive = False
        self.fallPos = 50
        random.seed(time.time())

    def draw(self):
        if not self.isActive:
            if random.random() * 1000 <= 5:
                self.isActive = True
                self.fallPos = 50
        
        if self.isActive:
            if self.fallPos >= 0:
                self.fallPos -= 1
            screen.blit(self.image, (self.rect.x, self.rect.y + self.fallPos))

    def getRect(self):
        return self.rect
    
    def disable(self):
        self.rect.y = random.random() * 450 + 180
        self.isActive = False

    def isShow(self):
        return self.isActive
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
    
    def dir_animate(self, value):
        if (value >= 0):
            self.image = pygame.transform.flip(self.image, 1, 0)

# Text Class
class Txt():
    def __init__(self, x, y, content, color, isBorder = False, isClickable = False, size = 30):
        font = pygame.font.Font('BDLifelessGrotesk-Bold.otf', size)
        self.text = font.render(content, True, color)
        self.rect = self.text.get_rect()
        self.rect.topleft = (x, y)
        self.isBorder = isBorder
        self.isClickable = isClickable

    def render(self):
        if self.isBorder:
            rect_color = "#726f6f"
            rect_position = (self.rect.x - 5, self.rect.y - 5)
            rect_size = (self.text.get_width() + 10, self.text.get_height() + 10)
            
            pygame.draw.rect(screen, rect_color, (rect_position, rect_size))
        
        if self.isClickable:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.text = pygame.transform.scale(self.text, (self.text.get_width() * 1.05, self.text.get_height() * 1.05))
                self.rect = self.text.get_rect(center = self.rect.center)

        screen.blit(self.text, self.rect)

    def isClick(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            return True
        else:
            return False

# Image Class
class Img():
    def __init__(self, x, y, image, scale):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Item Class
class Item():
    def __init__(self, x, y, image, scale, value):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.value = value

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * 1.1, self.image.get_height() * 1.1))
        screen.blit(self.image, (self.rect.x, self.rect.y))

    
    def isClick(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            pygame.mixer.Sound("./Asset/Buy.mp3").play()
            return True
        else:
            return False  

    def getValue(self):
        return self.value

# Button Class
class Button():
    def __init__(self, x, y, image, scale):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.scale = scale

    def isClick(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            return True
        else:
            return False  

    def draw(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * 1.1, self.image.get_height() * 1.1))
            self.rect = self.image.get_rect(center = self.rect.center)

        screen.blit(self.image, self.rect)

# Mute and UnMute Class
class soundState():
    def __init__(self, x, y, image, scale):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.scale = scale

    def isClick(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            return True
        else:
            return False  

    def draw(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * 1.1, self.image.get_height() * 1.1))
            self.rect = self.image.get_rect(center = self.rect.center)

        screen.blit(self.image, self.rect)


# Send mail to player after create account
def sendMail(sender, password, receiver, subject, body):
    mail = EmailMessage()
    mail['From'] = sender
    mail['To'] = receiver
    mail['Subject'] = subject
    mail.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, mail.as_string())