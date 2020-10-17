from bangtal import *
import random

scene1 = Scene("씬","Images/배경.png")

INIT_CX = 4
INIT_CY = 19
COLOR_BLANK = 7
LEFT = 0
RIGHT = 1
DOWN = 2
CHECK_OUTSIDE = 0
CHECK_FILLED = 1
CHECK_BLANK = 2

TIMER_PERIOD = 0.7

cx = 0
cy = 0
# Color : 0~6 Tetris block, 7 : Blank, 8 : 
c_num = 1 # TODO Random
c_dir = 0
# dx [num][dircetion][rotate][0=y 1=x]
d = [ [ [ [0, -1], [0, 0], [0, 1], [0, 2] ], [ [-2, 1], [-1, 1], [0, 1], [1, 1] ], [ [-1, -1], [-1, 0], [-1, 1], [-1, 2] ], [ [-2, 0], [-1, 0], [0, 0], [1, 0] ]  ],
[ [ [0, -1], [0, 0], [0, 1], [1, -1] ], [ [-1, 0], [0, 0], [1, 1], [1, 0] ], [ [-1, 1], [0, -1], [0, 1], [0, 0] ], [ [-1, -1], [-1, 0], [0, 0], [1, 0] ]  ],
[ [ [0, -1], [0, 0], [0, 1], [1, 1] ], [ [-1, 1], [-1, 0],  [0, 0], [1, 0] ], [ [-1, -1], [0, -1], [0, 1], [0, 0] ], [ [-1, 0], [0, 0], [1, -1], [1, 0] ]  ],
[ [ [0, 0], [0, 1], [1, 0], [1, 1] ], [ [0, 0], [0, 1], [1, 0], [1, 1] ], [ [0, 0], [0, 1], [1, 0], [1, 1] ], [ [0, 0], [0, 1], [1, 0], [1, 1] ]  ],
[ [ [0, -1], [0, 0], [1, 1], [1, 0] ], [ [-1, 1], [0, 1], [0, 0], [1, 0] ], [ [-1, -1], [-1, 0],  [0, 1], [0, 0] ], [ [-1, 0], [0, -1], [0, 0], [1, -1] ]  ],
[ [ [0, -1], [0, 0], [0, 1], [1, 0] ], [ [-1, 0], [0, 1], [0, 0], [1, 0] ], [ [-1, 0], [0, -1],  [0, 1], [0, 0] ], [ [-1, 0], [0, -1], [0, 0], [1, 0] ]  ],
[ [ [0, 1], [0, 0], [1, -1], [1, 0]  ], [ [-1, 0], [0, 1], [0, 0], [1, 1] ], [ [-1, 1], [-1, 0],  [0, -1], [0, 0] ], [ [-1, -1], [0, -1], [0, 0], [1, 0] ]  ] ]
dx = [-1, 1, 0]
dy = [0, 0, -1]

### CLASS
class Block:
    def __init__(self, bx, by):
        self.blockObj = Object("Images/block7.png")
        self.blockObj.locate(scene1, 100+24*bx, 100+24*by)
        self.blockObj.show()

        self.x = bx
        self.y = by
        self.color = 7
    def changeColor(self, c):
        self.color = c
        self.blockObj.setImage("Images/block"+str(c)+".png")


### FUNCTION
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

def new_block():
    global cx, cy, c_num, c_dir
    cx = INIT_CX
    cy = INIT_CY
    c_num = block_queue.pop() # TODO Random or next block's
    if len(block_queue)<8:
        refill_queue()
    c_dir = 0
    
    if check_block(cx, cy, c_num, c_dir) != CHECK_BLANK:
        #TODO game_over()
        endGame()
    
    set_block(cx, cy, c_num, c_num, c_dir)

def get_color(x, y):
    if x<0 or 9<x or y<0 or 20<y:
        return COLOR_BLANK
    return block[y][x].color

def set_color(x, y, c):
    if x<0 or 9<x or y<0 or 20<y:
        return False    
    block[y][x].changeColor(c)

def check_clear():
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



# r : LEFT 0, RIGHT 1
def rotate_block(r):
    global cx, cy, c_num, c_dir
    if r!=0 and r!=1 :
        print("ERR : rotate_block(), wrong 'r' input")
        return False

    t_dir = (c_dir + 2*r -1)%4

    set_block(cx, cy, c_num, COLOR_BLANK, c_dir)
    if check_block(cx, cy, c_num, t_dir) == CHECK_BLANK:        
        c_dir = t_dir
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
        cx = tx
        cy = ty
        set_block(tx, ty, c_num, c_num, c_dir)
        return True
    else:
        print("옮기기불가능")
        set_block(cx, cy, c_num, c_num, c_dir)
        if r == DOWN:
            check_clear()
            new_block()
            timer1.set(TIMER_PERIOD)
    return False

def refill_queue():
    random.shuffle(block_list)
    block_queue.extend(block_list)

def game_start():
    refill_queue()
    refill_queue()
    new_block()


def game_over():
    endGame()


def defaultMouseAction(object, x, y, action):
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
    

def defaultTimeOut(timer):
    if timer == timer1:
        move_block(DOWN)
        timer1.set(TIMER_PERIOD)
        timer1.start()



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


# 버튼만들기
Object.onMouseActionDefault = defaultMouseAction
button_rotate_right = Object("Images/button.png")
button_rotate_right.locate(scene1, 700, 200)
button_rotate_right.show()

button_rotate_left = Object("Images/button.png")
button_rotate_left.locate(scene1, 500, 200)
button_rotate_left.show()

button_move_right = Object("Images/button.png")
button_move_right.locate(scene1, 700, 130)
button_move_right.show()

button_move_left = Object("Images/button.png")
button_move_left.locate(scene1, 500, 130)
button_move_left.show()

button_move_down = Object("Images/button.png")
button_move_down.locate(scene1, 600, 130)
button_move_down.show()

button_move_Fdown = Object("Images/button.png")
button_move_Fdown.locate(scene1, 600, 60)
button_move_Fdown.show()

game_start()
Timer.onTimeoutDefault = defaultTimeOut
timer1 = Timer(TIMER_PERIOD)
timer1.start()

startGame(scene1)

