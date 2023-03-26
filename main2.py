# -*- coding:utf-8 -*-
import multiprocessing
import random
import subprocess
import tkinter
from multiprocessing import Process
import threading

idlock = threading.Lock()

SAMETIME = 4
ITEM = 15
MAXTIME = 30
ELEVATORNUMBERID = [x + 1 for x in range(6)]

LEVELS = [x + 1 for x in range(11)]

id = 0


class Generator:
    def genData(self):
        thisid = 0
        num = random.choice(range(int(ITEM / 2), ITEM,1)) + 1
        sameitem = random.choice(range(SAMETIME)) + 1
        timelimit = random.choice(range(MAXTIME)) + 2
        time = 1
        res = []
        ori = []

        while (time < timelimit and len(res) < num):
            gap = random.random() * (timelimit * 3 / (float(num) / sameitem))
            n = random.choice(range(sameitem)) + 1
            for i in range(n):
                first = random.choice(LEVELS)
                secondrange = [x for x in LEVELS]
                secondrange.remove(first)
                second = random.choice(secondrange)
                thisid += 1
                res.append("[{:.2f}]{}-FROM-{}-TO-{}".format(time, thisid, first, second))
                ori.append({'gap': gap, 'id': thisid, 'from': first, 'to': second, 'n': n})
            time += gap
        return (res, '\n'.join(res), ori)


num = 0

datawrite = threading.Lock()

startGapLock = threading.Lock()

import psutil


def execute_java(ori, jar, conn):
    time.sleep(1)
    cmdjava = ['java', '-jar', "-Xms64m", "-Xmx256m", jar]
    procjava = subprocess.Popen(cmdjava, stdin=subprocess.PIPE, stderr=subprocess.STDOUT,stdout=subprocess.PIPE)
    input = procjava.stdin
    n = 0
    for item in ori:
        if n == 0:
            n = item['n']
            # print(item['gap'])
            time.sleep(item['gap'])
        n -= 1
        input.write("{}-FROM-{}-TO-{}\n".format(item['id'], item['from'], item['to']).encode())
        input.flush()
        # print("{}-FROM-{}-TO-{}".format(item['id'], item['from'], item['to']))
    input.close()

    success = True
    try:
        res,b = procjava.communicate(timeout=40)
    except subprocess.TimeoutExpired:
        procjava.kill()
        res, b = procjava.communicate()
        os.system("TASKKILL /F /T /PID " + str(procjava.pid))
        time.sleep(1)
        while procjava.pid in psutil.pids():
            print(2)
            time.sleep(0.5)
            os.system("TASKKILL /F /T /PID " + str(procjava.pid))
        success = False
    res = res.decode()
    print(res,success)
    conn['res']=res
    conn['success']=success


def safeaddtle(jar):
    if datawrite.acquire():
        data[jar]['tle'] += 1
        datawrite.release()


def safeaddsuccess(jar):
    if datawrite.acquire():
        data[jar]['pass'] += 1
        datawrite.release()


def safeaddre(jar):
    if datawrite.acquire():
        data[jar]['re'] += 1
        datawrite.release()


def safeaddwa(jar):
    if datawrite.acquire():
        data[jar]['fail'] += 1
        datawrite.release()


from importlib import reload

idnow = 0
sp = threading.Semaphore(0)


def check(ori, out):
    for x in ori:
        x['taked'] = False
    elelevel = {x: 1 for x in ELEVATORNUMBERID}
    eletime = {x: 0 for x in ELEVATORNUMBERID}
    eleopen = {x: False for x in ELEVATORNUMBERID}
    eleopentime = {x: 0 for x in ELEVATORNUMBERID}
    elepassenger = {x: [] for x in ELEVATORNUMBERID}
    linenum = 0
    for line in out.split('\n'):
        linenum += 1
        line.strip(' ')
        if line == '':
            continue
        dtime = float(line.split(']')[0][1:])
        things = line.split(']')[1]
        things = things.split('-')
        type = things[0]
        eleid = int(things[-1])
        if not eleid in ELEVATORNUMBERID:
            return 'wa', 'wrong elevator in on' + str(linenum)
        if type == 'ARRIVE':
            if (len(things) != 3):
                return ("wa", "error output on" + str(linenum))
            level = int(things[1])
            if abs(level - elelevel[eleid]) != 1:
                return ('wa', "error move gap on" + str(linenum))
            if (dtime - eletime[eleid] < 0.399):
                return ('wa', "move too fast on line" + str(linenum))
            elelevel[eleid] = level
            eletime[eleid] = dtime
        elif type == 'OPEN':
            if (len(things) != 3):
                return ("wa", "error output on" + str(linenum))
            level = int(things[1])
            if abs(level - elelevel[eleid]) != 0:
                return ('wa', "error move gap on" + str(linenum))
            if (dtime - eletime[eleid] < 0):
                return ('wa', "time error on line" + str(linenum))
            if eleopen[eleid] != False:
                return ('wa', 'reopen on' + str(linenum))
            eleopen[eleid] = True
            eletime[eleid] = dtime
            eleopentime[eleid] = dtime
        elif type == 'CLOSE':
            if (len(things) != 3):
                return ("wa", "error output on" + str(linenum))
            level = int(things[1])
            if abs(level - elelevel[eleid]) != 0:
                return ('wa', "error move gap on" + str(linenum))
            if (dtime - eleopentime[eleid] < 0.399 or dtime < eletime[eleid]):
                return ('wa', "time error on line" + str(linenum))
            if eleopen[eleid] != True:
                return ('wa', 'reclose on' + str(linenum))
            eleopen[eleid] = False
            eletime[eleid] = dtime
        elif type == 'IN':
            if (len(things) != 4):
                return ("wa", "error output on" + str(linenum))
            level = int(things[2])
            passid = int(things[1])
            if abs(level - elelevel[eleid]) != 0:
                return ('wa', "error move gap on" + str(linenum))
            if (dtime - eletime[eleid] < 0):
                return ('wa', "time error on line" + str(linenum))
            filterinput = [x for x in ori if x['id'] == passid]
            if filterinput == []:
                return ('wa', "wrong passenger id on" + str(linenum))
            filterinput = filterinput[0]
            if filterinput['from'] != elelevel[eleid]:
                return ('wa', "take passenger on wrong level on" + str(linenum))
            if filterinput['taked']:
                return ('wa', 'retake passenger on' + str(linenum))
            filterinput['taked'] = True
            elepassenger[eleid].append(passid)
            eletime[eleid] = dtime
        elif type == 'OUT':
            if (len(things) != 4):
                return ("wa", "error output on" + str(linenum))
            level = int(things[2])
            passid = int(things[1])
            if abs(level - elelevel[eleid]) != 0:
                return ('wa', "error move gap on" + str(linenum))
            if (dtime - eletime[eleid] < 0):
                return ('wa', "time error on line" + str(linenum))
            filterinput = [x for x in ori if x['id'] == passid]
            if filterinput == []:
                return ('wa', "wrong passenger id on" + str(linenum))
            filterinput = filterinput[0]
            if (not filterinput['taked']) or (passid not in elepassenger[eleid]):
                return ('wa', 'put ghost passenger on' + str(linenum))
            filterinput['taked'] = False
            elepassenger[eleid].remove(passid)
            eletime[eleid] = dtime
            filterinput['from'] = elelevel[eleid]
        elif type == "IN":
            if (len(things) != 4):
                return ("wa", "error output on" + str(linenum))
            level = int(things[2])
            passid = int(things[1])
            if abs(level - elelevel[eleid]) != 0:
                return ('wa', "error move gap on" + str(linenum))
            if (dtime - eletime[eleid] < 0):
                return ('wa', "time error on line" + str(linenum))
            filterinput = [x for x in ori if x['id'] == passid]
            if filterinput == []:
                return ('wa', "wrong passenger id on" + str(linenum))
            filterinput = filterinput[0]
            if filterinput['taked']:
                return ('wa', 'retake passenger on' + str(linenum))
            filterinput['taked'] = True
            elepassenger[eleid].append(passid)
            eletime[eleid] = dtime
    for oriitem in ori:
        if oriitem['from'] != oriitem['to']:
            return ("wa", "passenger {} not arrive, at {}".format(oriitem['id'], oriitem['from']))
    return ('ac', 'pass all')


def do(jar='hw1.jar'):
    global id
    thidid = 0
    if idlock.acquire():
        thisid = id
        id += 1
        idlock.release()
    g = Generator()
    oril, input, ori = g.genData()
    if len(ori)==0:
        return
    stdin = str(thisid) + "input.txt"
    with open(stdin, 'w') as f:
        f.write(input)
    with multiprocessing.Manager() as m:
        result = m.dict({'res':'','success':False})
        process = Process(target=execute_java, args=(ori, jar, result))
        process.start()
        process.join()
        res = result['res']
        success = result['success']
    if ('java' in res):
        safeaddre(jar)
        os.rename(stdin, 're_' + stdin)
        with open('re_out_' + str(thisid) + '.txt', 'w') as f:
            f.write(res)
        sp.release()
        return
    if not success:
        safeaddtle(jar)
        os.rename(stdin, 'tle_' + stdin)
        with open('tle_out_' + str(thisid) + '.txt', 'w') as f:
            f.write(res)
        sp.release()
        return
    checkResult, reason = check(ori, res)
    if checkResult == 'wa':
        safeaddwa(jar)
        os.rename(stdin, 'wa_' + stdin)
        with open('wa_out_' + str(thisid) + '.txt', 'w') as f:
            f.write(reason)
            f.write('\n')
            f.write(res)
        sp.release()
        return
    os.remove(stdin)
    safeaddsuccess(jar)
    sp.release()
    return


import tkinter as tk
from tkintertable import TableCanvas

onlyOne = threading.Lock()


def tickerRedraw(tb, root):
    global data
    tb.redraw()

    root.after(3000, tickerRedraw, tb, root)


import gc


def timeoutMain(jar, times, num):
    global total, sp
    total = times
    sp = threading.Semaphore(num)
    now = 0
    while now <= times:
        now += 1
        if now % 10 == 0 and datawrite.acquire(True):
            data['当前测试进度']['name'] = str(now) + '/' + str(times)
            datawrite.release()
        if sp.acquire(True):
            threading.Thread(target=do, args=(jar,)).start()
    if datawrite.acquire(True):
        data["当前测试进度"]['name'] = 'finished'
        datawrite.release()


def forjar(jars, ent, e2):
    if onlyOne.acquire(True, timeout=1):
        for jar in jars:
            timeoutMain(jar, int(ent.get()), int(e2.get()))

        onlyOne.release()


def trigTest(jars, ent, e2, emax, esametime, etime):
    global SAMETIME, ITEM, MAXTIME
    ITEM = int(emax.get())
    SAMETIME = int(esametime.get())
    MAXTIME = int(etime.get())
    t = threading.Thread(target=forjar, args=(jars, ent, e2))
    t.start()


def window_thread(data, jars):
    root = tk.Tk()
    root.geometry("1024x500")
    frame = tkinter.Frame(root)
    frame.pack(fill="both", expand=True)

    framebutton = tkinter.Frame(root)
    framebutton.pack(side='right', fill='both', expand=True)

    frame2 = tkinter.Frame(root)
    frame2.pack(side='top', fill='x')
    tk.Label(frame2, text="输入测试次数").pack(side='left')
    e = tk.Entry(frame2)
    e.pack(side="left", fill='x', expand=True)
    e.insert(0, '100')
    tk.Label(frame2, text="输入线程").pack(side='left')
    e2 = tk.Entry(frame2)
    e2.pack(side="left", fill='x', expand=True)
    e2.insert(0, '32')

    frame3 = tkinter.Frame(root)
    frame3.pack(fill='x')
    tk.Label(frame3, text='最大请求数量：').pack(side='left')
    e3 = tk.Entry(frame3)
    e3.pack(side='left', fill='x', expand=True)
    e3.insert(0, '15')
    tk.Label(frame3, text="最大同时请求量：").pack(side='left')
    e4 = tk.Entry(frame3)
    e4.pack(side='left', fill='x', expand=True)
    e4.insert(0, '2')
    tk.Label(frame3, text="时间限制：").pack(side='left')
    e5 = tk.Entry(frame3)
    e5.pack(side='left', fill='x', expand=True)
    e5.insert(0, '20')

    b = tk.Button(framebutton, text="run!", command=lambda: trigTest(jars, e, e2, e3, e4, e5))
    b.pack(side="right", fill='both', expand=True)
    tb = TableCanvas(frame, data=data)
    tb.show()
    tickerRedraw(tb, root)
    root.wm_title('xgenerator-u2-v2.0')
    root.mainloop()


data = {}

jars = []


def main():
    for jar in jars:
        data[jar] = {'name': jar, 'pass': 0, 'fail': 0, 'tle': 0, 're': 0}
    data['当前测试进度'] = {'name': "0/0"}
    threading.Thread(target=window_thread, args=(data, jars)).start()


def mainTest():
    g = Generator()
    for i in range(100):
        print(g.genData())


import time
import os

if __name__ == '__main__':
    files = os.listdir('.')
    jars = [file for file in files if os.path.splitext(file)[-1] == '.jar']
    time1 = time.time()
    main()
    time2 = time.time()
    print("start time: " + str(time2 - time1))

    while True:
        time.sleep(10)
        pass
