import math
import random
import pygame
import random
import tkinter as tk
from tkinter import messagebox
import sys
from time import sleep

pygame.init()

width = 500   #화면의 가로길이
height = 500   #화면의 세로길이 
 
cols = 25   #열의 개수
rows = 20   #행의 개수


class cube():
    rows = 20
    w = 500
    def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny # "L", "R", "U", "D"
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos  = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) #위치 바꾸기 
            

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows  # 큐브의 가로, 세로길이 
        i = self.pos[0]  # 현재 열 
        j = self.pos[1]  # 현재 행 
        
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2)) #어디에 그릴지 계산
        if eyes:  # 눈 그리기 
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        


class snake():
    body = []
    turns = {}
    
    def __init__(self, color, pos):  # 사용자가 입력하여 객체 생성 
        #pos is given as coordinates on the grid ex (1,5) 
        self.color = color
        self.head = cube(pos) # snake의 머리 
        self.body.append(self.head) # body 리스트에 head 추가 
        self.dirnx = 0  #snake가 움직이는 방향 제시 
        self.dirny = 1
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # 창을 닫으면
                pygame.quit()
                sys.exit(0)
            keys = pygame.key.get_pressed() # 어떤 키를 누르는지 확인
            
            for key in keys:
                if keys[pygame.K_LEFT]: # 좌키를 누르면 
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_RIGHT]:  # 우키를 누르면  
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_UP]: # 상키를 누르면 
                    self.dirny = -1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
                elif keys[pygame.K_DOWN]:   # 하키를 누르면 
                    self.dirny = 1
                    self.dirnx = 0
                    self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        
        for i, c in enumerate(self.body):
            p = c.pos[:] # 큐브의 좌표 저장함 
            if p in self.turns:  # if turning the cube
                turn = self.turns[p] # 돌아야할 방향 get
                c.move(turn[0], turn[1]) # 그 방향으로 큐브를 move
                if i == len(self.body)-1: # body의 마지막 큐브라면 
                    self.turns.pop(p)  # dict에서 turn 삭제 
            else: # if not turning the cube
                c.move(c.dirnx,c.dirny) # 현재 방향으로 움직임 
        
        
    def reset(self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0: # 어떤 쪽에 큐브를 추가할지  
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx  # 큐브의 방향 == 뱀의 방향 
        self.body[-1].dirny = dy
    
    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:  # 첫번째 큐브라면 
                c.draw(surface, True) # 눈을 그려라 
            else: #첫번째 큐브가 아니면 
                c.draw(surface)  # 그냥 큐브만 그려라

def redrawWindow():
    global win
    win.fill((0,0,0)) #화면을 블랙으로 채움 
    drawGrid(width, rows, win) #격자선 그림 
    s.draw(win)
    snack.draw(win)
    draw_score()
    if gameover == 1:
        draw_gameover()
        pygame.display.update()
        sleep(1)
    else:
        pygame.display.update() #화면을 업데이트



def drawGrid(w, rows, surface):
    sizeBtwn = w // rows # 줄 간격 계산 

    x = 0  # 현재 x값을 기록 
    y = 0  # 현재 y값을 기록 
    for l in range(rows):  #하나의 가로선, 하나의 세로선 반복해서 그림 
        x = x + sizeBtwn
        y = y +sizeBtwn
        pygame.draw.line(surface, (255,255,255), (x, 0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0, y),(w,y))
    


def randomSnack(rows, item):
    positions = item.body  # 뱀의 모든 위치 가져옴 
    while True:
        x = random.randrange(1,rows-1)
        y = random.randrange(1,rows-1)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
               continue  # 뱀이 스낵을 먹었는지 확인 
        else:
               break
    return (x,y)


def draw_score():
    YELLOW = (255, 255, 0)
    small_font = pygame.font.SysFont(None, 36)
    score_image = small_font.render('Point {}'.format(len(s.body)), True, YELLOW)
    win.blit(score_image, (15, 15)) # blit() 통해 게임판에 출력
    
def draw_gameover():
    RED = (255, 0, 0)
    large_font = pygame.font.SysFont(None, 72)
    gameover_image = large_font.render('Game Over', True, RED)
    win.blit(gameover_image, (width // 2 - gameover_image.get_width() // 2, height // 2 - gameover_image.get_height() // 2))
    

    
def main():
    global s, snack, win, gameover
    win = pygame.display.set_mode((width,height))  #화면에 screen object 생성  
    s = snake((255,0,0), (10,10))  #화면에 snake object 생성 
    snack = cube(randomSnack(rows,s), color=(0,255,0))
    gameover = 0
    flag = True
    clock = pygame.time.Clock() #clock object 생성
    
    while flag:  #main 루프 시작 
        pygame.time.delay(50)  #게임의 프레임속도 제어 
        clock.tick(10)  #지정된 프레임 값 넘지 않도록 딜레이
        s.move()
        headPos = s.head.pos
        if headPos[0] >= 20 or headPos[0] < 0 or headPos[1] >= 20 or headPos[1] < 0:
            # 벽에 충돌하면 
            print("Score:", len(s.body))
            gameover = 1
            s.reset((10, 10))
            
        if s.body[0].pos == snack.pos:  # 머리가 스낵 먹으면 
            s.addCube()  # 뱀에 큐브추가 
            snack = cube(randomSnack(rows,s), color=(0,255,0))  # 새로운 스낵 생성 
            
        for x in range(len(s.body)): #자기 몸과 부딪히면 
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print("Score:", len(s.body))
                gameover = 1
                s.reset((10,10))
                break
        redrawWindow() #화면 업데이트 
        gameover = 0
        

main()