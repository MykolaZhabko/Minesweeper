import sweeperlib as sl
import random
import floodfill
from os import system
import time
from datetime import datetime
import json
import math

#GLOBAL VARIABLES
history = []

PER_PAGE = 10

available = []

#Dictionary for saving of played game info
results = {
    "start_time": 0,
    "end_time": 0,
    "start_game_date": 0,
    "end_game_date": 0,
    "mines": 0,
    "not_demined": 0,
    "demined": 0,
    "game_res": ""
}

#MAIN GAME DICTIONARY
state = {
    "field": [],
    "empty_field": [],
    "game": True,
    "first_click": False,
    "mines": 0,
    "win": 0,
    "game_win": False,
    "all_open": 0,
    "width": 0,
    "hight": 0
}

def save_history(history, filename):
    """
    This method saving the history about played game to the file
    """
    try:
        with open(filename, "w") as target:
            json.dump(history, target)
    except IOError:
        print("Unable to open the target file. Saving failed.")

def load_history(filename):
    """
    This method loads the history about played game to the list
    If there is no history inside the file method returns empty list
    """
    arr = []
    try:
        with open(filename) as source:
            arr = json.load(source)
    except (IOError, json.JSONDecodeError):
        print("Unable to open the target file. Starting with an empty collection.")

    return arr

def show_history(history):
    """
    This method shows the history in pleasant format to the console
    """
    pages = math.ceil(len(history) / PER_PAGE)
    for i in range(pages):
        start = i * PER_PAGE
        end = (i + 1) * PER_PAGE
        format_page(history[start:end], i)
        if i < pages - 1:
            input("   -- press enter to continue --")

def format_page(lines, page_n):
    """
    With this method you can format the history line about one played game
    """
    for i, result in enumerate(lines, page_n * PER_PAGE + 1):
        print("{i:2}. Played from {start_date} til {end_date}. Duration ({duration}). Result ({game_res}) Demined [{demined}] Not demined[{not_demined}]".format(
            i=i,
            start_date=result["start_game_date"],
            end_date=result["end_game_date"],
            duration=time.strftime("%H:%M:%S", time.gmtime(result["end_time"]-result["start_time"])),
            game_res=result["game_res"],
            demined=result["demined"],
            not_demined=result["not_demined"]
        ))

def count_mines_around(x, y, arr):
    count = 0
    if arr[y][x] == "x":
        return None
    # Corner with coordinates (0,0)
    if x == 0 and y == 0 and len(arr) > 1:
        for i in arr[0:2]:
            for j in i[0:2]:
                if j == "x":
                    count += 1
    #Corner with coordinates (0,last)
    elif x == len(arr[0]) - 1 and y == 0:
        for i,arr_i in enumerate(arr[0:2]):
            for j, arr_j in enumerate(arr_i[x-1:x+1]):
                if arr_j == "x":
                    count += 1

    elif x == 0 and y == len(arr)-1:
        for i in arr[len(arr)-2:len(arr)]:
            for j in i[0:2]:
                if j == "x":
                    count = count + 1


    elif y == len(arr)-1 and x == len(arr[0])-1:
        for i, arr_i in enumerate(arr[len(arr)-2:len(arr)]):
            for j, arr_j in enumerate(arr_i[len(arr_i)-2:len(arr_i)]):
                if arr_j == "x":
                    count += 1

    elif x > 0 and x < len(arr[0]) - 1 and y == 0:
        for i in arr[y:y+2]:
            for j in i[x-1:x+2]:
                if j == "x":
                    count += 1

    elif x > 0 and x < len(arr[0]) - 1 and y == len(arr) - 1:
        for i in arr[y-1:y+1]:
            for j in i[x-1:x+2]:
                if j == "x":
                    count += 1

    elif x == 0 and y > 0 and y < len(arr) - 1:
        for i in arr[y-1:y+2]:
            for j in i[x:x+2]:
                if j == "x":
                    count += 1

    elif x == len(arr[0]) - 1 and y > 0 and y < len(arr) - 1:
        for i in arr[y-1:y+2]:
            for j in i[x-1:x+1]:
                if j == "x":
                    count += 1

    elif x > 0 and x < len(arr[0]) - 1 and y > 0 and y < len(arr) - 1:
        for i in arr[y-1:y+2]:
            for j in i[x-1:x+2]:
                if j == "x":
                    count += 1
    return count

def place_mines(field, av_tile, mine_num):
    """
    Places N mines to a field in random tiles.
    """
    for i in range(mine_num):
        mine = random.choice(av_tile)
        #print(mine[0], mine[1])
        field[mine[0]][mine[1]] = "x"
        av_tile.remove(mine)

def draw_field():
    """
    A handler function that draws a field represented by a two-dimensional list
    into a game window. This function is called whenever the game engine requests
    a screen update.
    """
    sl.clear_window()
    sl.begin_sprite_draw()

    if state["game"] == True:
        for y, colums in enumerate(state["field"]):
            for x, rows in enumerate(colums):
                sl.prepare_sprite(state["empty_field"][y][x], x * 40, y * 40)
        sl.draw_sprites()

    elif not state["game"] and state["game_win"]:
        for y, colums in enumerate(state["field"]):
            for x, rows in enumerate(colums):
                sl.prepare_sprite(state["empty_field"][y][x], x * 40, y * 40)
        sl.draw_sprites()
        sl.draw_text("YOU WON", 0, 0, (0, 255, 0, 255),)

    else:
        for y, colums in enumerate(state["field"]):
            for x, rows in enumerate(colums):
                #sl.prepare_sprite(state["field"][y][x], x * 40, y * 40)
                sl.prepare_sprite(state["empty_field"][y][x], x * 40, y * 40)
        sl.draw_sprites()
        sl.draw_text("GAME OVER", 0, 0, (0, 255, 0, 255),)

def field_init():
    print("Before you start the game, input WIDTH and HIGHT and amount of MINES of the mine field with integers")
    while True:
        try:
            state["width"] = int(input("Input WIDTH of the field: "))
            state["hight"] = int(input("Input HIGHT of the field: "))
            state["mines"] = int(input("Input MINES amount: "))
            results["mines"] = state["mines"]
        except ValueError:
            print("WIDTH, HIGHT and MINES have to be integer numbers")
        else:

            #THE GAME STARTS HERE
            results["start_time"] = time.time()
            results["start_game_date"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


            #Initializing FIELD WICH IS CHANGED DURING THE GAME
            for row in range(state["hight"]):
                state["empty_field"].append([])
                for coll in range(state["width"]):
                    state["empty_field"][-1].append(" ")


            #Initializing FIELD WITH MINES
            for row in range(state["hight"]):
                state["field"].append([])
                for coll in range(state["width"]):
                    state["field"][-1].append(" ")

            #Initializing AVAILANBLE INDICES FIELD
            for x in range(state["hight"]):
                for y in range(state["width"]):
                    available.append((x, y))

            break

def place_number(field):
    """
    this method counts how many mines around each tile inside the field
    and placing that number to that tile, if there is no mines around placing " ".
    """
    for i, row in enumerate(state["field"]):
        for j, coll in enumerate(row):
            mines = count_mines_around(j, i, state["field"])
            if mines != None:
                if mines == 0:
                    state["field"][i][j] = " "
                else:
                    state["field"][i][j] = mines

def mouse_handler(x, y, button, modifiers):

    #FINAL OF THE GAME
    if not state["game"]:
        history = load_history("results.json")
        history.append(results)
        save_history(history, "results.json")
        state["field"] = []
        state["empty_field"] = []
        state["game"] = True
        state["first_click"] = False
        state["mines"] = 0
        state["win"] = 0
        state["game_win"] = False
        state["all_open"] = 0
        state["width"] = 0
        state["hight"] = 0

        results["demined"] = 0
        results["not_demined"] = 0
        sl.close()

    else:
        if button == sl.MOUSE_LEFT and state["empty_field"][int(y/40)][int(x/40)] != "f":

            #The MINE is never appears at the first open tile
            if state["first_click"] == False:
                available.remove((int(y/40),int(x/40)))
                place_mines(state["field"], available, state["mines"])
                place_number(state["field"])
                state["first_click"] = True

            #If pressed tile is with MINE - GAME OVER
            if state["field"][int(y/40)][int(x/40)] == "x":
                state["game"] = False
                results["end_time"] = time.time()
                results["end_game_date"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                results["game_res"] = "Lost"

                for i, val in enumerate(state["field"]):
                    for j, val_2 in enumerate(val):
                        if val_2 == "x" and state["empty_field"][i][j] != "f":
                            state["empty_field"][i][j] = "x"
                            results["not_demined"] += 1
                        if val_2 == "x" and state["empty_field"][i][j] == "f":
                            results["demined"] += 1
                state["empty_field"][int(y/40)][int(x/40)] = "b"

            #Flood fill if EMPTY TILE
            elif state["field"][int(y/40)][int(x/40)] == " ":
                floodfill.floodfill(state["field"], state["empty_field"], int(x/40), int(y/40))
            else:
                state["empty_field"][int(y/40)][int(x/40)] = state["field"][int(y/40)][int(x/40)]

            #Wining STATE
            for i, val in enumerate(state["empty_field"]):
                for j, val_2 in enumerate(val):
                    if (state["empty_field"][i][j] == " " and state["field"][i][j] == "x") or (state["empty_field"][i][j] == "f" and state["field"][i][j] == "x"):
                        state["win"] += 1

                    elif state["empty_field"][i][j] != " " and state["empty_field"][i][j] != "f":
                        state["all_open"] += 1


            if state["win"] == state["mines"] and state["all_open"] == (state["hight"] * state["width"] - state["mines"]):
                for i, val in enumerate(state["empty_field"]):
                    for j, val_2 in enumerate(val):
                        if state["empty_field"][i][j] == " " and state["field"][i][j] == "x":
                            state["empty_field"][i][j] = "f"
                state["game"] = False
                state["game_win"] = True
                results["end_time"] = time.time()
                results["end_game_date"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                results["game_res"] = "Won"
                results["demined"] = state["mines"]
                results["not_demined"] = 0

            state["win"] = 0
            state["all_open"] = 0


        #Plasing FLAG or Removing FLAG
        elif button == sl.MOUSE_RIGHT:
            if state["empty_field"][int(y/40)][int(x/40)] == " ":
                state["empty_field"][int(y/40)][int(x/40)] = "f"
            elif state["empty_field"][int(y/40)][int(x/40)] == "f":
                state["empty_field"][int(y/40)][int(x/40)] = " "

        #Redrawing field ()
        draw_field()
        sl.draw_sprites()


def minesweeper():
    #system("clear")
    field_init()
    sl.create_window(len(state["field"][0]) * 40, len(state["field"]) * 40)
    sl.load_sprites("spritet")
    sl.set_draw_handler(draw_field)
    sl.set_mouse_handler(mouse_handler)
    sl.start()

def menu(source_file):
    print("Welcome to the MINESWEEPER GAME")
    print("(S)tart the game")
    print("(R)esults of the played games")
    print("(Q)uit")
    while True:
        choice = input("Make your choice: ").strip().lower()
        if choice == "s":
            minesweeper()
        elif choice == "r":
            history = load_history(source_file)
            show_history(history)
        elif choice == "q":
            break
        else:
            print("The chosen feature is not available.")

if __name__ == "__main__":
    menu("results.json")
