from tkinter import *
import time

tk = Tk()
tk.title("Pacman game")  # create tittle of the window
# tk.resizeable(0,0) # 0,0 => cannot move the window, but did not need btw
# tk.wm_attributes("-topmost",1) #to make the priority if the window

canvas = Canvas(tk, width=1200, height=800, bd = 0, highlightthickness = 0)  # create the canvas window
# canvas is canvas not actually the window
tk.geometry("+20+0")  # geometry ("ww x wh +pw +ph") #set position of the window
canvas.configure(background='black')
canvas.pack()
tk.update()
# ----------------------SETUP MAP ARRAY---------------------------

file = open("map2.txt", "r")

config = file.readline()
config = list(map(int, config.split()))

N = config[0]
M = config[1]



array = []
for i in range(int(N)):
    x = file.readline()
    array.append(list(map(int, x.split())))

pos_pacman = file.readline()
pos_pacman = list(map(int, pos_pacman.split()))

px=int(pos_pacman[0])
py=int(pos_pacman[1])
array[px][py]=4
# ---------------------FINISH INIT STATE---------------------------
FPS=64 # this value is frame per second. The more it is, the smoother it will be
class Pacman:
    def __init__(self, canvas,array, color,score,emptypath):
        self.step = 0
        self.canvas = canvas  # this state create the pacman canvas
        self.matrix = array
        self.color=color
        self.score=score
        self.emptypath=emptypath
        self.predict = 0
        self.highscore = 0
        self.title = title
        self.canvas_height = self.canvas.winfo_height()  # set the pacman canvas detected height equal to the window canvas height
        self.canvas_width = self.canvas.winfo_width()  # set the pacman canvas detected width equal to the window canvas width
        self.pixel_per_matrix_w = float(self.canvas_width) / M
        self.pixel_per_matrix_h = float(self.canvas_height) / (N+1)
        self.check=False
        for i in range(N):
            for j in range(M):
                if self.matrix[i][j] == 4:
                    self.id = canvas.create_oval(15, 15,self.pixel_per_matrix_w-15,self.pixel_per_matrix_h-15,width=2.5, fill=color)  # create pacman has the this->color
                    canvas.move(self.id, j * self.pixel_per_matrix_w, i * self.pixel_per_matrix_h)  # draw first state of the pacman
                    self.xstart=j
                    self.ystart=i

    def draw(self):
        self.canvas.move(self.id, self.x*self.pixel_per_matrix_w, self.y*self.pixel_per_matrix_h) # ******set the next move (id,xnext,ynext)******



    def nextmove(self):
        print(self.matrix)
        for i in range(N):
            for j in range(M):
                if self.matrix[i][j] == 4:
                    self.xend=j
                    self.yend=i
                    self.x=(self.xend - self.xstart)/float(FPS)
                    self.y=(self.yend - self.ystart)/float(FPS)
                    for o in range(FPS):
                        self.draw()
                        tk.update_idletasks()
                        tk.update()
                        time.sleep(1.0/FPS)
                    self.xstart=self.xend
                    self.ystart = self.yend

    #def finish(self):
    def remap(self):
        for i in range(N):
            for j in range (M):
                if self.matrix[i][j] == -1:
                    self.matrix[i][j]=0
    #---------------------level1-------------------------------------
    def level1(self):
        nQ , l=0,0

        Q = M * N
        Qi, Qj, Qk = [0 for a in range(Q)], [0 for b in range(Q)], [0 for c in range(Q)]
        path=[0 for d in range(11)]
        nQ += 1
        Qi[nQ-1]=px
        Qj[nQ - 1] = py
        Qk[nQ -1] =0
        count = 0
        self.matrix[px][py]=-1
        print(self.matrix[Qi[count]][Qj[count]])
        #for r in range(N):
            #for c in range (M):
        while self.matrix[Qi[count]][Qj[count]] != 2 and count < nQ:
            if self.matrix[Qi[count] - 1][Qj[count]] == 0 or self.matrix[Qi[count] - 1][Qj[count]] == 2:
                nQ += 1
                Qi[nQ-1] = Qi[count] - 1
                Qj[nQ - 1] = Qj[count]
                Qk[nQ - 1] = count
                if self.matrix[Qi[count] - 1][Qj[count]] == 0:
                    self.matrix[Qi[count] - 1][Qj[count]] = -1
            if self.matrix[Qi[count] + 1][Qj[count]] == 0 or self.matrix[Qi[count] + 1][Qj[count]] == 2:
                nQ += 1
                Qi[nQ-1] = Qi[count] + 1
                Qj[nQ - 1] = Qj[count]
                Qk[nQ - 1] = count
                if self.matrix[Qi[count] + 1][Qj[count]] == 0:
                    self.matrix[Qi[count] + 1][Qj[count]] = -1
            if self.matrix[Qi[count]][Qj[count] - 1] == 0 or self.matrix[Qi[count]][Qj[count] - 1] == 2:
                nQ += 1
                Qi[nQ-1] = Qi[count]
                Qj[nQ - 1] = Qj[count] - 1
                Qk[nQ - 1] = count
                if self.matrix[Qi[count]][Qj[count] - 1] == 0:
                    self.matrix[Qi[count]][Qj[count] - 1] = -1
            if self.matrix[Qi[count]][Qj[count] + 1] == 0 or self.matrix[Qi[count]][Qj[count] + 1] == 2:
                nQ+= 1
                Qi[nQ -1] = Qi[count]
                Qj[nQ - 1] = Qj[count] + 1
                Qk[nQ - 1] = count
                if self.matrix[Qi[count]][Qj[count] + 1] == 0:
                    self.matrix[Qi[count]][Qj[count] + 1] = -1

            count += 1
        if self.matrix[Qi[count]][Qj[count]] != 2:
            print("step:", 0)
            print("point:", 0)
            print("GAME OVER")
            self.title.gameover()
            return
        self.remap()
        while count != 0:
            l +=1
            if l > 10:
                print("step:", 0)
                print("point:", 0)
                print("GAME OVER")
                self.title.gameover()
                return
            path[l - 1] = count
            count = Qk[count]
        path[l] = 0
        step = l
        while l>0:
            self.matrix[Qi[path[l - 1]]][Qj[path[l - 1]]] = 4
            self.matrix[Qi[path[l]]][Qj[path[l]]] = 0
            self.score.hit()
            self.nextmove()
            l -=1
            self.emptypath.hit(Qi[path[0]],Qj[path[0]],'yellow')
        self.score.hitfood()
        print("step:", step)
        print("point:", self.score.score)
        print("GAME OVER")
        self.title.gameover()
        
    #0-------------------------level 2-----------------------
    def level2(self):
        self.level1()

    #--------------------------level 3-----------------------
    def countPredict(self,matrix3,posi,posj):
        c = 0
        if matrix3[posi - 1][posj] == 0 and self.matrix[posi - 1][posj] == 2:
            c += 10
            matrix3[posi - 1][posj] = 1

        if matrix3[posi + 1][posj] == 0 and self.matrix[posi + 1][posj] == 2:
            c += 10
            matrix3[posi + 1][posj] = 1

        if matrix3[posi][posj- 1] == 0 and self.matrix[posi][posj - 1] == 2:
            c += 10
            matrix3[posi][posj - 1] = 1

        if matrix3[posi][posj + 1] == 0 and self.matrix[posi][posj+ 1] == 2:
            c += 10
            matrix3[posi][posj + 1] = 1
        self.cp=c

    def algo3 (self, matrix3, posi, posj, back):
        self.matrix[posi][posj] = 4
        self.step+=1
        self.emptypath.hit(posi,posj,'yellow')
        self.countPredict(matrix3, posi, posj)
        self.nextmove()
        self.emptypath.hit(posi,posj,'black')
        c=self.cp
        print(c)
        if c > 10:
            back = 1
        self.predict += c
        if (self.score.score + self.predict) > self.highscore :
            if self.matrix[posi - 1][posj] == 2 and not self.check:
                self.matrix[posi][posj] = 0
                self.score.hit()
                self.score.hitfood()
                if self.score.score > self.highscore:
                    self.highscore = self.score.score
                self.predict -= 10
                back +=1
                self.algo3(matrix3, posi - 1, posj, back)
                if not self.check:
                    self.matrix[posi][posj] = 4
                    self.nextmove()

            if self.matrix[posi+ 1][posj] == 2 and not self.check:
                self.matrix[posi][posj] = 0
                self.score.hit()
                self.score.hitfood()
                if self.score.score > self.highscore:
                    self.highscore = self.score.score
                self.predict -= 10
                back += 1
                self.algo3(matrix3, posi+ 1, posj, back)
                if not self.check:
                    self.matrix[posi][posj] = 4
                    self.nextmove()

            if self.matrix[posi][posj- 1] == 2 and not self.check:
                self.matrix[posi][posj] = 0
                self.score.hit()
                self.score.hitfood()
                if self.score.score > self.highscore:
                    self.highscore = self.score.score
                self.predict -= 10
                back +=1
                self.algo3(matrix3, posi , posj-1, back)
                if not self.check:
                    self.matrix[posi][posj] = 4
                    self.nextmove()

            if self.matrix[posi][posj+1] == 2 and not self.check:
                self.matrix[posi][posj] = 0
                self.score.hit()
                self.score.hitfood()
                if self.score.score > self.highscore:
                    self.highscore = self.score.score
                self.predict -= 10
                back +=1
                self.algo3(matrix3, posi , posj+1, back)
                if not self.check:
                    self.matrix[posi][posj] = 4
                    self.nextmove()

        if back >= self.predict or self.check :
            self.check = True
            return

        self.score.hit()
        self.predict -=1
        self.matrix[posi][posj] = 0
        self.step+=1

    def level3(self):
        matrix3 =[[0 for i in range (M)] for j in range(N)]
        back = 0
        print(matrix3)
        self.algo3(matrix3, px, py, back)
        self.step -= 1
        print("step: ", self.step)
        print("point: ", self.score.score)
        print("GAME OVER")
        self.title.gameover()


class Wall:
    def __init__(self,canvas,array,color,):
        self.canvas=canvas
        self.matrix=array
        self.canvas_height = self.canvas.winfo_height()  # set the pacman canvas detected height equal to the window canvas height
        self.canvas_width = self.canvas.winfo_width()  # set the pacman canvas detected width equal to the window canvas width
        self.pixel_per_matrix_w=float(self.canvas_width)/M
        self.pixel_per_matrix_h=float(self.canvas_height)/(N+1)
        for i in range(N):
            for j in range(M):
                if self.matrix[i][j]==1:
                    self.id = canvas.create_rectangle(0, 0, self.pixel_per_matrix_w, self.pixel_per_matrix_h,width=15,outline=color, fill='black')
                    canvas.move(self.id, j * self.pixel_per_matrix_w , i * self.pixel_per_matrix_h)


class EmptyPath:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.matrix = array
        self.canvas_height = self.canvas.winfo_height()  # set the pacman canvas detected height equal to the window canvas height
        self.canvas_width = self.canvas.winfo_width()  # set the pacman canvas detected width equal to the window canvas width
        self.pixel_per_matrix_w = float(self.canvas_width) / M
        self.pixel_per_matrix_h = float(self.canvas_height) / (N + 1)

    def hit(self,posi,posj, color):
        id = self.canvas.create_oval(30, 30, self.pixel_per_matrix_w-30,self.pixel_per_matrix_h-30 , fill=color)
        self.canvas.move(id, posj * self.pixel_per_matrix_w , posi * self.pixel_per_matrix_h)
        
class Food:
    def __init__(self, canvas, array, color):
        self.canvas = canvas
        self.matrix = array
        self.food_num=0
        self.canvas_height = self.canvas.winfo_height()  # set the pacman canvas detected height equal to the window canvas height
        self.canvas_width = self.canvas.winfo_width()  # set the pacman canvas detected width equal to the window canvas width
        self.pixel_per_matrix_w = float(self.canvas_width) / M
        self.pixel_per_matrix_h = float(self.canvas_height) / (N + 1)
        for i in range(N):
            for j in range(M):
                if self.matrix[i][j] == 2:
                    self.id = canvas.create_oval(30, 30, self.pixel_per_matrix_w-30,self.pixel_per_matrix_h-30 , fill=color)
                    canvas.move(self.id, j * self.pixel_per_matrix_w , i * self.pixel_per_matrix_h)
                    self.food_num += 1

#class Monster:
class Score(Pacman):
    def __init__(self,canvas,color):
        self.score = 0
        self.canvas = canvas
        self.canvas_height = self.canvas.winfo_height()  # set the pacman canvas detected height equal to the window canvas height
        self.canvas_width = self.canvas.winfo_width()  # set the pacman canvas detected width equal to the window canvas width
        self.id = canvas.create_text(20,self.canvas_height-40, text = self.score,font = ('Consolas',20) , fill = color)

    def hit(self): #2 tao su thay doi khi tang diem so
        self.score -= 1
        self.canvas.itemconfig(self.id, text = self.score)
    
    def hitfood(self):
        self.score += 10
        self.canvas.itemconfig(self.id, text = self.score)

class Title:
    def __init__(self,canvas,color):
        self.canvas=canvas
        self.canvas_height = self.canvas.winfo_height()  # set the pacman canvas detected height equal to the window canvas height
        self.canvas_width = self.canvas.winfo_width()  # set the pacman canvas detected width equal to the window canvas width
        self.id= canvas.create_text(600, self.canvas_height-40, text='PACMAN GAME', font=('Consolas', 30), fill=color)
    def gameover(self):
        self.canvas.itemconfig(self.id,text='GAME OVER')

class Monster:
    def __init__(self, canvas, array, color):
        self.canvas = canvas
        self.matrix = array
        self.canvas_height = self.canvas.winfo_height()  # set the pacman canvas detected height equal to the window canvas height
        self.canvas_width = self.canvas.winfo_width()  # set the pacman canvas detected width equal to the window canvas width
        self.pixel_per_matrix_w = float(self.canvas_width) / M
        self.pixel_per_matrix_h = float(self.canvas_height) / (N + 1)
        for i in range(N):
            for j in range(M):
                if self.matrix[i][j] == 3:
                    self.id = canvas.create_oval(20, 20, self.pixel_per_matrix_w-20,self.pixel_per_matrix_h-20 , fill=color)
                    canvas.move(self.id, j * self.pixel_per_matrix_w , i * self.pixel_per_matrix_h)
# -------------------------MAIN----------------------------
score=Score(canvas,"green")
emptypath = EmptyPath(canvas,'black')
wall=Wall(canvas,array,'blue')
food=Food(canvas,array,'orange')
monster=Monster(canvas, array, "red")
title=Title(canvas,'white')
pacman_AI = Pacman(canvas,array, 'yellow',score,emptypath)  # create the orange pacman
pacman_AI.level3()
tk.mainloop()
tk.update_idletasks()
tk.update()

# while True:4hn6
#     pacman_AI.draw()  # --PACMAN---
#     tk.update_idletasks()
#     tk.update()
#     time.sleep(0.01)