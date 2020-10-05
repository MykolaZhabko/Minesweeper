import sweeperlib as sl

def floodfill(arr, arr2, x, y):
    """
    arr = it is a list with mines and numbers around mines
        and if there is zero mines around tile it is marked as - " "
    arr2 = it is a list which is drawn on playground(game window)

    This is floodfill method which replace all tiles which is " " to tiles "0" in arr and copying it to arr2
    and also copying tiles which is around "0" tile to arr2
    """
    if (arr[y][x] == "x"):
        return

    indices = []
    indices.append([y, x])
    for val in indices:
        #print(val)

        if val[1] == 0 and val[0] == 0 and len(arr) > 1:
            x_1 = 0
            y_1 = 0
            #print("STATE 1")
            for coll in arr[0:2]:
                for row in coll[0:2]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] == " ":
                        arr[y_1][x_1] = "0"
                        arr2[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    else:
                        arr2[y_1][x_1] = arr[y_1][x_1]

                    x_1 += 1
                y_1 += 1
                x_1 = 0


        elif val[1] == len(arr[0]) - 1 and val[0] == 0:
            x_1 = val[1] - 1
            y_1 = 0
            #print("STATE 2")
            for coll in arr[0:2]:
                for row in coll[val[1]-1:val[1]+1]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] == " ":
                        arr[y_1][x_1] = "0"
                        arr2[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    else:
                        arr2[y_1][x_1] = arr[y_1][x_1]
                    x_1 += 1
                y_1 += 1
                x_1 = val[1] - 1


        elif val[1] == 0 and val[0] == len(arr)-1:
            x_1 = 0
            y_1 = len(arr)-2
            #print("STATE 3")
            for coll in arr[len(arr)-2:len(arr)]:
                for row in coll[0:2]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] == " ":
                        arr[y_1][x_1] = "0"
                        arr2[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    else:
                        arr2[y_1][x_1] = arr[y_1][x_1]
                    x_1 += 1
                y_1 += 1
                x_1 = 0


        elif val[0] == len(arr)-1 and val[1] == len(arr[0])-1:
            x_1 = len(arr[0]) - 2
            y_1 = len(arr) - 2
            #print("STATE 4")
            for arr_i in arr[len(arr)-2:len(arr)]:
                for arr_j in arr_i[len(arr_i)-2:len(arr_i)]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] == " ":
                        arr[y_1][x_1] = "0"
                        arr2[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    else:
                        arr2[y_1][x_1] = arr[y_1][x_1]
                y_1 += 1
                x_1 = len(arr[0]) - 2

        elif val[1] > 0 and val[1] < len(arr[0]) - 1 and val[0] == 0:
            x_1 = val[1] - 1
            y_1 = 0
            #print("STATE 5")
            for i in arr[val[0]:val[0]+2]:
                for j in i[val[1] - 1:val[1] + 2]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] == " ":
                        arr[y_1][x_1] = "0"
                        arr2[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    else:
                        arr2[y_1][x_1] = arr[y_1][x_1]
                    x_1 += 1
                y_1 += 1
                x_1 = val[1] - 1

        elif val[1] > 0 and val[1] < len(arr[0]) - 1 and val[0] == len(arr) - 1:
            x_1 = val[1] - 1
            y_1 = val[0] - 1
            #print("STATE 6")
            for i in arr[val[0]-1:val[0]+1]:
                for j in i[val[1]-1:val[1]+2]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] == " ":
                        arr[y_1][x_1] = "0"
                        arr2[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    else:
                        arr2[y_1][x_1] = arr[y_1][x_1]
                    x_1 += 1
                y_1 += 1
                x_1 = val[1] - 1

        elif val[1] == 0 and val[0] > 0 and val[0] < len(arr) - 1:
            x_1 = val[1]
            y_1 = val[0] - 1
            #print("STATE 7")
            for i in arr[val[0]-1:val[0]+2]:
                for j in i[val[1]:val[1]+2]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] == " ":
                        arr[y_1][x_1] = "0"
                        arr2[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    else:
                        arr2[y_1][x_1] = arr[y_1][x_1]
                    x_1 += 1
                y_1 += 1
                x_1 = val[1]

        elif val[1] == len(arr[0]) - 1 and val[0] > 0 and val[0] < len(arr) - 1:
            x_1 = val[1] - 1
            y_1 = val[0] - 1
            #print("STATE 8")
            for i in arr[val[0]-1:val[0]+2]:
                for j in i[val[1]-1:val[1]+1]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] == " ":
                        arr[y_1][x_1] = "0"
                        arr2[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    else:
                        arr2[y_1][x_1] = arr[y_1][x_1]
                    x_1 += 1
                y_1 += 1
                x_1 = val[1] - 1

        elif val[1] > 0 and val[1] < len(arr[0]) - 1 and val[0] > 0 and val[0] < len(arr) - 1:
            x_1 = val[1] - 1
            y_1 = val[0] - 1
            #print("STATE 9")
            for i in arr[val[0]-1:val[0]+2]:
                for j in i[val[1]-1:val[1]+2]:
                    if arr[y_1][x_1] != "x" and arr[y_1][x_1] == " ":
                        arr[y_1][x_1] = "0"
                        arr2[y_1][x_1] = "0"
                        indices.append([y_1, x_1])
                    else:
                        arr2[y_1][x_1] = arr[y_1][x_1]
                    x_1 += 1
                y_1 += 1
                x_1 = val[1] - 1
