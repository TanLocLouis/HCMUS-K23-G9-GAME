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

pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("Et Bi 99 - NHA CAI DEN TU CHAU A")
clock = pygame.time.Clock()

class Car():
    def __init__(self, x, y, image, scale, speed = 0):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed

        random.seed(time.time())

    def draw(self):
        self.rect.topleft = (self.rect.topleft[0] + self.speed + random.random() * 2, self.rect.topleft[1])
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def isCollide(self, rect):
        return self.rect.collidepoint(rect.topleft[0], rect.topleft[1])

    def itemSpeed(self, speed):
        self.speed += speed

    def hitBox(self, speed):
        option = random.random() * 50 

        if option <= 10:
            self.speed += speed
        elif option <= 20:
            self.speed -= speed
        elif option <= 30:
            self.rect.topleft = (200, self.rect.topleft[1])
        elif option <= 40:
            self.speed *= -1

    def isWin(self, border):
        return self.rect.topleft[0] >= border - 200 
         
class Box():
    def __init__(self, x, y, image, scale):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.isActive = False
        random.seed(time.time())

    def draw(self):
        if not self.isActive:
            if random.random() * 1000 <= 4:
                self.isActive = True
        
        if self.isActive:
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def getRect(self):
        return self.rect
    
    def disable(self):
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