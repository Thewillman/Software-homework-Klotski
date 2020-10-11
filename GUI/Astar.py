from queue import PriorityQueue
import re
import copy

changeId = [
    [-1, -1, 3, 1],
    [-1, 0, 4, 2],
    [-1, 1, 5, -1],
    [0, -1, 6, 4],
    [1, 3, 7, 5],
    [2, 4, 8, -1],
    [3, -1, -1, 7],
    [4, 6, -1, 8],
    [5, 7, -1, -1]
]  # 九个位置能上下左右位移到的图片位置
reverse = {'w': 's', 's': 'w', 'a': 'd', 'd': 'a'}
change = {'w': 0, 'a': 1, 's': 2, 'd': 3}
dir = ['w', 'a', 's', 'd']



# node类表示当前的局势以及操作序列还有移动步数
class node(object):
    def __init__(self, num, step, zeroPos, des, operation):
        # num指当前局势，cost表示用于A*算法的估价函数值，step指移动步数，des指目标状态，operation指操作序列，swap记录自由交换的位置，flag指是否已经被强制交换
        self.num = num
        self.step = step
        self.zeroPos = zeroPos
        self.des = des
        self.x1 = [0, 0, 0, 1, 1, 1, 2, 2, 2]
        self.y1 = [0, 1, 2, 0, 1, 2, 0, 1, 2]
        self.Init_zeroPos = self.get_zeroPos()
        self.cost = self.setCost()
        self.operation = operation


    def __lt__(self, other):
        # 重载运算符，优先队列用得到
        return self.cost < other.cost

    def get_zeroPos(self):
        for i in range(9):
            if self.des[i] == '0':
                return i

    def setCost(self):  # A*算法要用到的估价函数
        c = 0
        # print(self.Init_zeroPos)
        for i in range(9):
            if self.num[i] != 0:
                c += abs(int(i / 3) - self.x1[self.num[i]-1]) + abs(int(i%3) - self.y1[self.num[i]-1])
            else:
                c += abs(int(i / 3) - int(self.Init_zeroPos/3)) + abs(int(i%3) - int(self.Init_zeroPos%3))
        return c + self.step

def check_list(dest, now):  # 校对当前局势是否为目标局势
    str1 = ""
    for i in now:
        str1 += str(i)
    return str1 == dest

def list_to_string(list):
    result = ''
    for item in list:
        result = result + str(item)
    return result

# A*算法搜索到达目标局势的最短步数操作
def bfsHash(start, zero_row1,zero_column1, des, degree):
    # 之前采取的是哈希表，由于哈希表会存在冲突问题，然后采取O（n）的后移操作，在面对需要用到大量操作数的时候
    # 算法效率上就会大幅度降低，所以最后用回python自带的字典
    que = PriorityQueue()
    zeroPos = zero_row1*degree + zero_column1
    first = node(start, 0, zeroPos, des,[])
    que.put(first)
    mymap = {}
    s = ""
    for i in start:
        s += str(i)
    mymap[s] = 1
    m = -1
    # 开始搜索
    while not que.empty():
        tempN = que.get()
        temp = tempN.num.copy()
        pos = tempN.zeroPos

        if check_list(des, temp):  # 若为目标局势则跳出
            write_order(list_to_string(tempN.operation))
            return change(list_to_string(tempN.operation))
        for i in range(4):
            if changeId[pos][i] != -1:
                pos = tempN.zeroPos
                temp = tempN.num.copy()
                temp[pos], temp[changeId[pos][i]] = temp[changeId[pos][i]], temp[pos]
                # print(k)
                s = ""
                for j in temp:
                    s += str(j)
                if s not in mymap:
                    #    print(1)
                    mymap[s] = 1
                    operation = tempN.operation.copy()
                    operation.append(dir[i])
                    temp_step = tempN.step + 1
                    temp_num = temp
                    tempM = node(temp_num, temp_step, changeId[pos][i], des, operation)
                    que.put(tempM)

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