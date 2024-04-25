"""
XOs is the good old Tic-Tac-Toe PvP turn-based game.
Running in terminal, uses readchar library to check input.
It uses '\033[H\033[J' terminal code to clear screen and '\033[F\033[K' to clear last line, So it should run stably on linux and macos. 
NOT TESTED on windows.
PLESE NOTE! In this code, the Y-axis is always written before the X-axis.

wasd or arrow keys to move selector
spacebar or enter to select
"""
# ----------------- Check if you have a readchar library, install it if not
def check_installation(package):    
    import importlib
    import subprocess
    import platform

    try:
        importlib.import_module(package)
        print(f"{package} already installed.")
    except ImportError:
        print(f"{package} is not installed. Installing...")
        if platform.system() == "Darwin":
            subprocess.call(["pip3", "install", package])
        if platform.system() == "Linux" or platform.system() == "Windows":
            subprocess.call(["pip", "install", package])
        
check_installation("readchar")


# =============================== Start ================================== 
import readchar
import time

E = "   "   # empty cell
X = " X "   # X cell
O = " O "   # O cell
S = "[ ]"   # selected cell

def main():     # Main function
    player = X
    x = 0
    y = 0
    mtrx = [[E, E, E],      # That's the reason why using 'y' before 'x'
            [E, E, E],
            [E, E, E]]
    
    mtrx[y][x] = S
    
    while True:
        clear_screen()      # clear terminal
        
        mtrx, status = check_combo(mtrx, player)        # check if we have a winnig combination
        if status == "win":
            clear_screen()   
            print_screen(mtrx, player, status) 
            try_again()
            break
        
        print_screen(mtrx, player)                      # show frame
        
        dir = get_input()                               # check controls and return a direction
        mtrx, player = select_cell(mtrx, dir, player)   # move a selector
        
        time.sleep(0.08)                                # 0.08 seconds per frame equals 12.5fps; 0.04spf = 25fps
        
              
#================================================= End of main function 
    

# functions: __________________________________________________________

def clear_screen():
    print("\033[H\033[J", end='', flush=True)       # use this terminal comand to clear screen
    
 
def print_screen(mtrx: list, player, status=None):  # make a pretty little map
    screen = f"""
|---|---|---|
|{mtrx[0][0]}|{mtrx[0][1]}|{mtrx[0][2]}|
|---|---|---|
|{mtrx[1][0]}|{mtrx[1][1]}|{mtrx[1][2]}|
|---|---|---|
|{mtrx[2][0]}|{mtrx[2][1]}|{mtrx[2][2]}|
|---|---|---|\n"""      
    
    if status == "win":
        screen = f"{player} WINS!\n" + screen    
    else:    
        screen = f"{player} turn\n" + screen           
    print(screen)
    
    
def get_input():
    key = readchar.readkey()

    if key.lower() == "w" or key == "\x1b[A": dir = "up"
    elif key.lower() == "s" or key == "\x1b[B": dir = "down"
    elif key.lower() == "d" or key == "\x1b[C": dir = "right"
    elif key.lower() == "a" or key == "\x1b[D": dir = "left"
    elif key == " " or key == "\n": dir = "enter"
    else: dir = ""
                
    return dir


def find_empty(mtrx: list, y, x):
    E_indexes = [(row_index, col_index) for row_index, row in enumerate(mtrx) for col_index, val in enumerate(row) if val == E]     # return a list of tuples with y and x of empty cells
    if (y, x) in E_indexes:                 
        E_indexes.pop(E_indexes.index((y, x)))      # removing a current selected cell if it's in a list
    return E_indexes                    
    

def select_cell(mtrx: list, dir: str, player):      # a big but simple function to move between empty cells
    import random       # it will help me do decide what empty cell to select
    
    S_indexes = [(row_index, col_index) for row_index, row in enumerate(mtrx) for col_index, val in enumerate(row) if val == S]     # sort a matrix to retrurn a list of selected cells, contains only one tuple
    y, x = S_indexes[0]                                                                                                         # unpack a tuple
    
    # All selectors moves here:
    if dir == "up" and y > 0:
        if mtrx[y-1][x] == E: 
            mtrx[y][x] = E
            y -= 1
        elif y > 1 and mtrx[y-2][x] == E:
            mtrx[y][x] = E
            y -= 2
        else: 
            mtrx[y][x] = E
            y, x = find_empty(mtrx, y, x)[0]
            
    if dir == "down" and y < 2: 
        if mtrx[y+1][x] == E:
            mtrx[y][x] = E
            y += 1
        elif y < 1 and mtrx[y+2][x] == E:
            mtrx[y][x] = E
            y += 2
        else: 
            mtrx[y][x] = E
            y, x = find_empty(mtrx, y, x)[-1]
            
    if dir == "right" and x < 2: 
        if mtrx[y][x+1] == E:
            mtrx[y][x] = E
            x += 1
        elif x < 1 and mtrx[y][x+2] == E:
            mtrx[y][x] = E
            x += 2
        else: 
            mtrx[y][x] = E
            y, x = find_empty(mtrx, y, x)[-1]
                 
    if dir == "left" and x > 0: 
        if mtrx[y][x-1] == E:
            mtrx[y][x] = E
            x -= 1
        elif x > 1 and mtrx[y][x-2] == E:
            mtrx[y][x] = E
            x -= 2            
        else: 
            mtrx[y][x] = E
            y, x = find_empty(mtrx, y, x)[0]
        
    if dir == "enter":
        mtrx[y][x] = player
        y, x = find_empty(mtrx, y, x)[random.randint(0, len(find_empty(mtrx, y, x))-1)]     # its random module, baby! 
        if player == X:
            player = O
        else:
            player = X
        
    mtrx[y][x] = S
    return mtrx, player


def check_combo(mtrx, player):      # All winning combinations here:
    if mtrx[0][0] == player and mtrx[1][0] == player and mtrx[2][0] == player:
        new = [[val.replace(" ", "|") if val == player else val for val in line] for line in mtrx]
        return new, "win" 
    
    if mtrx[0][0] == player and mtrx[1][1] == player and mtrx[2][2] == player:
        new = [[val.replace(" ", "\\") if val == player else val for val in line] for line in mtrx]
        return new, "win"
            
    if mtrx[0][0] == player and mtrx[0][1] == player and mtrx[0][2] == player:
        new = [[val.replace(" ", ":") if val == player else val for val in line] for line in mtrx]
        return new, "win" 
              
    if mtrx[1][0] == player and mtrx[1][1] == player and mtrx[1][2] == player:
        new = [[val.replace(" ", ":") if val == player else val for val in line] for line in mtrx]
        return new, "win"  
         
    if mtrx[2][0] == player and mtrx[2][1] == player and mtrx[2][2] == player:
        new = [[val.replace(" ", ":") if val == player else val for val in line] for line in mtrx]
        return new, "win"       
    
    if mtrx[0][1] == player and mtrx[1][1] == player and mtrx[2][1] == player:
        new = [[val.replace(" ", "|") if val == player else val for val in line] for line in mtrx]
        return new, "win" 
    
    if mtrx[0][2] == player and mtrx[1][2] == player and mtrx[2][2] == player:
        new = [[val.replace(" ", "|") if val == player else val for val in line] for line in mtrx]
        return new, "win" 
    
    if mtrx[0][2] == player and mtrx[1][1] == player and mtrx[2][0] == player:
        new = [[val.replace(" ", "/") if val == player else val for val in line] for line in mtrx]
        return new, "win" 
    
    return mtrx, player


def try_again():    # a try again menu
    print("\nTry again?\n")
    var_y = ("[_Yes_]<--     _No__ \n")
    var_n = (" _Yes_     -->[_No__]\n")
    choise = var_y
    
    while True:
        print(choise)
        time.sleep(0.08)
        
        dir = get_input()
        if dir != "" and dir !="enter":
            if choise == var_y:
                choise = var_n
            else:
                choise = var_y
                
        elif dir == "enter" and choise == var_y:
            main()
        elif dir == "enter" and choise == var_n:
            print("\nGood bye!")
            time.sleep(2)
            clear_screen()
            break
                
        print("\033[F\033[K\033[F\033[K\033[F\033[K")     # clear last three lines
          
# Start program     
main()
