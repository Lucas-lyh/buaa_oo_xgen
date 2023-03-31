import sys
import time

inputFileName = sys.argv[1]
ori = []
with open(inputFileName, 'r') as f:
    lines = f.readlines()
    tori = 0
    n = 1
    for line in lines:
        t = float(line.split(']')[0][1:])
        things = line.split(']')[1].split('-')
        item = {}
        if t != tori:
            gap = t - tori
            tori = t
            if ori != []:
                for i in range(n):
                    ori[-i-1]['n'] = n
            n = 1
        else:
            n += 1
        item['gap'] = gap
        item['id'] = int(things[0])
        item['from'] = int(things[2])
        item['to'] = int(things[4])
        ori.append(item)
    for i in range(n):
        ori[-i-1]['n'] = n

if __name__ == '__main__':
    time.sleep(1)
    n = 0
    for item in ori:
        if n == 0:
            n = item['n']
            # print(item['gap'])
            time.sleep(item['gap'])
        n -= 1
        print("{}-FROM-{}-TO-{}".format(item['id'], item['from'], item['to']))
        sys.stdout.flush()
        # print("{}-FROM-{}-TO-{}".format(item['id'], item['from'], item['to']))
    success = True
