import json
import requests
import time
if __name__ == '__main__':
    res = requests.get('http://47.102.118.1:8089/api/challenge/list')
    all = res.json()
    f = open('ProblemRank.txt', 'w', encoding='UTF-8')
    for m in range(len(all)):
        time.sleep(1)
        if all[m]['author'] == 19:
            continue
        k = all[m]['uuid']
        check = 'http://47.102.118.1:8089/api/challenge/record/' + k
        res = requests.get(check)
        f.write(str(all[m]['author']))
        f.write('\n')
        dict = res.json()
        for k in range(len(dict)):
            f.write(str(dict[k]))
            f.write('\n')