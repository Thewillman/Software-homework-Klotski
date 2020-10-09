import queue
import re
import copy

sdes1 = '123456780'
des1 = [1, 2, 3, 4, 5, 6, 7, 8, 0]
mymap = {}
changeId1 = [
    [-1, -1, 3, 1],
    [-1, 0, 4, 2],
    [-1, 1, 5, -1],
    [0, -1, 6, 4],
    [1, 3, 7, 5],
    [2, 4, 8, -1],
    [3, -1, -1, 7],
    [4, 6, -1, 8],
    [5, 7, -1, -1]
]
wasd = ['w', 'a', 's', 'd']


class node(object):
    def __init__(self, num, step, zeroPos, order, degree):
        self.num = num
        self.step = step
        self.zeroPos = zeroPos
        self.order = order
        self.degree = degree
        self.cost = self.setCost()

    def __lt__(self, other):
        return self.cost < other.cost

    def setCost(self):
        c = 0
        for i in range(self.degree * self.degree):
            if self.num[i] != des1[i]:
                c = c + 1
        return c + self.step

def string_to_list(k):
    list = re.findall('\d', k)
    return list

def list_to_string(list):
    result = ''
    for item in list:
        result = result + str(item)
    return result

def bfsHash(start1, zero_row1, zero_column1, degree1):
    start = copy.deepcopy(start1)
    zero_row = copy.deepcopy(zero_row1)
    zero_column = copy.deepcopy(zero_column1)
    degree = copy.deepcopy(degree1)
    print('astart:', start)
    print('astart:', zero_row)
    print('astart:', zero_column)
    print('astart:', degree)
    zeroPos = zero_row * degree + zero_column
    first = node(start, 0, zeroPos, '', degree)
    que = queue.PriorityQueue()
    while not que.empty():
        que.get()
    mymap.clear()
    que.put(first)
    print(first.order)
    key = list_to_string(start)
    mymap[key] = 1
    if degree == 3:
        while not que.empty():
            tempN = que.get()
            # print(tempN.order)
            temp = tempN.num
            pos = tempN.zeroPos
            for i in range(4):
                if changeId1[pos][i] != -1:
                    temp[pos], temp[changeId1[pos][i]] = temp[changeId1[pos][i]], temp[pos]
                    k = list_to_string(temp)
                    if k == sdes1:
                        write_order(tempN.order + wasd[i])
                        return change(tempN.order + wasd[i])
                    if k not in mymap.keys():
                        list = string_to_list(k)
                        tempM = node(list, tempN.step+1, changeId1[pos][i], tempN.order + wasd[i], degree)
                        que.put(tempM)
                        mymap[k] = 1
                    temp[pos], temp[changeId1[pos][i]] = temp[changeId1[pos][i]], temp[pos]

def write_order(string):
    list = re.findall('[a-z]', string)
    temp = ''
    for i in range(len(list)):
        if list[i] == 'w':
            temp = temp + '第' + str(i + 1) + '步：下' + '\n'
        elif list[i] == 'a':
            temp = temp + '第' + str(i + 1) + '步：右' + '\n'
        elif list[i] == 's':
            temp = temp + '第' + str(i + 1) + '步：上' + '\n'
        else:
            temp = temp + '第' + str(i + 1) + '步：左' + '\n'
    with open('order.txt', 'a') as file_handle:
        file_handle.truncate(0)
        file_handle.write(temp)
        file_handle.close()

def change(string):
    list = re.findall('[a-z]', string)
    walk = []
    for item in list:
        if item == 'w':
            walk.append(1)
        elif item == 'a':
            walk.append(3)
        elif item == 's':
            walk.append(0)
        else:
            walk.append(2)
    return walk

#
# list = [1, 2, 3, 4, 0, 8, 7, 6, 5]
# walklist = bfsHash(list, 1, 1, 3)
# print(walklist)