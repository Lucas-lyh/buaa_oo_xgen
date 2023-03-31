from main2 import *

if __name__ == "__main__":
    with open("data.txt", "w") as f:
        g = Generator()
        a,b,c,d,e = g.genData()
        f.write(b)