import argparse
import os

a = [ 3 ]

if __name__ == "__main__":
    #for root, dirs, files in os.walk("./websource"):
    #    for x in files:
    #        print(str(root) + str(x))
    
    b = [ str(y[0]) + "/" + str(y[2][x]) for y in os.walk("./websource") for x in range(len(y[2])) ]
    print(b)
