# 在对问题图片和目标图片都进行编号后我们可以发现，题目要我们解决的本质上其实是变种版本的八数码问题
# 所以我们在生成测试样例只需要对123456789这个序列进行操作即可，图片处理操作基本一致这里不做改变
from queue import PriorityQueue
import random
import AstarFind as answer
import AstarFind2 as answer2
import AstarFind3 as answer3
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

# 用于对付unittest
def showmap(temp):
    for i in range(0, len(temp), 3):
        str1 = str(temp[i]) + ' ' + str(temp[i + 1]) + ' ' + str(temp[i + 2])
        print(str1)


def SampleSolve(order, origin, swap, swapStep):
    # 确定白块位置
    for k in range(9):
        if order[k] == 0:
            break
    # 开始搜索
    b = answer.bfsHash(order, k, origin, swapStep, swap)
    print('跑出来了！')
    print('初始局势：')
    showmap(order)
    print('目标局势：')
    showmap(origin)
    print('强制交换步数：', swapStep)
    print('强制交换位置：', swap)
    print('操作序列：', b.operation)
    print('自由交换：', b.swap)
    return b.operation

def SampleSolve2(order, origin, swap, swapStep):
    # 确定白块位置
    for k in range(9):
        if order[k] == 0:
            break
    # 开始搜索
    b = answer2.bfsHash(order, k, origin, swapStep, swap)
    print('跑出来了！')
    print('初始局势：')
    showmap(order)
    print('目标局势：')
    showmap(origin)
    print('强制交换步数：', swapStep)
    print('强制交换位置：', swap)
    print('操作序列：', b.operation)
    print('自由交换：', b.swap)
    return b.operation

def SampleSolve3(order, origin, swap, swapStep):
    # 确定白块位置
    for k in range(9):
        if order[k] == 0:
            break
    # 开始搜索
    b = answer3.bfsHash(order, k, origin, swapStep, swap)
    print('跑出来了！')
    print('初始局势：')
    showmap(order)
    print('目标局势：')
    showmap(origin)
    print('强制交换步数：', swapStep)
    print('强制交换位置：', swap)
    print('操作序列：', b.operation)
    print('自由交换：', b.swap)
    return b.operation

def NormalRun(start, zeroPos, des):  # 解决非交换位置的八数码问题
    first = answer.node(start, 0, zeroPos, des, [], [], 0)
    que = PriorityQueue()
    que.put(first)
    mymap = {}
    s = ""
    for i in start:
        s += str(i)
    mymap[s] = 1
    # print(start)
    # print(des)
    # print(answer.check_list(start,des))
    # 开始搜索
    while not que.empty():
        tempN = que.get()
        temp = tempN.num.copy()
        step = tempN.step
        # print(temp)
        # print(des)
        # print(answer.check_list(des, temp))
        pos = tempN.zeroPos
        if answer.check_list(des, temp):  # 若为目标局势则跳出
            return step
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
                    tempM = answer.node(temp_num, temp_step, changeId[pos][i], des, operation, tempN.swap, tempN.flag)
                    que.put(tempM)
    print(1)


def NoAnswerRun(start, zeroPos, des):  # 找出Astar判出无解的最长步数
    first = answer.node(start, 0, zeroPos, des, [], [], 0)
    que = PriorityQueue()
    que.put(first)
    mymap = {}
    s = ""
    for i in start:
        s += str(i)
    mymap[s] = 1
    que = PriorityQueue()
    # 开始搜索
    noAnswerstep = 0
    while not que.empty():
        tempN = que.get()
        temp = tempN.num.copy()
        pos = tempN.zeroPos
        if answer.check_list(des, temp):  # 若为目标局势则跳出
            return tempN.step
        cnt = 0
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
                    tempM = answer.node(temp_num, temp_step, changeId[pos][i], des, operation, tempN.swap, tempN.flag)
                    que.put(tempM)
                else:
                    cnt += 1
            else:
                cnt += 1
        if cnt == 4:
            noAnswerstep = max(noAnswerstep, tempN.step)
    return noAnswerstep


def CreateNormalSample():
    # 正常的变种八数码问题随机生成的样例
    # 首先随机挖一块图片作白块
    origin = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    k = random.randint(0, 8)
    origin[k] = 0
    # 随机交换两个块
    order = origin.copy()
    swap = []
    k1 = random.randint(0, 8)
    k2 = random.randint(0, 8)
    swap.append(k1+1)
    swap.append(k2+1)
    if k == k1:
        k = k2
    elif k == k2:
        k = k1
    order[k1], order[k2] = order[k2], order[k1]
    # 随机走500下
    for i in range(500):
        random_num = random.randint(0, 3)
        if changeId[k][random_num] != -1:
            order[k], order[changeId[k][random_num]] = order[changeId[k][random_num]], order[k]
            k = changeId[k][random_num]
    step = 20  # 在主程序跑的过程中我们发现基本最大的步数都是在20步左右
    return origin, order, swap, step


def CreateNoSwapSample():  # 存在解在未交换前就跑出来了
    # 正常随机交换后随机移动若干次
    # 首先随机挖一块图片作白块
    origin = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    k = random.randint(0, 8)
    origin[k] = 0
    order = origin.copy()
    # print(origin)
    # 开始随机移动
    for i in range(500):
        random_num = random.randint(0, 3)
        # print(k)
        if changeId[k][random_num] != -1:
            order[k], order[changeId[k][random_num]] = order[changeId[k][random_num]], order[k]
            k = changeId[k][random_num]
            # print(order)
    # print(answer.check(order,origin))
    shortestStep = NormalRun(order, k, origin)
    print(shortestStep)
    swapStep = shortestStep + random.randint(0, 5)
    swap = []
    k1 = random.randint(0, 8)
    k2 = random.randint(0, 8)
    swap.append(k1+1)
    swap.append(k2+1)
    return origin, order, swap, swapStep


def CreateNoAnswerAfterSwapSample():  # 必须在交换后才有解且Astar存在发现无解的情况在强制交换要求的步数后
    # 直接随机选取两个临近位置的块交换便可无解
    # 首先随机挖一块图片作白块
    origin = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    k = random.randint(0, 8)
    origin[k] = 0
    order = origin.copy()
    while answer.check(origin, order):
        k1 = random.randint(0, 8)
        k2 = random.randint(0, 8)
        if k == k1:
            k = k2
        elif k == k2:
            k = k1
        order[k1], order[k2] = order[k2], order[k1]
    limited_swap = NoAnswerRun(order, k, origin)
    swap = []
    k1 = random.randint(0, 8)
    k2 = random.randint(0, 8)
    swap.append(k1+1)
    swap.append(k2+1)
    if limited_swap:
        swapStep = random.randint(1, limited_swap)
    else:
        swapStep = 0
    return origin, order, swap, swapStep


def CreateNoAnswerBeforeSwapSample():  # 必须在交换后才有解且Astar存在发现无解的情况在强制交换要求的步数前
    # 直接随机选取两个临近位置的块交换便可无解
    # 首先随机挖一块图片作白块
    origin = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    k = random.randint(0, 8)
    origin[k] = 0
    order = origin.copy()
    while answer.check(origin, order):
        k1 = random.randint(0, 8)
        k2 = random.randint(0, 8)
        if k == k1:
            k = k2
        elif k == k2:
            k = k1
        order[k1], order[k2] = order[k2], order[k1]
    limit_step = NoAnswerRun(order, k, origin)
    swap = []
    k1 = random.randint(0, 8)
    k2 = random.randint(0, 8)
    swap.append(k1+1)
    swap.append(k2+1)
    swapStep = max(limit_step + random.randint(1, 10),20)
    return origin, order, swap, swapStep


def CreateOriginMapCheck():  # 原图对比
    origin = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    k = random.randint(0, 8)
    origin[k] = 0
    order = origin.copy()
    step = random.randint(0, 20)
    swap = []
    k1 = random.randint(0, 8)
    k2 = random.randint(0, 8)
    swap.append(k1+1)
    swap.append(k2+1)
    if k == k1:
        k = k2
    elif k == k2:
        k = k1
    return origin, order, swap, step


def CreateFindAnswerAfterSwapSample():  # 交换后马上找到结果
    # 目前没有想到有效的数据创造方法，先用apiget到的样例
    origin = [1, 0, 3, 4, 5, 6, 7, 8, 9]
    order = [4, 1, 7, 5, 6, 9, 3, 8, 0]
    swap = [6, 6]
    swapStep = 5
    return origin, order, swap, swapStep


def CreateAnswerOnlyBySwapSample():  # 一开始交换完就是目标局势
    origin = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    k = random.randint(0, 8)
    origin[k] = 0
    order = origin.copy()
    k1 = k
    while k == k1 or k == k1 + 1:
        k1 = random.randint(0, 7)
    order[k1], order[k1+1] = order[k1+1], order[k1]
    k1 = random.randint(0, 8)
    k2 = random.randint(0, 8)
    swap = []
    if k == k1:
        k = k2
    elif k == k2:
        k = k1
    order[k1], order[k2] = order[k2], order[k1]
    swap.append(k1+1)
    swap.append(k2+1)
    swapStep = 0
    return origin, order, swap, swapStep
