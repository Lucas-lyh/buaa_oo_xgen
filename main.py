# -*- coding:utf-8 -*-
import ctypes
import random
import subprocess
import sys
import tkinter

import sympy
from sympy import symbols

DEPTH = 4
ITEM = 10
MAXLEN = 150


class Generator:
    x, y, z = symbols("x y z")
    function = {}
    genfunc = True
    dgened = False

    def genDFactor(self, varilist, depth=1, ):
        self.dgened = True
        res = '(' + self.generateExpr(depth=depth, varilist=varilist, item=3) + ')'
        vari = random.choice(varilist)
        if vari not in res:
            vari = random.choice(varilist)
        res = 'd' + vari + res
        return res

    def regenfunc(self, num=1):
        self.function = {}
        funcname = ['f', 'g', 'h']
        random.shuffle(funcname)
        for i in range(num):
            name = funcname[i]
            variname = ['x', 'y', 'z']
            varinum = random.choice([1, 2, 3])
            random.shuffle(variname)
            varilist = [variname[i] for i in range(varinum)]
            expr = self.generateExpr(varilist, max(1, DEPTH // 3), 2)
            self.function[name] = [varilist, expr]

    def generateExpr(self, varilist, depth=1, item=5):
        if varilist is None:
            varilist = ['x', 'y', 'z']
        item = random.choice(range(1, item + 1))
        res = ''
        for i in range(item):
            res += (random.choice(range(2)) * ' ')
            if (i == 0):
                res += random.choice(["", '+', '-'])
            else:
                res += random.choice(['+', '-'])
            res += (random.choice(range(2)) * ' ')
            res += self.generateTerm(depth=depth, item=item, varilist=varilist)
        return res

    def generateExprFactor(self, varilist, depth=0):
        res = ''
        res += '('
        res += self.generateExpr(depth=depth, item=3, varilist=varilist)
        res += ")"
        k = random.choice([0, 1])
        if k == 1:
            res += (random.choice(range(2)) * ' ')
            res += self.generateIndex(varilist=varilist)
        return res

    def generateIndex(self, varilist, max=2):
        res = "**"
        res += (random.choice(range(2)) * ' ')
        res += random.choice(["", '+'])
        res += self.generateNum(len=1, max=max, zero_begin=True, varilist=varilist)
        return res

    def generateNum(self, varilist, len=10, max=10000000, zero_begin=False, depth=0):
        return str(random.choice(range(5)))

    def generateFunctionCall(self, varilist, max=8, depth=1):
        funcname = random.choice(list(self.function.keys()))
        res = "" + funcname + "("
        varinum = len(self.function[funcname][0])
        for i in range(varinum):
            if (i != 0):
                res += ','
            clist = [self.generateNumFactor, self.generateVariFactor]
            if (depth > 0):
                clist += [self.generateExprFactor,
                          self.generateCosFactor,
                          self.generateSinFactor
                          ] \
                         + ([self.genDFactor] if not self.dgened else []) \
                         + ([self.generateFunctionCall] if (self.genfunc and self.function != {}) else [])
            factor = random.choice(clist)
            res += factor(varilist=varilist, depth=depth - 1)
        res += ')'
        return res

    def generateVariFactor(self, varilist, max=8, depth=0):
        res = random.choice(varilist)
        k = random.choice([0, 1])
        if k == 1:
            res += (random.choice(range(2)) * ' ')
            res += self.generateIndex(varilist=varilist)
        return res

    def generateSinFactor(self, varilist, depth=0):
        res = "sin("
        clist = [self.generateNumFactor, self.generateVariFactor]
        if (depth > 0):
            clist += [self.generateExprFactor,
                      self.generateCosFactor,
                      self.generateSinFactor] \
                     + ([self.genDFactor] if not self.dgened else []) \
                     + ([self.generateFunctionCall] if (self.genfunc and self.function != {}) else [])
        factor = random.choice(clist)
        res += factor(depth=depth - 1, varilist=varilist)
        res += ')'
        return res

    def generateCosFactor(self, varilist, depth=0):
        res = "cos("
        clist = [self.generateNumFactor, self.generateVariFactor]
        if (depth > 0):
            clist += [self.generateExprFactor,
                      self.generateCosFactor,
                      self.generateSinFactor] \
                     + ([self.genDFactor] if not self.dgened else []) \
                     + ([self.generateFunctionCall] if (self.genfunc and self.function != {}) else [])
        factor = random.choice(clist)
        res += factor(depth=depth - 1, varilist=varilist)
        res += ')'
        return res

    def generateNumFactor(self, varilist, max=100000000000, depth=0):
        res = random.choice(['', '+', '-'])
        res += self.generateNum(len=5, max=max, varilist=varilist)
        return res

    def generateTerm(self, varilist, depth=1, item=5):
        item = random.choice(range(1, item + 1))
        res = ''
        res += random.choice(['', '+', '-'])
        res += (random.choice(range(2)) * ' ')
        if (depth >= 1):
            factor = random.choice([self.generateNumFactor,
                                    self.generateVariFactor,
                                    self.generateExprFactor,
                                    self.generateCosFactor,
                                    self.generateSinFactor] \
                                   + ([self.genDFactor] if not self.dgened else []) \
                                   + ([self.generateFunctionCall] if (self.genfunc and self.function != {}) else []))
            res = res + factor(depth=depth - 1, varilist=varilist)
        else:
            factor = random.choice([self.generateNumFactor,
                                    self.generateVariFactor])
            res = res + factor(depth=depth - 1, varilist=varilist)
        if depth > 0:
            for i in range(item - 1):
                res += (random.choice(range(2)) * ' ')
                res += '*'
                res += (random.choice(range(2)) * ' ')
                factor = random.choice([self.generateNumFactor,
                                        self.generateVariFactor,
                                        self.generateExprFactor,
                                        self.generateCosFactor,
                                        self.generateSinFactor] \
                                       + ([self.genDFactor] if not self.dgened else []) \
                                       + ([self.generateFunctionCall] if (
                        self.genfunc and self.function != {}) else []))
                res += factor(depth=depth - 1, varilist=varilist)
        else:
            for i in range(item - 1):
                res += (random.choice(range(2)) * ' ')
                res += '*'
                res += (random.choice(range(2)) * ' ')
                factor = random.choice([self.generateNumFactor,
                                        self.generateVariFactor])
                res += factor(depth=depth - 1, varilist=varilist)
        return res


import threading

num = 0
mutex = threading.Lock()
datawrite = threading.Lock()


def execute_java(stdin, jar):
    cmd = ['java', '-jar',"-Xms128m", "-Xmx256m", jar]  # 更改为自己的.jar包名
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    success = True
    try:
        stdout, stderr = proc.communicate(stdin.encode(), timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        success = False
    if not success:
        raise
    return stdout.decode().strip()


def aSympify(str, locals):
    return sympy.sympify(str, locals=locals)


def getlocals(varilistori):
    varilist = varilistori
    res = '{'
    for v in varilist:
        res += '"' + v + '":' + v
        res += ','
    res = res[:-1]

    res += '}'
    return res


import asyncio


def dx(x):
    return sympy.diff(x, sympy.symbols('x'))


def dy(x):
    return sympy.diff(x, sympy.symbols('y'))


def dz(x):
    return sympy.diff(x, sympy.symbols('z'))


idlock = threading.Lock()
idnow = 0
sp = threading.Semaphore(0)
def do(jar='hw1.jar'):
    print("lock"+str(sp._value))
    global data
    gen = Generator()
    def myret():
        sp.release()
        #del gen,funclocals
        #del funclocals
        exit(0)
    try:
        def f():
            return 0

        def g():
            return 0

        def h():
            return 0

        whered = random.choice(range(2))
        gen.dgened = whered
        gen.genfunc = True
        gen.regenfunc(random.choice([1, 2, 3]))
        gen.dgened = not whered
        if idlock.acquire(True):
            global idnow
            id = idnow
            idnow += 1
            idlock.release()
        instr = str(len(gen.function))
        instr += '\n'
        funclocals = {'dx': dx, 'dy': dy, 'dz': dz}
        for name in gen.function.keys():
            fstart = name
            fstart += '('
            varistr = ''
            for v in gen.function[name][0]:
                if varistr != '':
                    varistr += ','
                varistr += v
            fstart += varistr
            fstart += ')'
            defstr = "def " + fstart + ":\n" + "\treturn sympy.sympify(\"" + \
                     str(sympy.sympify(gen.function[name][1], locals=funclocals))

            defstr = defstr + '\",locals = ' + getlocals(gen.function[name][0]) + ')\n'
            loc = {}
            exec(defstr, globals(), loc)
            f = loc['f'] if 'f' in loc else f
            g = loc['g'] if 'g' in loc else g
            h = loc['h'] if 'h' in loc else h
            funclocals[name] = eval(name)
            instr += fstart
            instr += "="
            instr += gen.function[name][1]
            instr += '\n'

        test = gen.generateExpr(item=ITEM, depth=DEPTH, varilist=['x', 'y', 'z'])
        checktest = test.replace(' ', '', -1)
        if (len(checktest) > MAXLEN):
            del test,checktest
            del gen, funclocals
            myret()
        time1 = time.time()
        correct =  0
        try:
            correct = aSympify(test, locals=funclocals).expand()
        except Exception as e:
            del correct
            del gen, funclocals
            myret()
        if (len(str(correct)) > 2000):
            myret()

        # print('ac pre')
        if mutex.acquire(True):
            # print('aced pre')
            with open("./tle_" + jar + "_" + str(id) + '.txt', 'w') as f:
                f.write(instr + test)
            mutex.release()
        # print('ac pred')
        if datawrite.acquire(True):
            # print('aced pred')
            data[jar]['tle'] += 1
            datawrite.release()
        out = 0
        try:
            out = execute_java(instr + test, jar)
        except:
            del test, checktest
            del out
            del gen, funclocals
            myret()
        if ('java' in out):
            # print('acre pred')
            if datawrite.acquire(True):
                # print('acred pred')
                data[jar]['tle'] -= 1
                data[jar]['re'] += 1
                datawrite.release()
            # print('acre pre')
            if mutex.acquire(True):
                # print('acred pre')
                if ([file for file in os.listdir('.') if "tle_" + jar + "_" + str(id) + '.txt' in file] != []):
                    os.remove("./tle_" + jar + "_" + str(id) + '.txt')
                with open('./re_' + jar + "_" + str(id) + '.txt', 'w') as f:
                    f.write(instr + test)
                mutex.release()
            myret()
        check = 0
        try:
            check = aSympify(out, {})
        except:
            del test, checktest
            del out
            del gen, funclocals
            del check
            if (datawrite.acquire(True)):
                data[jar]['fail'] += 1
                if (mutex.acquire(True)):
                    # print("acfed pred")
                    with open("./hacklist.txt", 'a') as f:
                        f.write(
                            jar + 'can\'t sympify, try to run and check the result\ndata:-------------------------------\n')
                        f.write(str(instr) + str(test))
                        f.write('\nerr:\n' + out + '\n============================================\n')
                    data[jar]['tle'] -= 1
                    if ([file for file in os.listdir('.') if "tle_" + jar + "_" + str(id) + '.txt' in file] != []):
                        os.remove("./tle_" + jar + "_" + str(id) + '.txt')
                    mutex.release()
                datawrite.release()
            myret()
        test1 = 0
        test2 = 0
        subresult = 0
        try:
            test1 = correct
            test2 = check.expand()
            subresult = (test1 - test2).simplify()
        except:
            del test, checktest
            del out
            del gen, funclocals
            del check
            del test1,test2,subresult
            if datawrite.acquire(True):
                if mutex.acquire(True):
                    data[jar]['tle'] -= 1
                    if ([file for file in os.listdir('.') if "tle_" + jar + "_" + str(id) + '.txt' in file] != []):
                        os.remove("./tle_" + jar + "_" + str(id) + '.txt')
                    mutex.release()
                datawrite.release()
            myret()

        if (datawrite.acquire(True)):
            if (subresult != 0):
                data[jar]['fail'] += 1
                if (mutex.acquire(True)):
                    with open("./hacklist.txt", 'a') as f:
                        f.write(jar + '\ndata:-------------------------------\n')
                        f.write(str(instr) + str(test) + '\nright:\n')
                        f.write(str(test1) + '\nerr:\n' + out + '\n============================================\n')
                    mutex.release()
            else:
                data[jar]['pass'] += 1
            global total
            print(total)
            total = total - 1
            data[jar]['tle'] -= 1
            if ([file for file in os.listdir('.') if ("tle_" + jar + "_" + str(id) + '.txt') in file] != []):
                os.remove("./tle_" + jar + "_" + str(id) + '.txt')
            datawrite.release()
        del test, checktest
        del out
        del gen, funclocals
        del check
        del test1, test2, subresult
        myret()
    except Exception as e:
        print(e.args)
        print("fatal error!!!!!!!!!!")
        myret()


import tkinter as tk
from tkintertable import TableCanvas

onlyOne = threading.Lock()


def tickerRedraw(tb, root):
    global data
    tb.redraw()

    root.after(3000, tickerRedraw, tb, root)
import gc

def timeoutMain(jar, times, num):
    global total,sp
    total = times
    sp = threading.Semaphore(num)
    now = 0
    while now <= times:
        now += 1
        if now%10==0 and datawrite.acquire(True):
            data['当前测试进度']['name'] = str(now) + '/' + str(times)
            datawrite.release()
        if sp.acquire(True):
            threading.Thread(target=do, args=(jar,)).start()
        gc.collect()
    if datawrite.acquire(True):
        data["当前测试进度"]['name'] = 'finished'
        datawrite.release()


def forjar(jars, ent, e2):
    if onlyOne.acquire(True, timeout=1):
        for jar in jars:
            t = threading.Thread(target=timeoutMain, args=(jar, int(ent.get()), int(e2.get())))
            t.start()
            t.join()
        onlyOne.release()


def trigTest(jars, ent, e2, edep, eitem, elen):
    global DEPTH, ITEM, MAXLEN
    ITEM = int(eitem.get())
    DEPTH = int(edep.get())
    MAXLEN = int(elen.get())
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
    tk.Label(frame3, text='表达式嵌套深度：').pack(side='left')
    e3 = tk.Entry(frame3)
    e3.pack(side='left', fill='x', expand=True)
    e3.insert(0, '4')
    tk.Label(frame3, text="表达式项数：").pack(side='left')
    e4 = tk.Entry(frame3)
    e4.pack(side='left', fill='x', expand=True)
    e4.insert(0, '3')
    tk.Label(frame3, text="最大长度：").pack(side='left')
    e5 = tk.Entry(frame3)
    e5.pack(side='left', fill='x', expand=True)
    e5.insert(0, '150')

    b = tk.Button(framebutton, text="run!", command=lambda: trigTest(jars, e, e2, e3, e4, e5))
    b.pack(side="right", fill='both', expand=True)
    tb = TableCanvas(frame, data=data)
    tb.show()
    tickerRedraw(tb, root)
    root.mainloop()


data = {}


async def main(jars):
    for jar in jars:
        data[jar] = {'name': jar, 'pass': 0, 'fail': 0, 'tle': 0, 're': 0}
    data['当前测试进度'] = {'name': "0/0"}
    threading.Thread(target=window_thread, args=(data, jars)).start()


import time
import os

if __name__ == '__main__':
    files = os.listdir('.')
    jars = [file for file in files if os.path.splitext(file)[-1] == '.jar']
    time1 = time.time()
    asyncio.run(main(jars))
    time2 = time.time()
    print("start time: " + str(time2 - time1))
