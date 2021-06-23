import pygame
import time
import random
import threading
pygame.font.init()
class grid:

    def __init__(self,row,col,width,height,window):
        self.row= row
        self.col = col
        self.width = width
        self.height = height
        self.win = window
        self.cube =[[cube(i,j,width,height,window,0)for j in range(col)] for i in range(row)]
        self.timer = 0
        self.gap = self.width //col
    def show(self):
        for i in range(self.timer):
            for j in range(self.col):
                self.cube[i][j].draw()
    def attack(self,val,col):
        location = 0
        for i in range(self.row-1,0,-1):
            if self.cube[i][col].value !=0:
                location = i
                break
        if(self.cube[location][col].value == val):
            print(location,col,val)
            self.detect(location,col,val)
    def detect(self,x,y,v):
        if(y>self.width//10):
            return 
        self.cube[x][y].clean()
        if self.cube[x+1][y].value == v :
            self.detect(x+1,y,v)
        if y+1 <10:
            if self.cube[x][y+1].value == v :
                self.detect(x,y+1,v)
        if self.cube[x-1][y].value == v:
            self.detect(x-1,y,v)
        if self.cube[x][y-1].value == v and y-1>=0:
            self.detect(x,y-1,v)
    def shoot(self,angle,x,y,x_end,y_end,v):
        x_step = int((x_end-x)/(15))
        y_step = int((y_end-y)/(15))
        x_start = x
        y_start = y

        for i in range(15):
            y_start += y_step
            x_start += x_step
            ccol = int(x_start//self.gap)
            rrow = int(y_start//self.gap)
            print(i,rrow,ccol)
            if rrow <self.row:
                if self.cube[rrow][ccol].value==v:
                    self.detect(rrow,ccol,v)
                    break
            


    def time_update(self,t):
        #time.sleep()
        if self.timer<9 and t%10000==0:
            self.timer  +=1
            self.cube_change()
        elif self.timer ==9 and t%10000==0:
            self.cube_change()
        # print(self.timer)
    def cube_change(self):
        for i in range(self.timer,0,-1):
            for j in range(self.col):
                self.cube[i][j].value = self.cube[i-1][j].value
        for j in range(self.col):
            self.cube[0][j].value = random.randint(1,5)
        self.show()
        pygame.display.update()

class bubble:
    def __init__(self,row,col,value,width,height,win):
        self.value = value
        self.width = width
        self.height = height
        self.win = win
        self.col = col
        self.gap = width /11
        self.row = row
        self.x = (col+0.5)*self.gap
        self.y = (row+0.5)*self.gap
        self.x_end = 0
        self.y_end = 0
    def draw_line(self,visible):
        
        if visible:
            if self.angle ==0:
                pygame.draw.line(self.win,(0,0,0),((self.col+0.5)*self.gap,self.row*self.gap),((self.col+0.5)*self.gap,0),3)
                self.x_end = (self.col+0.5)*self.gap
                self.y_end = 0
            else:
                pygame.draw.line(self.win,(0,0,0),((self.col+0.5)*self.gap,self.row*self.gap),((self.col+0.5)*self.gap+self.angle*110,0),3)
                self.slope_1 =  (self.row*self.gap/self.angle*110)
                self.x_end = (self.col+0.5)*self.gap+self.angle*110
                self.y_end = 0
                if(self.col+0.5)*self.gap+self.angle*110>self.width:
                    #pygame.draw.line(self.win,(0,0,0),((self.col+0.5)*self.gap,self.row*self.gap),(self.width,((self.col+0.5)*self.gap+angle*110)*(2/abs(angle)+2)),3)
                    pygame.draw.line(self.win,(0,0,0),(self.width+2*110,self.row*self.gap),(self.width+220-self.angle*110,0),3)
                    self.slope_2 = -(self.row*self.gap/self.angle*110)
                    self.x = self.width
                    self.y = (self.row+0.5)*self.gap - (self.row+0.5)*(1-self.width/2)/self.angle*110
                    self.x_end = self.width+220-self.angle*110
                    self.y_end = 0

                elif (self.col+0.5)*self.gap+self.angle*110<0:
                    #pygame.draw.line(self.win,(0,0,0),((self.col+0.5)*self.gap,self.row*self.gap),(0,((self.col+0.5)*self.gap+angle*110)*(2/abs(angle)+2)),3)
                    pygame.draw.line(self.win,(0,0,0),(0-2*110,self.row*self.gap),(0-220-self.angle*110,0),3)
                    self.slope_2 = -(self.row*self.gap/self.angle*110)
                    self.x = 0
                    self.y = (self.row+0.5)*self.gap - (self.row+0.5)*(1-self.width/2)/self.angle*110
                    self.x_end = 0-220-self.angle*110
                    self.y_end = 0
                

    def line_clean(self):
        if self.angle == 0:
            pygame.draw.line(self.win,(255,255,255),((self.col+0.5)*self.gap,self.row*self.gap),((self.col+0.5)*self.gap,0),3)
        else:
            pygame.draw.line(self.win,(255,255,255),((self.col+0.5)*self.gap,self.row*self.gap),((self.col+0.5)*self.gap+self.angle*110,0),3)
            if (self.col+0.5)*self.gap+self.angle*110>self.width:
                #pygame.draw.line(self.win,(255,255,255),((self.col+0.5)*self.gap,self.row*self.gap),(self.width,((self.col+0.5)*self.gap+self.angle*110)*(2/self.angle+2)),3)
                pygame.draw.line(self.win,(255,255,255),(self.width+2*110,self.row*self.gap),(self.width+220-self.angle*110,0),3)
            elif (self.col+0.5)*self.gap+self.angle*110<0:
                #pygame.draw.line(self.win,(255,255,255),((self.col+0.5)*self.gap,self.row*self.gap),(0,((self.col+0.5)*self.gap+self.angle*110)*(2/abs(self.angle)+2)),3)
                pygame.draw.line(self.win,(255,255,255),(0-2*110,self.row*self.gap),(0-220-self.angle*110,0),3)
            
    def draw(self):
        r = self.col*self.gap
        
        if self.value == -1:
            pygame.draw.rect(self.win,(255,255,255),(r,self.row*self.gap,self.gap,self.gap),0)
        else:
            pygame.draw.rect(self.win,(self.value*25,self.value*50%255,self.value*100%255),(r,self.row*self.gap,self.gap,self.gap),0)
    def move(self,direction):
        if direction == "right":
            r = self.col*self.gap
            pygame.draw.rect(self.win,(255,255,255),(r,540,self.gap,self.gap),0)
            self.set(1)
            self.draw()
        elif direction =="left":
            r = self.col*self.gap
            pygame.draw.rect(self.win,(255,255,255),(r,540,self.gap,self.gap),0)
            self.set(-1)
            self.draw()
    def draw_change(self):
        self.value = (self.value+1)%5+1
        
        self.draw()
    def set(self,val):
        if(self.col+val<10 and self.col+val>=0):
             self.col+=val
    def move_up(self,t):
        if t%1000 == 0 and self.row >=0 and self.value!=-1 and self.col>0 and self.col<10:  
            self.clean()

            print(self.x,self.y)
            self.col +=1
            self.row -=3 
            self.draw()
        if self.row <0 or self.col <0 or  self.col>=10:
            self.reset()
    def reset(self):
        self.row =13
        self.col = 0
        self.value =-1
    def clean(self):
        x = self.col*self.gap
        y = self.row*self.gap
        pygame.draw.rect(self.win,(255,255,255),(x,y,self.gap,self.gap),0)

    def attack(self):
        return self.value,self.col
    def set_angle(self,angle):
        self.angle = angle




class cube:
    def __init__(self,row,col,width,height,win,val):
        self.col = col
        self.row = row
        self.height = height
        self.width = width
        self.win = win
        self.value = val
        self.gap = width/11


    def draw(self):
        x = self.col*self.gap
        y = self.row*self.gap
        if self.value !=0:
            '''
            if self.value == 1:
                pygame.draw.rect(self.win,(255,0,0),(x,y,self.gap,self.gap),0)
            elif self.value == 2:
                pygame.draw.rect(self.win,(0,255,0),(x,y,self.gap,self.gap),0)
            elif self.value ==3:
                pygame.draw.rect(self.win,(0,0,255),(x,y,self.gap,self.gap),0)'''
            pygame.draw.rect(self.win,(self.value*25,self.value*50%255,self.value*100%255),(x,y,self.gap,self.gap),0)
        else:
            pygame.draw.rect(self.win,(255,255,255),(x,y,self.gap,self.gap),0)
    def clean(self):
        x = self.col*self.gap
        y = self.row*self.gap
        self.value = 0
        pygame.draw.rect(self.win,(255,255,255),(x,y,self.gap,self.gap),0)
    def set(self,val):
        self.value = val
        self.draw()
    




def main():
    win = pygame.display.set_mode((440,600))
    win.fill((255,255,255))
    width = 440
    height = 600
    pygame.display.set_caption("Bubble")
    board = grid(13,11,440,600,win)

    page = 1
    fnt_80 = pygame.font.SysFont("comicsans",80)
    #win.blit(text_title,(width/2-30,410))
    run =True
    time  =0
    angle = 0
    bullet_lst = [bubble(13,0,-1,440,600,win) for i in range(5)]
    bub = bubble(14,5,1,440,600,win)
    bub.set_angle(angle)
    bub.draw_line(True)
    
    bub.draw()
    while run:
        board.time_update(time)
        board.show()
        for i in bullet_lst:
            if i.row<10:
                if i.value == board.cube[i.row][i.col].value:
                    val,col = i.attack()
                    board.attack(val,col)
                    i.reset()
                elif i.value !=board.cube[i.row][i.col].value and i.value!=-1 and board.cube[i.row][i.col].value!=0:
                    i.reset()
            #i.move_up(time)
            i.draw()
        
        bub.draw()
        time+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and page ==1:
                if event.key == pygame.K_RIGHT:
                    bub.line_clean()
                    #bub.move("right")
                    angle +=1
                    bub.set_angle(angle)
                    bub.draw_line(True)
                    
                if event.key == pygame.K_LEFT:
                    bub.line_clean()
                    angle -=1
                    bub.set_angle(angle)
                    bub.draw_line(True)
                    #bub.move("left")
                if event.key == pygame.K_SPACE:
                    bub.draw_change()
                if event.key == pygame.K_RETURN:
                    print(bub.angle,bub.x,bub.y,bub.x_end,bub.y_end,bub.value)
                    board.shoot(bub.angle,bub.x,bub.y,bub.x_end,bub.y_end,bub.value)
                    print("shoot")

                    
                    
                    '''for i in range(5):
                        if bullet_lst[i].value ==-1:
                            bullet_lst[i].value = bub.value
                            bullet_lst[i].col = bub.col
                            bullet_lst[i].angle = bub.angle
                            break'''
                    
                    



        pygame.display.update()



main()
pygame.quit()
    