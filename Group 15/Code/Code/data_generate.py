import random
import numpy as np
m = int(input('M ='))
n = int(input('N = '))

for i in range(2,m):
    for j in range(2,n):
        file = open('%sx%s(random).txt'%(i,j),'w')
        file.write('%s \n'%i)
        file.write('%s\n'%j)
        for x in range(i):
            for y in range(j):
                file.write(str(random.randint(0,1))+ ' ')
            file.write('\n')
