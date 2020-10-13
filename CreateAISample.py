import CreateSample as sample
import requests
import json
if __name__ == "__main__":
    origin, order, swap, step = sample.CreateAnswerOnlyBySwapSample()
    i = 0
    dst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    map = {}
    for i in order:
        map[i] = 1
    print(map)
    m = 0
    for m in range(0, len(dst)):
        if dst[m] not in map.keys():
            break
    p = []
    for i in range(0,9,3):
        temp = []
        for j in range(i,i+3):
            temp.append(order[j])
        p.append(temp)
    print(m+1)
    print(p)
    data = {
        "teamid": 19,
        "data":{
            "letter":"g",
            "exclude": m+1,
            "challenge":p,
            "step":step,
            "swap":swap
        },
        "token":'6c74b0ea-c164-4efb-88ec-334fb268ee64'
    }
    url = 'http://47.102.118.1:8089/api/challenge/create'
    headers = {'Content-Type': 'application/json'}
    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    # 输出提交返回的信息
    print(res.text)