from queue import PriorityQueue
import cv2
import requests
import base64
import os
import json

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
map_cost = {}# 确定最小估价值是否唯一
x = [0, 0, 0, 1, 1, 1, 2, 2, 2]
y = [0, 1, 2, 0, 1, 2, 0, 1, 2]
bfs_flag = 0 # 标记位，确认最小估价值是否唯一

# node类表示当前的局势以及操作序列还有移动步数
class node(object):
    def __init__(self, num, step, zeroPos, des, operation, swap, flag):
        # num指当前局势，cost表示用于A*算法的估价函数值，step指移动步数，des指目标状态，operation指操作序列，swap记录自由交换的位置，flag指是否已经被强制交换
        self.num = num
        self.step = step
        self.zeroPos = zeroPos
        self.des = des
        self.Init_zeroPos = self.get_zeroPos()
        self.cost = self.setCost()
        self.operation = operation
        self.swap = swap
        self.flag = flag

    def __lt__(self, other):
        # 重载运算符，优先队列用得到
        if self.flag == other.flag:
            if bfs_flag == 1:
                return self.step < other.step
            else:
                return self.cost < other.cost
        else:
            return self.flag < other.flag

    def get_zeroPos(self):
        for i in range(9):
            if self.des[i] == 0:
                return i

    def setCost(self):  # A*算法要用到的估价函数
        c = 0
        for i in range(9):
            if self.num[i] != 0:
                c += abs(int(i / 3) - x[self.num[i] - 1]) + abs(int(i % 3) - y[self.num[i] - 1])
            else:
                c += abs(int(i / 3) - int(self.Init_zeroPos / 3)) + abs(int(i % 3) - self.Init_zeroPos % 3)
        return c + self.step


def CostCount(num, des, step):  # 估价函数
    c = 0
    k = 0
    for k in range(9):
        if des[k] == 0:
            break
    for i in range(9):
        if num[i] != 0:
            c += abs(int(i / 3) - x[num[i] - 1]) + abs(int(i % 3) - y[num[i] - 1])
        else:
            c += abs(int(i / 3) - int(k / 3)) + abs(int(i % 3) - int(k % 3))
    return c + step


def check(map, des):  # 校对当前局势是否有解

    cnt1 = 0
    cnt2 = 0
    for i in range(0, len(map)):
        for j in range(0, i):
            if map[j] > map[i] and map[i] != 0:
                cnt1 = cnt1 + 1
    for i in range(0, len(des)):
        for j in range(0, i):
            if des[j] > des[i] and des[i] != 0:
                cnt2 = cnt2 + 1
    return (cnt1 % 2) == (cnt2 % 2)


def getRightChange(order, des, step,cost_swap):  # 获得到保证交换后局势有解且估价函数最小的自由交换

    cost = int(10000000)
    pos1 = 0
    pos2 = 0
    for i in range(0, len(order)):
        for j in range(i + 1, len(order)):
            order[i], order[j] = order[j], order[i]
            # print(order)
            tempCost = CostCount(order, des, step)
            # print(tempCost)
            if tempCost < cost and check(order, des):
                cost = tempCost
                pos1 = i
                pos2 = j
            order[i], order[j] = order[j], order[i]
    if cost_swap > cost:
        cost_swap = cost
    if cost not in map_cost:
        map_cost[cost] = 1  #对于每次最佳交换我们都要记录他的估价值
    else:
        map_cost[cost] += 1
    return pos1, pos2,cost_swap


def check_list(dest, now):  # 校对当前局势是否为目标局势
    for i in range(9):
        if dest[i] != now[i]:
            return False
    return True


def getOrder(temp, operation, delta, m, zeroPos):
    # 对于无解情况出现在强制交换要求的步数前的node我们要强行添加白块来回移动的步数使其达到强制交换要求
    for i in range(delta):
        if i % 2 == 0:
            operation.append(reverse[m])
        else:
            operation.append(m)
    if delta % 2:
        temp[zeroPos], temp[changeId[zeroPos][change[reverse[m]]]] = temp[changeId[zeroPos][change[reverse[m]]]], temp[
            zeroPos]
        zeroPos = changeId[zeroPos][change[reverse[m]]]
    return temp, operation, zeroPos


# A*算法搜索到达目标局势的最短步数操作
def bfsHash(start, zeroPos, des, step, change_position,cost_swap):
    # 之前采取的是哈希表，由于哈希表会存在冲突问题，然后采取O（n）的后移操作，在面对需要用到大量操作数的时候
    # 算法效率上就会大幅度降低，所以最后用回python自带的字典
    que = PriorityQueue()
    que2 = PriorityQueue()
    first = node(start, 0, zeroPos, des, [], [], 0)
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
        # print(list_to_string(tempN.operation))
        temp = tempN.num.copy()
        pos = tempN.zeroPos
        if check_list(des, temp):  # 若为目标局势则跳出
            return tempN
        if len(tempN.operation) == step and tempN.flag == 0:  # 符合强制交换条件，开始执行变换操作
            temp = tempN.num.copy()
            if change_position[0] - 1 == pos:
                pos = change_position[1] - 1
            elif change_position[1] - 1 == pos:
                pos = change_position[0] - 1
            temp[change_position[0] - 1], temp[change_position[1] - 1] = temp[change_position[1] - 1], temp[
                change_position[0] - 1]
            swap = []
            if not check(temp, des):
                pos1, pos2,cost_swap= getRightChange(temp, des, tempN.step,cost_swap)
                if pos1 == pos:
                    pos = pos2
                elif pos2 == pos:
                    pos = pos1
                temp[pos1], temp[pos2] = temp[pos2], temp[pos1]
                swap.append(pos1 + 1)
                swap.append(pos2 + 1)
            s = ""
            for i in temp:
                s += str(i)
            mymap[s] = 1
            operation = tempN.operation.copy()
            temp_step = tempN.step
            tempN = node(temp, temp_step, pos, des, operation, swap, 1)
            if cost_swap > tempN.cost:
                cost_swap = tempN.cost
            if tempN.cost not in map_cost:
                map_cost[tempN.cost] = 1  # 对于每次最佳交换我们都要记录他的估价值
            else:
                map_cost[tempN.cost] += 1
            if check_list(des, temp):  # 若交换后刚好为目标局势那就直接返回
                operation.append(' ')  # 应测试组要求加上一个字符防止评测判断不到交换这一步
                tempN = node(temp, temp_step, pos, des, operation, swap, 1)
                return tempN
            else:
                que2.put(tempN)# 把所有交换后的节点都放在que2队列
                continue

        # cnt用来对付无解情况，四个方向（cnt=4）都无路可走就为无解情况。
        # 如果这个情况出现在强制交换要求的步数前那么我们要添加“反复横跳”操作使得他达到强制交换要求的步数
        cnt = 0
        for i in range(4):
            if changeId[pos][i] != -1:
                pos = tempN.zeroPos
                temp = tempN.num.copy()
                temp[pos], temp[changeId[pos][i]] = temp[changeId[pos][i]], temp[pos]
                s = ""
                for j in temp:
                    s += str(j)
                if s not in mymap:
                    mymap[s] = 1
                    operation = tempN.operation.copy()
                    operation.append(dir[i])
                    temp_step = tempN.step + 1
                    temp_num = temp
                    tempM = node(temp_num, temp_step, changeId[pos][i], des, operation, tempN.swap, tempN.flag)
                    que.put(tempM)
                else:
                    cnt += 1
            else:
                cnt += 1

        if cnt == 4 and tempN.step < step:  # 进行“反复横跳”操作
            # 对于在强制交换前就发现无解的情况，我们直接处理成白块来回摆动的情况让他直接到达目标步数
            temp = tempN.num.copy()
            operation = tempN.operation.copy()
            m = operation[len(operation) - 1]
            delta = step - len(operation)
            pos = tempN.zeroPos
            temp, operation, pos = getOrder(temp, operation, delta, m, pos)  # 添加“反复横跳”的操作序列
            tempM = node(temp, step, pos, des, operation, tempN.swap, tempN.flag)
            que.put(tempM)
    if not que2.empty():
        #print(1)
        return bfsAfterSwap(que2,des,mymap,cost_swap)

def bfsAfterSwap(que,des,mymap,cost_swap):
    #print(1)
    global bfs_flag
    if map_cost.get(cost_swap) > 1:
        bfs_flag = 1
    print(bfs_flag)
    #然后就是对着交换后的队列继续bfs
    while not que.empty():
        tempN = que.get()
        # print(list_to_string(tempN.operation))
        temp = tempN.num.copy()
        pos = tempN.zeroPos
        if check_list(des, temp):  # 若为目标局势则跳出
            return tempN
        for i in range(4):
            if changeId[pos][i] != -1:
                pos = tempN.zeroPos
                temp = tempN.num.copy()
                temp[pos], temp[changeId[pos][i]] = temp[changeId[pos][i]], temp[pos]
                s = ""
                for j in temp:
                    s += str(j)
                if s not in mymap:
                    mymap[s] = 1
                    operation = tempN.operation.copy()
                    operation.append(dir[i])
                    temp_step = tempN.step + 1
                    temp_num = temp
                    tempM = node(temp_num, temp_step, changeId[pos][i], des, operation, tempN.swap, tempN.flag)
                    que.put(tempM)


def getDestImageOrder(order):  # 得确定哪块空了，将其标号为0表示白色块
    dst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    map = {}
    for i in order:
        map[i] = 1
    # print(map)
    for m in range(0, len(dst)):
        if dst[m] not in map.keys():
            dst[m] = 0
            break
    return dst

def PostAnswer(post_id, operation, swap, teamid, token):  # 提交答案
    url = 'http://47.102.118.1:8089/api/challenge/submit'
    str1 = ''
    for i in operation:
        str1 += i
    headers = {'Content-Type': 'application/json'}
    data = {
        "uuid": str(post_id),
        "teamid": teamid,
        "token" : token,
        "answer": {
            "operations": str1,
            "swap": swap
        }
    }
    print(json.dumps(data))
    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    # 输出提交返回的信息
    print(res.text)

# 拿到我们的图以及其他要求信息，与之前预被处理成九宫格的36个正常字符图进行比对并标号
def getProblemImageOrder(teamid, uuid, token):
    # 拿图
    print(uuid)
    url = 'http://47.102.118.1:8089/api/challenge/start/' + uuid
    data = {
        "teamid": teamid,
        "token": token
    }
    headers = {'Content-Type': 'application/json'}
    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    #print(res.text)
    dict = res.json()
    #print(dict)
    target = base64.b64decode(dict['data']['img'])
    file = open('json_img_test.jpg', 'wb')
    file.write(target)
    file.close()

    # 切图
    img = cv2.imread('json_img_test.jpg')
    height = img.shape[0]
    width = img.shape[1]
    single_height = height / 3
    single_width = width / 3
    for i in range(3):
        for j in range(3):
            dst = img[int(i * single_height):int((i + 1) * single_height),
                  int(j * single_width):int((j + 1) * single_width)]
            # img_list.append(dst)
            # 在本目录生成被分割的图片
            cv2.imwrite(str(i * 3 + j) + '.jpg', dst)

    # 开始对号入座
    h = 0
    init_path = 'cut_chars'
    for file in os.listdir(init_path):
        path = init_path + '\\' + str(file)
        count = 0
        for img_name in os.listdir(path):
            # print(path + '\\' + str(img_name))
            img = cv2.imread(path + '\\' + str(img_name))
            # for item in img_list:
            #     # result = not np.any(cv2.subtract(item, img))
            #     if (item == img).all():
            #         count = count + 1
            #         break
            for i in range(9):
                temp_path = str(i) + '.jpg'
                temp = cv2.imread(temp_path)
                if (temp == img).all():
                    count = count + 1
                    break
            h = h + 1
            if h == 3:
                break
            # print(count)
        if count >= 2:
            print(file)
            break

    order = []
    path1 = 'cut_chars' + '\\' + str(file) + '\\'
    for k in range(9):
        sum = 0
        path2 = str(k) + '.jpg'
        # print(path2)
        img2 = cv2.imread(path2)
        for i in range(1, 4, 1):
            for j in range(1, 4, 1):
                temp = path1 + str(i) + ',' + str(j) + '.jpg'
                # print(temp)
                img1 = cv2.imread(temp)
                if (img1 == img2).all():
                    sum = (i - 1) * 3 + j
        if sum > 0:
            order.append(sum)
        else:
            order.append(0)

    return order, dict['data']['step'], dict['data']['swap'], dict['uuid']

if __name__ == '__main__':
    res = requests.get('http://47.102.118.1:8089/api/team/problem/19')
    all = res.json()
    for m in range(0,len(all)):
        flag = 0
        map_cost = {}
        if all[m]['author'] == 19:
            continue
        uuid = all[m]['uuid']
        order, limit_step, change_position, post_id = getProblemImageOrder(19,uuid,'6c74b0ea-c164-4efb-88ec-334fb268ee64')
        # 将所需信息输入到txt文本中方便debug和手模数据
        str1 = 'ans' + str(m) +'.txt'
        f = open(str1, 'w', encoding='UTF-8')
        f.write(str(order))
        f.write('\n')
        f.write(str(limit_step))
        f.write('\n')
        f.write(str(change_position))
        f.write('\n')
        f.write(str(post_id))
        f.write('\n')
        dst = getDestImageOrder(order)

        f.write(str(dst))
        f.write('\n')
        # 确定白块位置
        for k in range(9):
            if order[k] == 0:
                break
        # 开始搜索
        b = bfsHash(order, k, dst, limit_step, change_position,1000)
        f.write(str(b.step))
        f.write('\n')
        f.write(str(b.operation))
        f.write('\n')
        f.write(str(b.swap))
        f.write('\n')
        f.close()

        # 提交结果
        PostAnswer(post_id, b.operation, b.swap,19,'6c74b0ea-c164-4efb-88ec-334fb268ee64')
