import linecache
import re
import datetime
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
    fensi = []
    bh = []
    fname = 'asoulbh-h.txt'
    linecache.clearcache()
    line_count = get_line_count(fname)
    # print('num: ', line_count)
    line_count = line_count - 149  # 最后150行
    for p in range(150):
        last_line = linecache.getline(fname, line_count)
        # print(last_line)
        fs = re.findall(r'\d+', last_line, re.S)
        fensi.extend(fs)
        line_count += 1
    # print(fensi)
    for x in range(0, 24, 2):
        fsbh = int(fensi[x + 744]) - int(fensi[x])
        # print(fsbh)
        if fsbh >= 0:
            fsbh = "+" + str(fsbh)
        bh.append(fsbh)
    print(bh)
    # 倒序写入
    with open("day.txt", "r+", encoding='gb2312') as f:
        old = f.read()
        f.seek(0)
        f.write("向晚 粉:" + fensi[744] + "(" + str(bh[0]) + ")" + "舰:" +
                fensi[746] + "(" + str(bh[1]) + ")" + "\n")
        f.write("贝拉 粉:" + fensi[748] + "(" + str(bh[2]) + ")" + "舰:" +
                fensi[750] + "(" + str(bh[3]) + ")" + "\n")
        f.write("嘉然 粉:" + fensi[756] + "(" + str(bh[6]) + ")" + "舰:" +
                fensi[758] + "(" + str(bh[7]) + ")" + "\n")
        f.write("乃琳 粉:" + fensi[760] + "(" + str(bh[8]) + ")" + "舰:" +
                fensi[762] + "(" + str(bh[9]) + ")" + "\n")
        f.write("官号 粉:" + fensi[764] + "(" + str(bh[10]) + ")" + "舰:" +
                fensi[766] + "(" + str(bh[11]) + ")" + "\t" +
                str(datetime.date.today()) + "\n")
        f.write(old)
    # 顺序写入
    with open("asoulbh-d.txt", "a", encoding='utf-8') as f:
        f.write("向晚 粉:" + fensi[744] + "(" + str(bh[0]) + ")" + "舰:" +
                fensi[746] + "(" + str(bh[1]) + ")" + "\n")
        f.write("贝拉 粉:" + fensi[748] + "(" + str(bh[2]) + ")" + "舰:" +
                fensi[750] + "(" + str(bh[3]) + ")" + "\n")
        f.write("珈乐 粉:" + fensi[752] + "(" + str(bh[4]) + ")" + "舰:" +
                fensi[754] + "(" + str(bh[5]) + ")" + "\n")
        f.write("嘉然 粉:" + fensi[756] + "(" + str(bh[6]) + ")" + "舰:" +
                fensi[758] + "(" + str(bh[7]) + ")" + "\n")
        f.write("乃琳 粉:" + fensi[760] + "(" + str(bh[8]) + ")" + "舰:" +
                fensi[762] + "(" + str(bh[9]) + ")" + "\n")
        f.write("官号 粉:" + fensi[764] + "(" + str(bh[10]) + ")" + "舰:" +
                fensi[766] + "(" + str(bh[11]) + ")" + "\t" +
                str(datetime.date.today()) + "\n")


job = scheduler.add_job(func,
                        'cron',
                        hour='0',
                        minute='0',
                        second='10',
                        timezone='Asia/Shanghai',
                        misfire_grace_time=None,
                        coalesce=True)
scheduler.start()