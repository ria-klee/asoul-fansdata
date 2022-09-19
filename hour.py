import datetime
import linecache
import re
import json
import requests
from apscheduler.schedulers.background import BlockingScheduler

scheduler = BlockingScheduler()


def get_line_count(filename):
    count = 0
    with open(filename, 'r', encoding='utf-8') as file:
        while True:
            buffer = file.read(1024 * 1)
            if not buffer:
                break
            count += buffer.count('\n')
    return count


def func():
    # res = requests.get('https://api.bilibili.com/x/web-interface/card?mid=672346917')
    # 应该是没用的...
    # # 打印变量res的响应状态码，以检查请求是否成功
    # # print(res.status_code)
    # while res.status_code != 200:
    #     res = requests.get('https://api.bilibili.com/x/web-interface/card?mid=672346917')
    #     # print(res.status_code)
    #     if res.status_code == 200:
    #         break
    fanss = []
    names = []
    jian = []
    room_id = [
        '22625025', '22632424', '22634198', '22637261', '22625027', '22632157'
    ]
    ruid = [
        '672346917', '672353429', '351609538', '672328094', '672342685',
        '703007996'
    ]
    for i in range(6):
        web = 'https://api.bilibili.com/x/web-interface/card?mid=' + ruid[i]
        data = requests.get(web)
        info = json.loads(data.text)
        fanss.append(info['data']['card']['fans'])
        names.append(info['data']['card']['name'])

        url = "https://api.live.bilibili.com/xlive/app-room/v1/guardTab/topList?roomid=" + room_id[
            i] + "&page=1&ruid=" + \
            ruid[i]
        # print(url)
        headers = {
            'Host': "api.live.bilibili.com",
            'Origin': "https://live.bilibili.com",
            'Referer': f"https://live.bilibili.com/{room_id}",
            'User-Agent':
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            'Cookie': '1'
        }
        re1 = requests.request('get', url, headers=headers).json()
        num = re1['data']['info']['num']  # 获取现役舰长人数
        list_pages = 0  # 列数
        order = 1
        jian.append(num)

        # print(names[i] + " 的粉丝数量为：" + str(fanss[i]) + "\t" + names[i] +" 的舰长数量为：" + str(jian[i]))

        with open("asoul-h.txt", "a", encoding='utf-8') as f:
            f.write(names[i] + " 的粉丝数量为：" + str(fanss[i]) + "\t" + names[i] +
                    " 的舰长数量为：" + str(jian[i]) + "\n")

    fensi = []
    bh = []
    fname = 'asoul-h.txt'
    linecache.clearcache()
    line_count = get_line_count(fname)
    # print('num: ', line_count)
    line_count = line_count - 11  # 最后12行
    for p in range(12):
        last_line = linecache.getline(fname, line_count)
        # print(last_line)
        fs = re.findall(r'\d+', last_line, re.S)
        fensi.extend(fs)
        line_count += 1
    # print(fensi)
    for x in range(0, 11, 2):
        fsbh = int(fensi[x + 12]) - int(fensi[x])
        # print(fsbh)
        if fsbh >= 0:
            fsbh = "+" + str(fsbh)
        bh.append(fsbh)
    for y in range(0, 11, 2):
        jzbh = int(fensi[y + 13]) - int(fensi[y + 1])
        # print(jzbh)
        if jzbh >= 0:
            jzbh = "+" + str(jzbh)
        bh.append(jzbh)
    # print(bh)

    with open("asoulbh-h.txt", "a", encoding='utf-8') as f:
        f.write("向晚 粉:" + fensi[12] + "(" + str(bh[0]) + ")" + "舰:" +
                fensi[13] + "(" + str(bh[6]) + ")" + "\n")
        f.write("贝拉 粉:" + fensi[14] + "(" + str(bh[1]) + ")" + "舰:" +
                fensi[15] + "(" + str(bh[7]) + ")" + "\n")
        f.write("珈乐 粉:" + fensi[16] + "(" + str(bh[2]) + ")" + "舰:" +
                fensi[17] + "(" + str(bh[8]) + ")" + "\n")
        f.write("嘉然 粉:" + fensi[18] + "(" + str(bh[3]) + ")" + "舰:" +
                fensi[19] + "(" + str(bh[9]) + ")" + "\n")
        f.write("乃琳 粉:" + fensi[20] + "(" + str(bh[4]) + ")" + "舰:" +
                fensi[21] + "(" + str(bh[10]) + ")" + "\n")
        f.write("官号 粉:" + fensi[22] + "(" + str(bh[5]) + ")" + "舰:" +
                fensi[23] + "(" + str(bh[11]) + ")" +
                str(datetime.datetime.now()) + "\n")

    fname1 = 'asoulbh-h.txt'
    zong_line = ''
    linecache.clearcache()
    line_count = get_line_count(fname1)
    line_count = line_count - 149
    # print(line_count)
    for p in range(150):
        last_line = linecache.getline(fname1, line_count)
        # print(last_line)
        line_count += 1
        zong_line = zong_line + last_line
    with open("24hour.txt", "w", encoding='gb2312') as f:
        f.write(zong_line)


job = scheduler.add_job(func,
                        'cron',
                        hour='0-23',
                        minute='0',
                        timezone='Asia/Shanghai',
                        misfire_grace_time=None,
                        coalesce=True)  # 整点执行一次func
scheduler.start()
