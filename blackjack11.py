#!/usr/bin/env python

import pygame
import random
import time

pygame.init()
screen = pygame.display.set_mode((800,600),pygame.RESIZABLE)
pygame.display.set_caption('BlackJack!')
clock = pygame.time.Clock()

white = (255,255,255)
black = (0,0,0)
green = (0,200,0)
brightGreen = (0,255,0)
red = (200,0,0)
brightRed = (255,0,0)
blue = (0,0,200)
brightBlue = (0,0,255)

path = '/home/shane/programming/python/blackjack/'

cards = [i.strip() for i in open(str(path)+'cards.txt').readlines()]

bgImg = pygame.image.load(str(path)+'background.jpg')
bgImg = pygame.transform.scale(bgImg,(800,600))

pValues = []
dValues = []
pHand = []
dHand = []

pot = 100
px = 125
py = 400
dx = 575
dy = 20
pDraw = 4
dDraw=pDraw+1

def text_objects(text,font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def intro():
    intro = True
    while intro:
        introImg = pygame.image.load(str(path)+'intro.jpg')
        introImg = pygame.transform.scale(introImg,(800,600))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                    introImg = pygame.transform.scale(introImg,(1024,768))

        screen.blit(introImg,(0,0))
        font = pygame.font.SysFont('freesansbold.ttf',75)
        text = font.render('Welcome to', True, white)
        screen.blit(text,(250,40))

        font = pygame.font.SysFont('freesansbold.ttf',25)
        text = font.render('Press "f" to toggle fullscreen',True,white)
        screen.blit(text,(0,0))

        introButtons('Play!',100,450,100,50, green,brightGreen,'play')
        introButtons('Quit!',600,450,100,50,red,brightRed,'quit')

        pygame.display.flip()
        clock.tick(15)


def introButtons(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x,y,w,h))
        text1 = pygame.font.Font('freesansbold.ttf',35)
        TextSurf, TextRect = text_objects(msg,text1)
        TextRect.center = (((x+100/2)), (450+(50/2)))
        screen.blit(TextSurf, TextRect)

        if click[0] == 1 and action is not None:
            if action == 'play':
                wager()
            elif action == 'quit':
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(screen, ic, (x,y,w,h))
        text1 = pygame.font.Font('freesansbold.ttf',25)
        TextSurf, TextRect = text_objects(msg,text1)
        TextRect.center = (((x+100/2)), (450+(50/2)))
        screen.blit(TextSurf, TextRect)


def wager():
    wager = True
    while wager:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            screen.blit(bgImg,(0,0))
            font = pygame.font.SysFont('gargi',30)
            text = font.render('Pot = $'+str(pot), True, blue)
            screen.blit(text, (325,325))
            font = pygame.font.SysFont('gargi',21)
            text = font.render(' What would you like to wager?',True,white)
            screen.blit(text,(250,375))

            bets('$5',300,425,55,45,green,brightRed,'5')
            bets('$10',375,425,55,45,green,brightRed,'10')
            bets('$25',450,425,55,45,green,brightRed,'25')

            pygame.display.flip()


def bets(msg,x,y,w,h,ic,ac,action=None):
    global bet
    global pot
    bet = 0
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x,y,w,h))
        font = pygame.font.SysFont('ubuntu',25)
        text = font.render(msg, True, black)
        screen.blit(text,(x+5,y+7))
        if click[0] == 1 and action is not None:
            if action == '5':
                bet +=5
                game()

            elif action == '10':
                if pot > 9:
                    bet +=10
                    game()
                else:
                    font = pygame.font.SysFont('ubuntu',25,bold=True)
                    text = font.render('Insufficient Funds!', True, red,black)
                    screen.blit(text,(300,500))
                    pygame.display.flip()
                    time.sleep(2)

            elif action == '25':
                if pot > 24:
                    bet +=25
                    game()
                else:
                    font = pygame.font.SysFont('ubuntu',25,bold=True)
                    text = font.render('Maybe you should hit the bank', True, red,black)
                    screen.blit(text,(220,500))
                    pygame.display.flip()
                    time.sleep(2)

    else:
        pygame.draw.rect(screen, ic, (x,y,w,h))
        font = pygame.font.SysFont('gargi',25,bold=True)
        text = font.render(msg, True, black)
        screen.blit(text,(x,y+7))


def playerStart(cards,pValues,x,y):
    for i in range(2):
        loadCard = pygame.image.load(str(path)+'cards/'+str(cards[i]))
        loadCard = pygame.transform.scale(loadCard,(120,180))
        screen.blit(loadCard,(x,y))
        x+=50
        pValues.append(cards[i][-5])
        change(pHand,dHand,pValues,dValues)


def dealerStart(cards,dValues,x,y):
    cardBack = pygame.image.load((str(path)+'cards/cardback.png'))
    cardBack = pygame.transform.scale(cardBack,(120,180))
    loadCard = pygame.image.load(str(path)+'cards/'+str(cards[2]))
    loadCard = pygame.transform.scale(loadCard,(120,180))
    screen.blit(cardBack,(x,y))
    x-=50
    screen.blit(loadCard,(x,y))
    for i in range(2,4):
        dValues.append(cards[i][-5])
        change(pHand,dHand,pValues,dValues)


def change(pHand,dHand,pValues,dValues):
    for i in pValues:
        if i == '0' or i == 'j' or i == 'q' or i == 'k':
            pValues.remove(i)
            pHand.append(int(10))

        elif i == '1':
            if sum(pHand) < 11:
                    pValues.remove(i)
                    pHand.append(int(11))
            else:
                    pValues.remove(i)
                    pHand.append(int(1))
        else:
            pValues.remove(i)
            pHand.append(int(i))

    for i in dValues:
        if i == '0' or i == 'j' or i == 'q' or i == 'k':
            dValues.remove(i)
            dHand.append(int(10))

        elif i == '1':
            if sum(dHand) < 11:
                dValues.remove(i)
                dHand.append(int(11))
            else:
                dValues.remove(i)
                dHand.append(int(1))
        else:
            dValues.remove(i)
            dHand.append(int(i))

def hosButtons(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x,y,w,h))
        font = pygame.font.SysFont('ubuntu',25)
        text = font.render(msg, True, black)
        screen.blit(text,(x+15,y+7))

        if click[0] == 1 and action is not None:
            if action == 'hit':
                hit(pHand,py)
            elif action == 'stand':
                stand(pHand,dHand,dDraw,dx,dy)

    else:
        pygame.draw.rect(screen, ic, (x,y,w,h))
        font = pygame.font.SysFont('gargi',25,bold=True)
        text = font.render(msg, True, black)
        screen.blit(text,(x+15,y+7))


def hit(pHand,py):
    global pDraw,px
    ph = pygame.image.load(str(path)+'cards/'+str(cards[pDraw])).convert()
    ph = pygame.transform.scale(ph,(120,180))
    screen.blit(ph,(px,py))
    pValues.append(cards[pDraw][-5])
    change(pHand,dHand,pValues,dValues)
    pDraw+=1
    px+=50
    pygame.display.flip()
    if sum(dHand) == 21:
        lose(bet,pHand,dHand)
    if sum(pHand) == 21:
        win(bet,pHand,dHand)
    elif sum(pHand) > 21:
        lose(bet,pHand,dHand)


def stand(pHand,dHand,dDraw,dx,dy):
    if sum(pHand) == 21 and sum(dHand) == 21:
        lose(bet,pHand,dHand)
    elif sum(pHand) == 21:
        win(bet,pHand,dHand)
    elif sum(dHand) == 21:
        lose(bet,pHand,dHand)
    while sum(dHand) <=16:
        dh = pygame.image.load(str(path)+'cards/'+str(cards[dDraw])).convert()
        dh = pygame.transform.scale(dh,(120,180))
        screen.blit(dh,(dx,dy))
        time.sleep(1)
        dValues.append(cards[dDraw][-5])
        change(pHand,dHand,pValues,dValues)
        dDraw+=1
        dx-=50
        pygame.display.flip()
        time.sleep(1.5)
    if sum(dHand) > 21:
        win(bet,pHand,dHand)
    if sum(dHand) > sum(pHand):
        lose(bet,pHand,dHand)
    if sum(dHand) == sum(pHand):
        lose(bet,pHand,dHand)
    if sum(dHand) < sum(pHand):
        win(bet,pHand,dHand)


def win(bet,pHand,dHand):
    global pot
    pot+=bet

    cardBack = pygame.image.load(str(path)+'cards/'+str(cards[3]))
    cardBack = pygame.transform.scale(cardBack,(120,180))
    screen.blit(cardBack,(650,200))

    if sum(pHand) == 21:
        font = pygame.font.SysFont('ubuntu',65,bold=True)
        text = font.render('BlackJack!', True, brightGreen)
        screen.blit(text, (50,220))

    elif sum(dHand) > 21:
        font = pygame.font.SysFont('ubuntu',65,bold=True)
        text = font.render('Dealer Bust!', True, brightBlue)
        screen.blit(text, (50,220))

    else:
        font = pygame.font.SysFont('freesansbold.ttf',40)
        text = font.render('Win! Player: '+str(sum(pHand))+' Dealer: '+str(sum(dHand)), True, brightBlue)
        screen.blit(text, (50,250))

    pygame.display.flip()
    time.sleep(3)
    wager()


def lose(bet,pHand,dHand):
    global pot
    pot-=bet

    cardBack = pygame.image.load(str(path)+'cards/'+str(cards[3]))
    cardBack = pygame.transform.scale(cardBack,(120,180))
    screen.blit(cardBack,(650,200))

    while pot > 4:
        if sum(pHand) > 21:
            font = pygame.font.SysFont('ubuntu',65,bold=True)
            text = font.render('Bust!', True, red)
            screen.blit(text, (50,220))

        elif sum(dHand) > sum(pHand):
            font = pygame.font.SysFont('freesansbold.ttf',40)
            text = font.render('Lose! Player: '+str(sum(pHand))+' Dealer: '+str(sum(dHand)), True, red)
            screen.blit(text, (50,250))

        elif sum(pHand) == sum(dHand):
            font = pygame.font.SysFont('ubuntu',65,bold=True)
            text = font.render('Push', True, red)
            screen.blit(text, (50,220))
            pot+=bet

        pygame.display.flip()
        time.sleep(3)
        wager()

    else:
        time.sleep(2)
        screen.fill(black)
        font = pygame.font.SysFont('freesansbold.ttf',70)
        text = font.render("Pot = $"+str(pot),True, red)
        screen.blit(text,(200,150))
        text = font.render("Insufficient funds <('_')>",True,red)
        screen.blit(text,(100,300))
        pygame.display.flip()
        time.sleep(4)
        pot = 100
        intro()


def game():
    global pDraw,px
    pHand.clear()
    dHand.clear()
    screen.blit(bgImg,(0,0))
    random.shuffle(cards)
    playerStart(cards,pValues,25,400)
    dealerStart(cards,dValues,650,20)
    px = 125

    run = False
    while not run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()

            font = pygame.font.SysFont('ubuntu',25,bold=True)
            text = font.render('Press "f" to toggle fullscreen',True,black)
            screen.blit(text,(0,0))

            hosButtons('Hit',550,500,75,50,green,white,'hit')
            hosButtons('Stand',650,500,100,50,red,white,'stand')

        pygame.display.flip()
        clock.tick(30)


intro()
pygame.quit()
quit()
