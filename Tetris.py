from bangtal import *
import random
from time import sleep

scene1 = Scene("씬","Images/배경4.png")

INIT_CX = 4
INIT_CY = 19
COLOR_BLANK = 7
COLOR_SHADOW = 8
LEFT = 0
RIGHT = 1
DOWN = 2
CHECK_OUTSIDE = 0
CHECK_FILLED = 1
CHECK_BLANK = 2

TIMER_PERIOD = 0.7
EFFECT_PERIOD = 0.1

cx = 0
cy = 0
# Color : 0~6 Tetris block, 7 : Blank, 8 : Shadow
c_num = 0
c_dir = 0
sx = 0
sy = 0
s_num = 0
s_dir = 0
h_num = COLOR_BLANK
# dx [num][dircetion][4 block][0=y 1=x]
d = [ [ [ [0, -1], [0, 0], [0, 1], [0, 2] ], [ [-2, 1], [-1, 1], [0, 1], [1, 1] ], [ [-1, -1], [-1, 0], [-1, 1], [-1, 2] ], [ [-2, 0], [-1, 0], [0, 0], [1, 0] ]  ],
[ [ [0, -1], [0, 0], [0, 1], [1, -1] ], [ [-1, 0], [0, 0], [1, 1], [1, 0] ], [ [-1, 1], [0, -1], [0, 1], [0, 0] ], [ [-1, -1], [-1, 0], [0, 0], [1, 0] ]  ],
[ [ [0, -1], [0, 0], [0, 1], [1, 1] ], [ [-1, 1], [-1, 0],  [0, 0], [1, 0] ], [ [-1, -1], [0, -1], [0, 1], [0, 0] ], [ [-1, 0], [0, 0], [1, -1], [1, 0] ]  ],
[ [ [0, 0], [0, 1], [1, 0], [1, 1] ], [ [0, 0], [0, 1], [1, 0], [1, 1] ], [ [0, 0], [0, 1], [1, 0], [1, 1] ], [ [0, 0], [0, 1], [1, 0], [1, 1] ]  ],
[ [ [0, -1], [0, 0], [1, 1], [1, 0] ], [ [-1, 1], [0, 1], [0, 0], [1, 0] ], [ [-1, -1], [-1, 0],  [0, 1], [0, 0] ], [ [-1, 0], [0, -1], [0, 0], [1, -1] ]  ],
[ [ [0, -1], [0, 0], [0, 1], [1, 0] ], [ [-1, 0], [0, 1], [0, 0], [1, 0] ], [ [-1, 0], [0, -1],  [0, 1], [0, 0] ], [ [-1, 0], [0, -1], [0, 0], [1, 0] ]  ],
[ [ [0, 1], [0, 0], [1, -1], [1, 0]  ], [ [-1, 0], [0, 1], [0, 0], [1, 1] ], [ [-1, 1], [-1, 0],  [0, -1], [0, 0] ], [ [-1, -1], [0, -1], [0, 0], [1, 0] ]  ] ]
dx = [-1, 1, 0]
dy = [0, 0, -1]

running_effect = [False, False]
can_move = True
y_list = []
count2 = 0

### CLASS
class Block:
    def __init__(self, bx, by):
        self.blockObj = Object("Images/block7.png")
        self.blockObj.locate(scene1, 140+24*bx, 100+24*by)
        self.blockObj.show()

        self.x = bx
        self.y = by
        self.color = 7
    def changeColor(self, c):
        self.color = c
        self.blockObj.setImage("Images/block"+str(c)+".png")


### FUNCTION
# For test
def print_var():
    global cx, cy, c_num, c_dir, h_num
    print("cx :"+ str(cx) +", cy :"+ str(cy) + ", c_num :"+ str(c_num) + ", c_dir :"+ str(c_dir) + ", h_num :"+ str(h_num))

def check_block(x, y, num, dir):
    dir = dir % 4
    num = num % 7
    for i in range(4):   
        tx = x + d[num][dir][i][1]
        ty = y + d[num][dir][i][0]        
        if tx<0 or 9<tx or ty<0 or 20<ty:            
            return CHECK_OUTSIDE
        tc = block[ty][tx].color
        if 0 <= tc and tc <7:            
            return CHECK_FILLED    
    return CHECK_BLANK

# center (x, y) num's block shape -> change color to 'color'
def set_block(x, y, num, color, dir):
    #TODO determine 3 lines really required    
    dir = dir % 4
    num = num % 7
    color = color % 9
       
    for i in range(4):   
        tx = x + d[num][dir][i][1]
        ty = y + d[num][dir][i][0]        
        block[ty][tx].changeColor(color)
    return True

def make_block(x, y, num, dir):
    set_block(x, shadow_y(x, y, num, dir), num, COLOR_SHADOW, dir)
    set_block(x, y, num, num, dir)

def delete_block(x, y, num, dir):
    set_block(x, shadow_y(x, y, num, dir), num, COLOR_BLANK, dir)
    set_block(x, y, num, COLOR_BLANK, dir)


def set_hold():
    print_var()
    global h_num, cx, cy, c_num, c_dir
    #set_block(cx, cy, c_num, COLOR_BLANK, c_dir)
    delete_block(cx, cy, c_num, c_dir)
    if h_num == COLOR_BLANK:        
        h_num = c_num
        new_block()
    elif check_block(cx, cy, h_num, 0) != CHECK_BLANK:
        print(check_block(cx, cy, h_num, 0))
        print("Hold block can't change with filled space")
        make_block(cx, cy, c_num, c_dir)
        return
    else:        
        t_num = c_num
        c_dir = 0
        c_num = h_num
        #set_block(cx, cy, c_num, c_num, c_dir)
        make_block(cx, cy, c_num, c_dir)
        h_num = t_num

    for i in range(2):
        for j in range(4):
            hold_block[i][j].changeColor(COLOR_BLANK)
    for i in range(4):   
        tx = 1 + d[h_num][0][i][1]
        ty = 0 + d[h_num][0][i][0]        
        hold_block[ty][tx].changeColor(h_num)

def set_next():
    global cx, cy, c_num, c_dir
    color = block_queue[0]

    for i in range(2):
        for j in range(4):
            next_block[i][j].changeColor(COLOR_BLANK)

    for i in range(4):
        tx = 1 + d[color][0][i][1]
        ty = 0 + d[color][0][i][0]
        next_block[ty][tx].changeColor(color)
    

def new_block():    
    global cx, cy, c_num, c_dir
    cx = INIT_CX
    cy = INIT_CY
    c_num = block_queue.pop(0)
    
    if len(block_queue)<8:
        refill_queue()
    c_dir = 0    
    
    if check_block(cx, cy, c_num, c_dir) != CHECK_BLANK:
        #TODO game_over()
        endGame()

    set_block(cx, shadow_y(cx, cy, c_num, c_dir), c_num, COLOR_SHADOW, c_dir )
    set_block(cx, cy, c_num, c_num, c_dir)   

    set_next()
    timer1.set(TIMER_PERIOD)


def get_color(x, y):
    if x<0 or 9<x or y<0 or 20<y:
        return COLOR_BLANK
    return block[y][x].color

def set_color(x, y, c):
    if x<0 or 9<x or y<0 or 20<y:
        return False    
    block[y][x].changeColor(c)

def check_clear():
    global y_list
    y_list = []
    flag = True
    for i in range(cy-2, cy+2):
        if i<0 or 20<i:
            continue
        flag = True
        for j in range(10):
            if abs(block[i][j].color - 3) > 3:
                flag = False
        if flag == True:            
            y_list.append(i)

    if len(y_list)==0 :
        return False    
    return True

    
def clear_line():
    global y_list
    
    dc = []
    for i in range(21):
        dc.append(0)

    for i in range(len(y_list)):
        k = y_list[i] - i
        for j in range( k, 21 ):
            dc[j] +=1
    print(y_list)
    print(dc)
    for i in range(21):
        if dc[i] == 0:            
            continue
        for j in range(10):
            set_color(j, i, get_color(j, i+dc[i]))
    print("HERE")
    new_block()





# r : LEFT 0, RIGHT 1
def rotate_block(r):
    global cx, cy, c_num, c_dir
    if r!=0 and r!=1 :
        print("ERR : rotate_block(), wrong 'r' input")
        return False

    t_dir = (c_dir + 2*r -1)%4

    set_block(cx, cy, c_num, COLOR_BLANK, c_dir)
    if check_block(cx, cy, c_num, t_dir) == CHECK_BLANK:
        set_block(cx, shadow_y(cx, cy, c_num, c_dir), c_num, COLOR_BLANK, c_dir)
        c_dir = t_dir
        set_block(cx, shadow_y(cx, cy, c_num, c_dir), c_num, COLOR_SHADOW, t_dir)
        set_block(cx, cy, c_num, c_num, t_dir)
        
        return True
    else:
        print("돌리기불가능")
        set_block(cx, cy, c_num, c_num, c_dir)
    return False

# r : LEFT 0, RIGHT 1, DOWN 2
def move_block(r):
    global cx, cy, c_num, c_dir, dx, dy
    if r!=0 and r!=1 and r!=2:
        print("ERR : move_block(), wrong 'r' input")
        return False
    
    tx = cx + dx[r]
    ty = cy + dy[r]

    set_block(cx, cy, c_num, COLOR_BLANK, c_dir)    
    if check_block(tx, ty, c_num, c_dir) == CHECK_BLANK:
        set_block(cx, shadow_y(cx, cy, c_num, c_dir), c_num, COLOR_BLANK, c_dir)    # remove shadow
        cx = tx
        cy = ty
        set_block(tx, shadow_y(cx, ty, c_num, c_dir), c_num, COLOR_SHADOW, c_dir)    # make new shadow
        set_block(tx, ty, c_num, c_num, c_dir)        
        return True
    else:
        print("옮기기불가능")
        set_block(cx, cy, c_num, c_num, c_dir)
        if r == DOWN:
            if not check_clear():
                new_block()
            else :
                global y_list
                timer1.set(20.0) #TODO is it good?
                can_move = False
                
                for i in range(len(y_list)):
                    effect0_obj[i].locate(scene1, 140, 100 + 24*y_list[i])
                    effect0_obj[i].show()
                running_effect[0] = True    
                timer2.set(EFFECT_PERIOD)
                timer2.start()
    return False

# TODO 최적화가능
def shadow_y(x, y, num, dir):
    ix = []
    iy = []    
    for i in range(4):        
        ix.append( x + d[num][dir][i][1] )
        iy.append( y + d[num][dir][i][0] )
    
    flag = True
    stack = 0
    passing = False
    
    while flag and stack<21:        
        y -= 1        
        for i in range(4):
            tx = x + d[num][dir][i][1]
            ty = y + d[num][dir][i][0]            
            if ty<0:                
                return y+1
            for j in range(4):
                if tx == ix[j] and ty == iy[j]:                    
                    passing = True 
            if passing == False and abs(block[ty][tx].color - 3) < 4:                
                flag = False
            passing = False
    return y+1


def refill_queue():
    random.shuffle(block_list)
    block_queue.extend(block_list)



def game_start():
    refill_queue()
    refill_queue()    
    new_block()

def game_over():
    endGame()


def effect_clear(list):
    length = len(list)
    for i in range(length):
        effect0_obj[i].locate(scene1, 160, 100 + 24*list[i])
        effect0_obj[i].show()
    running_effect[0] = True
    timer2.set(EFFECT_PERIOD)
    timer2.start()
    while running_effect[0]:
        sleep(0.03)



def defaultMouseAction(object, x, y, action):
    if can_move==True:
        if object == button_rotate_right:
            rotate_block(RIGHT)
        elif object == button_rotate_left:
            rotate_block(LEFT)
        elif object == button_move_right:
            move_block(RIGHT)
        elif object == button_move_left:
            move_block(LEFT)
        elif object == button_move_down:
            can = move_block(DOWN)
        elif object == button_move_Fdown:
            while move_block(DOWN):
                pass
        elif object == button_hold:   
            set_hold()
    

def defaultTimeOut(timer):
    global count2
    if timer == timer1:
        move_block(DOWN)
        timer1.set(TIMER_PERIOD)
        timer1.start()
    elif timer == timer2:
        print(count2)
        if count2==6 :
            print("THERE")
            for i in range(4):
                effect0_obj[i].hide()
            running_effect[0] = False
            can_move = True
            clear_line()            
            count2=0
        else:
            count2+=1
            for i in range(4):
                effect0_obj[i].setImage("Images/eff_clear"+str(count2)+".png")
            timer2.set(EFFECT_PERIOD)
            timer2.start()



### MAIN
# 10 X 21 블록 만들기 block[y][x]
block = []
blockrow = []
for j in range (21):
    for i in range (10):
        blockrow.append(Block(i,j))        
    block.append(blockrow)
    blockrow = []

block_list = [0, 1, 2, 3, 4, 5, 6]
block_queue = []

# HOLD 블록 만들기
hold_block = []
for j in range(2):
    for i in range(4):
        blockrow.append(Block(i-5, j+18))
    hold_block.append(blockrow)
    blockrow = []

# NEXT 블록 만들기
next_block = []
for j in range(2):
    for i in range(4):
        blockrow.append(Block(i+11, j+18))
    next_block.append(blockrow)
    blockrow = []

# 버튼만들기
Object.onMouseActionDefault = defaultMouseAction
button_rotate_right = Object("Images/button_rotate_right.png")
button_rotate_right.locate(scene1, 544, 184)
button_rotate_right.show()

button_rotate_left = Object("Images/button_rotate_left.png")
button_rotate_left.locate(scene1, 420, 184)
button_rotate_left.show()

button_move_right = Object("Images/button_move_right.png")
button_move_right.locate(scene1, 544, 122)
button_move_right.show()

button_move_left = Object("Images/button_move_left.png")
button_move_left.locate(scene1, 420, 122)
button_move_left.show()

button_move_down = Object("Images/button_move_down.png")
button_move_down.locate(scene1, 482, 122)
button_move_down.show()

button_move_Fdown = Object("Images/button_move_Fdown.png")
button_move_Fdown.locate(scene1, 420, 60)
button_move_Fdown.show()

button_hold = Object("Images/button_hold.png")
button_hold.locate(scene1, 482, 184)
button_hold.show()

# 이펙트
effect0_obj = []
for i in range(4):
    effect0_obj.append(Object("Images/eff_clear0.png"))
    effect0_obj[i].locate(scene1, 140, 100+24*i)

# 타이머
Timer.onTimeoutDefault = defaultTimeOut
timer1 = Timer(TIMER_PERIOD)
timer1.start() #TODO START TIMER

timer2 = Timer(EFFECT_PERIOD)


game_start()
startGame(scene1)

