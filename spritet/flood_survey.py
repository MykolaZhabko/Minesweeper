import sweeperlib as sl


planet = [
    [" ", "x", " ", " ", " ", "x", " ", "x", "x", " ", "x", " ", " ", "x", "x", "x", "x", "x", " ", "x"],
    [" ", "x", " ", " ", " ", "x", "x", " ", "x", " ", "x", " ", "x", "x", "x", "x", " ", " ", "x", " "],
    ["x", " ", "x", " ", "x", "x", "x", " ", " ", " ", " ", "x", " ", " ", " ", " ", "x", "x", "x", "x"],
    [" ", " ", " ", " ", " ", "x", " ", " ", " ", " ", " ", "x", "x", "x", " ", " ", "x", " ", "x", "x"],
    ["x", "x", " ", "x", "x", "x", " ", " ", " ", " ", "x", " ", " ", " ", " ", "x", " ", "x", " ", "x"],
    [" ", " ", "x", " ", " ", " ", " ", "x", "x", " ", " ", "x", " ", "x", "x", "x", " ", " ", "x", " "],
    [" ", "x", " ", "x", " ", " ", "x", "x", "x", "x", " ", " ", "x", " ", " ", " ", "x", " ", "x", "x"],
    ["x", "x", " ", "x", "x", " ", "x", " ", " ", " ", "x", " ", " ", "x", "x", " ", "x", "x", " ", "x"]
]


def draw_field():
    """
    A handler function that draws a field represented by a two-dimensional list
    into a game window. This function is called whenever the game engine requests
    a screen update.
    """
    sl.clear_window()
    sl.begin_sprite_draw()
    for y, colums in enumerate(planet):
        for x, rows in enumerate(colums):
            sl.prepare_sprite(planet[y][x], x * 40, y * 40)
    sl.draw_sprites()

def floodfill(arr, x, y):
    """
    Marks previously unknown connected areas as safe, starting from the given
    x, y coordinates.
    """
    if (arr[y][x] == "x"):
        return

    indices = []
    indices.append([y, x])
    for val in indices:
        print(val)

        if val[1] == 0 and val[0] == 0 and len(arr) > 1:
            x_1 = 0
            y_1 = 0
            print("STATE 1")
            for coll in arr[0:2]:
                for row in coll[0:2]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] != "0":
                        arr[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    x_1 += 1
                y_1 += 1
                x_1 = 0


        elif val[1] == len(arr[0]) - 1 and val[0] == 0:
            x_1 = val[1] - 1
            y_1 = 0
            print("STATE 2")
            for coll in arr[0:2]:
                for row in coll[val[1]-1:val[1]+1]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] != "0":
                        arr[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    x_1 += 1
                y_1 += 1
                x_1 = val[1] - 1


        elif val[1] == 0 and val[0] == len(arr)-1:
            x_1 = 0
            y_1 = len(arr)-2
            print("STATE 3")
            for coll in arr[len(arr)-2:len(arr)]:
                for row in coll[0:2]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] != "0":
                        arr[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    x_1 += 1
                y_1 += 1
                x_1 = 0


        elif val[0] == len(arr)-1 and val[1] == len(arr[0])-1:
            x_1 = len(arr[0]) - 2
            y_1 = len(arr) - 2
            print("STATE 4")
            for arr_i in arr[len(arr)-2:len(arr)]:
                for arr_j in arr_i[len(arr_i)-2:len(arr_i)]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] != "0":
                        arr[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    x_1 += 1
                y_1 += 1
                x_1 = len(arr[0]) - 2

        elif val[1] > 0 and val[1] < len(arr[0]) - 1 and val[0] == 0:
            x_1 = val[1] - 1
            y_1 = 0
            print("STATE 5")
            for i in arr[val[0]:val[0]+2]:
                for j in i[val[1] - 1:val[1] + 2]:
                    print("CHECK TILE ", y_1 ,x_1)
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] != "0":
                        arr[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    x_1 += 1
                y_1 += 1
                x_1 = val[1] - 1

        elif val[1] > 0 and val[1] < len(arr[0]) - 1 and val[0] == len(arr) - 1:
            x_1 = val[1] - 1
            y_1 = val[0] - 1
            print("STATE 6")
            for i in arr[val[0]-1:val[0]+1]:
                for j in i[val[1]-1:val[1]+2]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] != "0":
                        arr[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    x_1 += 1
                y_1 += 1
                x_1 = val[1] - 1

        elif val[1] == 0 and val[0] > 0 and val[0] < len(arr) - 1:
            x_1 = val[1]
            y_1 = val[0] - 1
            print("STATE 7")
            for i in arr[val[0]-1:val[0]+2]:
                for j in i[val[1]:val[1]+2]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] != "0":
                        arr[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    x_1 += 1
                y_1 += 1
                x_1 = val[1]

        elif val[1] == len(arr[0]) - 1 and val[0] > 0 and val[0] < len(arr) - 1:
            x_1 = val[1] - 1
            y_1 = val[0] - 1
            print("STATE 8")
            for i in arr[val[0]-1:val[0]+2]:
                for j in i[val[1]-1:val[1]+1]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] != "0":
                        arr[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    x_1 += 1
                y_1 += 1
                x_1 = val[1] - 1

        elif val[1] > 0 and val[1] < len(arr[0]) - 1 and val[0] > 0 and val[0] < len(arr) - 1:
            x_1 = val[1] - 1
            y_1 = val[0] - 1
            print("STATE 9")
            for i in arr[val[0]-1:val[0]+2]:
                for j in i[val[1]-1:val[1]+2]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] != "0":
                        arr[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    x_1 += 1
                y_1 += 1
                x_1 = val[1] - 1

def main():
    """
    Loads the game graphics, creates a game window, and sets a draw handler
    """
    sl.load_sprites("spritet")
    sl.create_window(len(planet[0]) * 40, len(planet) * 40)
    sl.set_draw_handler(draw_field)
    sl.start()

if __name__ == "__main__":

    floodfill(planet, 6, 0)
    for i in planet:
        print(i)
    #main()
