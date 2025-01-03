import sys
import time
from PyQt5 import QtGui
from PyQt5.QtCore import QRect,Qt
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

class Mario(QWidget):
    MARIO_X =80
    MARIO_Y =580
    MARIO_ACTION_X = 80
    MARIO_ACTION_Y =580
    MARIO_ACTION = 0
    MARIO_LEFT_RIGHT = "marioR"
    MARIO_IS_LIVE = True
    MARIO_IS_RUN = False
    MARIO_LIVE = 5

    MARIO_SPEED_X = 10
    MARIO_SPEED_Y = 10
    MARIO_JUMP_MAX_HEIGHT = 350
    MARIO_JUMP_HEIGHT = 0
    MARIO_STATE = 0

    TORTOISE_ACTION_X = MARIO_X +700
    TORTOISE_ACTION_Y = MARIO_Y - 300
    TORTOISE_LEFT_RIGHT = "tortoiseR"
    TORTOISE_ACTION = 0

    BADFLOWER_ACTION_X = MARIO_X + 800+5
    BADFLOWER_ACTION_Y = MARIO_Y - 10
    BADFLOWER_HEIGHT = 10
    BADFLOWER_ACTION = 0

    FLOWER_ACTION_X = MARIO_X + 200
    FLOWER_ACTION_Y = MARIO_Y - 200-10
    FLOWER_HEIGHT = 10
    FLOWER_ACTION = 0

    MONSTER_ACTION_X = MARIO_X +100
    MONSTER_ACTION_Y = MARIO_Y
    MONSTER_LEFT_RIGHT = "monsterR"
    MONSTER_ACTION = 0

    ROCKT_ACTION = 200

    MONEY1_DISPLAY = True
    MONEY2_DISPLAY = True
    MONEY3_DISPLAY = True

    KUNKUN_DISPLAY = False

    DIMONDS_FLAG = 0
    HINT_FLAG = 0

    JUMP_FLAG = False
    GAME_SCORE = 0
    GAMEOVER = False
    GAMEWIN = False
    HUOJIAN = False
    ROCK_LAUNCH = False

    def __init__(self):
        super(Mario,self).__init__()
        self.setWindowTitle("超级马里奥")
        self.resize(1500,728)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(30)  # 每30毫秒触发一次移动更新

    def update_position(self):
        if self.MARIO_IS_RUN:
            if self.MARIO_LEFT_RIGHT == "marioR":
                self.MARIO_ACTION_X += self.MARIO_SPEED_X
                if self.MARIO_ACTION_X > 1300 :
                    self.MARIO_ACTION_X = 1300
            elif self.MARIO_LEFT_RIGHT == "marioL":
                self.MARIO_ACTION_X -= self.MARIO_SPEED_X
                if self.MARIO_ACTION_X < 51 :
                    self.MARIO_ACTION_X = 51

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        background_rect = QRect(0,0,1500,728)
        mario_rect = QRect(self.MARIO_ACTION_X, self.MARIO_ACTION_Y, 100, 100)
        if self.GAMEOVER == True:
            over_img = QImage("images/over.png")
            painter.drawImage(background_rect,over_img)
            return
        if self.GAMEWIN == True and self.ROCK_LAUNCH== True :
            win_img = QImage("images/end.png")
            painter.drawImage(background_rect,win_img)
            return
        background_img = QImage("images/8d7209fbaf013c51f98f7e0f2c3a1e09.jpg")
        painter.drawImage(background_rect,background_img)
        self.mario(painter)
        self.draw_Obstacle(painter)
        self.draw_Score(painter)
        self.draw_tortoise(painter)
        self.draw_badflower(painter)
        self.draw_flower(painter)
        self.draw_monster(painter)
        self.my_intersects()
        #self.draw_rocket(painter)
        self.update()
        self.draw_rocket_launch(painter)
        self.draw_Obstacle(painter)
        self.hit_wall(mario_rect,self.MARIO_X + 200,self.MARIO_Y - 200,100,100 )
        self.hit_diamonds(mario_rect,self.MARIO_X + 600,self.MARIO_Y - 200,100,100)
        self.hit_diamods8(mario_rect,self.MARIO_X + 1100,self.MARIO_Y - 300,100,100)
        self.hit_diamods9(mario_rect,self.MARIO_X + 600,self.MARIO_Y - 300,100,100)
        self.draw_kun_(painter)

    def keyPressEvent(self, QKeyEvent):
        key = QKeyEvent.key()
        if key == Qt.Key_Right:
                self.MARIO_IS_RUN = True
                self.MARIO_LEFT_RIGHT = "marioR"
        if key == Qt.Key_Left:
                self.MARIO_IS_RUN = True
                self.MARIO_LEFT_RIGHT = "marioL"
        if key == Qt.Key_Up:
            self.MARIO_IS_RUN = True
            if self.MARIO_STATE == 0 or self.MARIO_STATE == 3:
                self.MARIO_JUMP_HEIGHT = 350
                self.MARIO_STATE =1
                #self.JUMP_FLAG = True

    def keyReleaseEvent(self, QKeyEvent):
         key = QKeyEvent.key()
         if key == Qt.Key_Right or key == Qt.Key_Left or key == Qt.Key_Up:
             self.MARIO_IS_RUN = False

    def my_intersects(self):
        mario_rect = QRect(self.MARIO_ACTION_X, self.MARIO_ACTION_Y, 100, 100)
        money1_rect = QRect(self.MARIO_X + 400, self.MARIO_Y, 100, 100)
        money2_rect = QRect(self.MARIO_X + 600, self.MARIO_Y, 100, 100)
        money3_rect = QRect(self.MARIO_X + 1000, self.MARIO_Y, 100, 100)
        badf_rect = QRect(self.MARIO_X + 800, self.MARIO_Y, 100, self.BADFLOWER_HEIGHT+100)
        badm_rect = QRect(self.MONSTER_ACTION_X, self.MONSTER_ACTION_Y, 100, 100)
        badt_rect = QRect(self.TORTOISE_ACTION_X,self.TORTOISE_ACTION_Y,100,100)
        tower_rect = QRect(self.MARIO_X + 1100, self.MARIO_Y - 500, 100, 100)
        abnormalwall_rect = QRect(self.MARIO_X + 200, self.MARIO_Y - 200, 100, 100)
        if (mario_rect.intersected(money1_rect)):
            if(self.MONEY1_DISPLAY):
                self.GAME_SCORE += 10
            self.MONEY1_DISPLAY = False
        if (mario_rect.intersected(money2_rect)):
            if (self.MONEY2_DISPLAY):
                self.GAME_SCORE += 10
            self.MONEY2_DISPLAY = False
        if (mario_rect.intersected(money3_rect)):
            if (self.MONEY3_DISPLAY):
                self.GAME_SCORE += 10
            self.MONEY3_DISPLAY = False
        if (mario_rect.intersected(badf_rect)):
            self.hit_mario()
        if (mario_rect.intersected(badm_rect)):
            self.hit_mario()
        if (mario_rect.intersected(badt_rect)):
            self.hit_mario()
        if (mario_rect.intersected(tower_rect)):
            self.KUNKUN_DISPLAY = True
            self.HUOJIAN = True
            self.GAMEWIN = True

    def hit_wall(self,mario_rect,x,y,w,h):
        wall = QRect(x,y,w,h)
        if mario_rect.intersected(wall) :
            self.HINT_FLAG = 1
            if self.JUMP_FLAG == False:
                if self.MARIO_ACTION_Y >= y + 20:
                    #self.MARIO_ACTION_Y =0# self.MARIO_Y
                    self.MARIO_IS_RUN = False
                    self.MARIO_STATE = 2
                elif self.MARIO_ACTION_Y +60<= y - 20:
                #self.MARIO_ACTION_Y =0# self.MARIO_Y
                    self.MARIO_STATE = 0
                    self.JUMP_FLAG = True
                else:
                    if self.MARIO_LEFT_RIGHT=="marioL" :
                        self.MARIO_ACTION_X += 30
                    else:
                        self.MARIO_ACTION_X -= 30
        elif self.HINT_FLAG == 1 and not mario_rect.intersected(wall):
            if self.MARIO_STATE != 1  :#and self.HINT_FLAG == 1: #and QKeyEvent.key() != Qt.Key_Up:
                if self.MARIO_ACTION_Y < self.MARIO_Y:
                    self.MARIO_STATE = 2
            self.JUMP_FLAG = False
            self.HINT_FLAG = 0
             #self.MARIO_JUMP_HEIGHT = 1000
    def hit_diamods8(self, mario_rect, x, y, w, h):
        wall = QRect(x, y, w, h)
        if mario_rect.intersected(wall):
            self.HINT_FLAG =8
            if self.JUMP_FLAG == False:
                if self.MARIO_ACTION_Y >= y + 20:
                    # self.MARIO_ACTION_Y =0# self.MARIO_Y
                    self.MARIO_IS_RUN = False
                    self.MARIO_STATE = 2
                elif self.MARIO_ACTION_Y + 60 <= y - 20:
                    # self.MARIO_ACTION_Y =0# self.MARIO_Y
                    self.MARIO_STATE = 0
                    self.JUMP_FLAG = True
                else:
                    if self.MARIO_LEFT_RIGHT == "marioL":
                        self.MARIO_ACTION_X += 30
                    else:
                        self.MARIO_ACTION_X -= 30
        elif self.HINT_FLAG == 8 and not mario_rect.intersected(wall):
            if self.MARIO_STATE != 1:  # and self.HINT_FLAG == 1: #and QKeyEvent.key() != Qt.Key_Up:
                if self.MARIO_ACTION_Y < self.MARIO_Y:
                    self.MARIO_STATE = 2
            self.JUMP_FLAG = False
            self.HINT_FLAG = 0
            # self.MARIO_JUMP_HEIGHT = 1000
    def hit_diamods9(self, mario_rect, x, y, w, h):
        wall = QRect(x, y, w, h)
        if mario_rect.intersected(wall):
            self.HINT_FLAG =9
            if self.JUMP_FLAG == False:
                if self.MARIO_ACTION_Y >= y + 20:
                    # self.MARIO_ACTION_Y =0# self.MARIO_Y
                    self.MARIO_IS_RUN = False
                    self.MARIO_STATE = 2
                elif self.MARIO_ACTION_Y + 60 <= y - 20:
                    # self.MARIO_ACTION_Y =0# self.MARIO_Y
                    self.MARIO_STATE = 0
                    self.JUMP_FLAG = True
                else:
                    if self.MARIO_LEFT_RIGHT == "marioL":
                        self.MARIO_ACTION_X += 30
                    else:
                        self.MARIO_ACTION_X -= 30
        elif self.HINT_FLAG == 9 and not mario_rect.intersected(wall):
            if self.MARIO_STATE != 1:  # and self.HINT_FLAG == 1: #and QKeyEvent.key() != Qt.Key_Up:
                if self.MARIO_ACTION_Y < self.MARIO_Y:
                    self.MARIO_STATE = 2
            self.JUMP_FLAG = False
            self.HINT_FLAG = 0
    def hit_diamonds(self,mario_rect,x,y,w,h):
        for i in range(6):
            diamonds=QRect(x + i * 100,y,w,h)
            if mario_rect.intersected(diamonds):
                if self.MARIO_ACTION_X <= self.MARIO_ACTION + 750:
                    self.MARIO_ACTION_X = 750
                if self.MARIO_ACTION_X >= self.MARIO_ACTION + 1075:
                    self.MARIO_ACTION_X = 1075
                self.HINT_FLAG = i+2
                if self.JUMP_FLAG == False:
                    if self.MARIO_ACTION_Y >= y + 20:
                        # self.MARIO_ACTION_Y =0# self.MARIO_Y
                        self.MARIO_IS_RUN = False
                        self.MARIO_STATE = 2
                    elif self.MARIO_ACTION_Y + 60 <= y - 20:
                        # self.MARIO_ACTION_Y =0# self.MARIO_Y
                        self.MARIO_STATE = 0
                        self.JUMP_FLAG = True
                    else:
                        if self.MARIO_LEFT_RIGHT == "marioL":
                            self.MARIO_ACTION_X += 30
                        else:
                            self.MARIO_ACTION_X -= 30
            elif self.HINT_FLAG ==(i+2)  and not mario_rect.intersected(diamonds):
                if self.MARIO_STATE != 1 :  # and self.HINT_FLAG == 1: #and QKeyEvent.key() != Qt.Key_Up:
                    if self.MARIO_ACTION_Y < self.MARIO_Y:
                        self.MARIO_STATE = 2
                self.JUMP_FLAG = False
                self.HINT_FLAG = 0

    def hit_mario(self):
        if(self.MARIO_IS_LIVE):
            self.MARIO_LIVE -= 1
            self.MARIO_ACTION_X = self.MARIO_X
            self.MARIO_ACTION_Y = self.MARIO_Y
        if(self.MARIO_LIVE == 0):
            self.GAMEOVER = True

    def draw_badflower(self,painter):
        badflower_rect = QRect(self.BADFLOWER_ACTION_X,self.BADFLOWER_ACTION_Y,90,self.BADFLOWER_HEIGHT)
        badflower_img = QImage("images/badflower/"+str(self.BADFLOWER_ACTION)+".png")
        painter.drawImage(badflower_rect,badflower_img)
        self.BADFLOWER_ACTION += 1
        if(self.BADFLOWER_ACTION <= 16):
            self.BADFLOWER_ACTION_Y -= 3
            self.BADFLOWER_HEIGHT += 3
        elif(self.BADFLOWER_ACTION <= 35):
            self.BADFLOWER_ACTION_Y += 3
            self.BADFLOWER_HEIGHT -= 3
        else:
            self.BADFLOWER_ACTION_Y = self.MARIO_Y -10
            self.BADFLOWER_HEIGHT = 10
            self.BADFLOWER_ACTION = 0

    def draw_flower(self,painter):
        flower_rect = QRect(self.FLOWER_ACTION_X,self.FLOWER_ACTION_Y,90,self.FLOWER_HEIGHT)
        flower_img = QImage("images/flower/"+str(self.FLOWER_ACTION)+".png")
        painter.drawImage(flower_rect,flower_img)
        self.FLOWER_ACTION += 1
        if (self.FLOWER_ACTION <=4):
            self.FLOWER_ACTION_Y -=10
            self.FLOWER_HEIGHT +=10
        else:
            self.FLOWER_ACTION=4

    def draw_rocket(self,painter):
        if self.HUOJIAN == False:
            rocket_rect = QRect(1350,200,100,600)
            rocket_img = QImage("images/hj-removebg.png")
            painter.drawImage(rocket_rect,rocket_img)

        # if flag_img.isNull():
        #     print("图像加载失败")

#火箭发射
    def draw_rocket_launch(self, painter):
        if self.ROCK_LAUNCH == False:
            rocket_rect = QRect(1350,  self.ROCKT_ACTION, 100, 600)
            rocket_img = QImage("images/hj-removebg.png")
            painter.drawImage(rocket_rect, rocket_img)
            if self.HUOJIAN == True and self.ROCK_LAUNCH == False:
                self.ROCKT_ACTION -= 5
                if self.ROCKT_ACTION + 400<= 0 :
                     self.ROCKT_ACTION = 0
                     self.ROCK_LAUNCH = True
    def draw_kun_(self,painter):
        if self.KUNKUN_DISPLAY== True:
            rocket_rect = QRect(1300,  self.ROCKT_ACTION-100, 300, 300)
            rocket_img = QImage("images/OIP__1_-removebg-preview.png")
            painter.drawImage(rocket_rect, rocket_img)
            if self.HUOJIAN == True and self.ROCK_LAUNCH == False:
                self.ROCKT_ACTION -= 5
                if self.ROCKT_ACTION + 400<= 0 :
                    self.ROCKT_ACTION = 0
                    self.ROCK_LAUNCH = True

    def draw_monster(self,painter):
        monster_rect = QRect(self.MONSTER_ACTION_X, self.MONSTER_ACTION_Y, 100, 100)
        monster_img = QImage("images/monster/" + self.MONSTER_LEFT_RIGHT + "/" + str(self.MONSTER_ACTION) + ".png")
        painter.drawImage(monster_rect,monster_img)
        self.MONSTER_ACTION += 1
        if (self.MONSTER_ACTION > 4):
            self.MONSTER_ACTION = 0

        if (self.MONSTER_LEFT_RIGHT == "monsterR"):
            self.MONSTER_ACTION_X +=5
            if (self.MONSTER_ACTION_X >= self.MARIO_X + 500):
                self.MONSTER_ACTION_X = self.MARIO_X + 300
                self.MONSTER_LEFT_RIGHT = "monsterL"
        else:
            self.MONSTER_ACTION_X -= 5
            if (self.MONSTER_ACTION_X <= self.MARIO_X + 100):
                self.MONSTER_ACTION_X = self.MARIO_X + 100
                self.MONSTER_LEFT_RIGHT = "monsterR"

    def mario(self, painter):
        mario_rect = QRect(self.MARIO_ACTION_X,self.MARIO_ACTION_Y,100,100)
        if(self.MARIO_IS_RUN):
            mario_img = QImage("images/mario/smallmario/"+ self.MARIO_LEFT_RIGHT+ "/" +str(self.MARIO_ACTION)+".png")
        else:
            mario_img = QImage("images/mario/smallmario/"+ self.MARIO_LEFT_RIGHT+ "/stand.png")
        painter.drawImage(mario_rect,mario_img)
        self.MARIO_ACTION+=1
        if(self.MARIO_ACTION>21):
            self.MARIO_ACTION=0
        if (self.MARIO_ACTION_X >= 1300):
            self.MARIO_ACTION_X = 1300
            self.MARIO_LEFT_RIGHT = "marioL"
        if (self.MARIO_ACTION_X <= 50):
            self.MARIO_ACTION_X = 50
            self.MARIO_LEFT_RIGHT = "marioR"
        #上天
        if (self.MARIO_STATE == 1 and self.MARIO_JUMP_HEIGHT>0):
            self.MARIO_ACTION_Y -= self.MARIO_SPEED_Y
            self.MARIO_JUMP_HEIGHT -= self.MARIO_SPEED_Y
            if(self.MARIO_ACTION_Y <= 30):
                self.MARIO_ACTION_Y = 30
                self.MARIO_STATE = 2
                self.MARIO_JUMP_HEIGHT = 550
            if(self.MARIO_IS_RUN):
                if(self.MARIO_LEFT_RIGHT == "marioR"):
                    self.MARIO_ACTION_X += self.MARIO_SPEED_X // 2
                else:
                    self.MARIO_ACTION_X -= self.MARIO_SPEED_X // 2
        elif(self.MARIO_STATE == 1 and self.MARIO_JUMP_HEIGHT<=0):
            self.JUMP_FLAG = False
            self.MARIO_STATE = 2
            self.MARIO_JUMP_HEIGHT = self.MARIO_JUMP_MAX_HEIGHT
        #下降
        if (self.MARIO_STATE == 2 ):#and self.MARIO_JUMP_HEIGHT > 0):
            self.JUMP_FLAG = False
            self.MARIO_ACTION_Y += self.MARIO_SPEED_Y
            self.MARIO_JUMP_HEIGHT -= self.MARIO_SPEED_Y
            if (self.MARIO_ACTION_Y >= self.MARIO_Y):
                self.MARIO_ACTION_Y = self.MARIO_Y
                self.MARIO_STATE = 0
                self.MARIO_JUMP_HEIGHT = 0
            if (self.MARIO_IS_RUN):
                if (self.MARIO_LEFT_RIGHT == "marioR"):
                    self.MARIO_ACTION_X += self.MARIO_SPEED_X // 2
                else:
                    self.MARIO_ACTION_X -= self.MARIO_SPEED_X // 2
        elif (self.MARIO_STATE == 2 and self.MARIO_JUMP_HEIGHT <= 0):
            self.MARIO_STATE = 0
            self.MARIO_IS_RUN = False
            self.MARIO_JUMP_HEIGHT = self.MARIO_JUMP_MAX_HEIGHT


    def draw_tortoise(self,painter):
        tortoise_rect=QRect(self.TORTOISE_ACTION_X,self.TORTOISE_ACTION_Y,100,100)
        tortoise_img=QImage("images/tortoise/"+self.TORTOISE_LEFT_RIGHT+"/"+str(self.TORTOISE_ACTION)+".png")
        painter.drawImage(tortoise_rect,tortoise_img)
        self.TORTOISE_ACTION +=1
        if(self.TORTOISE_ACTION>11):
            self.TORTOISE_ACTION=0
        if(self.TORTOISE_LEFT_RIGHT=="tortoiseR"):
            self.TORTOISE_ACTION_X += 5
            if(self.TORTOISE_ACTION_X >= self.MARIO_X+1000):
                self.TORTOISE_ACTION_X = self.MARIO_X+1000
                self.TORTOISE_LEFT_RIGHT = "tortoiseL"
        else:
            self.TORTOISE_ACTION_X -= 5
            if(self.TORTOISE_ACTION_X <= self.MARIO_X +700):
                self.TORTOISE_ACTION_X = self.MARIO_X +700
                self.TORTOISE_LEFT_RIGHT = "tortoiseR"

    def draw_Obstacle(self, painter):
        #方块
        abnormalwall_rect = QRect(self.MARIO_X+200, self.MARIO_Y-200, 100, 100)
        abnormalwall_img = QImage("images/wall/abnormalwall.png")
        painter.drawImage(abnormalwall_rect,abnormalwall_img)

        #金币
        money1_rect = QRect(self.MARIO_X+400, self.MARIO_Y, 100, 100)
        money1_img = QImage("images/money.png")
        if (self.MONEY1_DISPLAY):
            painter.drawImage( money1_rect,money1_img)

        money2_rect = QRect(self.MARIO_X+600, self.MARIO_Y, 100, 100)
        money2_img = QImage("images/money.png")
        if (self.MONEY2_DISPLAY):
            painter.drawImage(money2_rect, money2_img)

        money3_rect = QRect(self.MARIO_X + 1000, self.MARIO_Y, 100, 100)
        money3_img = QImage("images/money.png")
        if (self.MONEY3_DISPLAY):
            painter.drawImage(money3_rect, money3_img)

        #下水道
        pipe_rect = QRect(self.MARIO_X + 800, self.MARIO_Y, 100, 100)
        pipe_img = QImage("images/pipe.png")
        painter.drawImage(pipe_rect, pipe_img)

        #墙
        for i in range(6):
            normalwall1_rect = QRect(self.MARIO_X + 600+i*100, self.MARIO_Y-200, 100, 100)
            normalwall1_img = QImage("images/wall/normalwall.png")
            painter.drawImage(normalwall1_rect, normalwall1_img)
        for i in range(2):
            normalwall2_rect = QRect(self.MARIO_X + 600 + i*500, self.MARIO_Y - 300, 100, 100)
            normalwall2_img = QImage("images/wall/normalwall.png")
            painter.drawImage(normalwall2_rect, normalwall2_img)

        #塔
        tower_rect = QRect(self.MARIO_X + 1100, self.MARIO_Y - 500, 100, 100)
        tower_img = QImage("images/tower.png")
        painter.drawImage(tower_rect, tower_img)

        #生命
        live_rect = QRect(self.MARIO_X -80, self.MARIO_Y - 570, 100, 40)
        live_img = QImage("images/life/s"+str(self.MARIO_LIVE)+".png")
        painter.drawImage(live_rect, live_img)

    def draw_Score(self,painter):
        painter.setPen(QColor(255,255,0))
        painter.setFont(QFont("宋体",20))
        painter.drawText(1000,50,"游戏得分:"+ str(self.GAME_SCORE))
        painter.drawText(100, 100, "乌景飞")
        painter.drawText(100, 130, "202305010101")


app = QApplication(sys.argv)
mario = Mario()
mario.show()
sys.exit(app.exec_())


