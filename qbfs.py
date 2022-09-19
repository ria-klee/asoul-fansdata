from pygal.style import Style
import pygal
import re
import linecache
from apscheduler.schedulers.background import BlockingScheduler

scheduler = BlockingScheduler()
custom_style = Style(colors=('#9AC8E2', '#BD7D74', '#B8A6D9', '#E799B0',
                             '#576690', '#FC966E'))


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
    fensi, bh, cya, cyb, cyc, cyd, cye, cyg = ([] for i in range(8))
    fname = 'asoulbh-h.txt'
    linecache.clearcache()
    line_count = get_line_count(fname)
    line_count = line_count - 143
    for i in range(144):
        last_line = linecache.getline(fname, line_count)
        fs = re.findall(r'[(](.*?)[)]', last_line, re.S)
        fensi.extend(fs)
        line_count += 1
    for x in range(0, 288, 2):
        fsbh = int(fensi[x])
        bh.append(fsbh)
    for y in range(0, 144, 6):
        cy = bh[y:y + 6]
        cya.append(cy[0])
        cyb.append(cy[1])
        cyc.append(cy[2])
        cyd.append(cy[3])
        cye.append(cy[4])
        cyg.append(cy[5])
    view = pygal.Line(print_values=False, style=custom_style)
    # 图表名
    view.title = '昨日粉丝数量时间段变化'
    # 添加数据
    view.x_title = '时间点(1指00:00-01:00)'
    view.y_title = '关注人数'
    view.x_labels = map(str, range(1, 25))
    view.add('向晚', list(map(int, cya)))
    view.add('贝拉', list(map(int, cyb)))
    view.add('珈乐', list(map(int, cyc)))
    view.add('嘉然', list(map(int, cyd)))
    view.add('乃琳', list(map(int, cye)))
    view.add('官号', list(map(int, cyg)))
    view.render_to_file('fs.svg')


# func()
job = scheduler.add_job(func,
                        'cron',
                        hour='0',
                        minute='0',
                        second='20',
                        timezone='Asia/Shanghai',
                        misfire_grace_time=None,
                        coalesce=True)  # 每隔5s执行一次func
scheduler.start()
