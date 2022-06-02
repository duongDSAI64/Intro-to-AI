import numpy as np
import time

def input_file(filename):
    global M,N,A
    with open(filename) as f:
        M=int(f.readline())
        N=int(f.readline())
        A=np.array([[int(num) for num in line.split()] for line in f])
input_file('3x3(0).txt')
A1 = np.zeros((M,N), dtype= int)
A1[:,:]=A[:,:]
print(A)
print('='*(3*N))

check = np.zeros((M,N), dtype = int)
for i in range(M):
    for j in range(N):
        if A[i,j] == 1:
            check[i,j] += 1
def adjacent(i,j):
    L = []
    if i == 0 :
        if j == 0 :
            L = [(i+1,j),(i,j+1)]
        elif j == N-1:
            L = [(i+1,j),(i,j-1)]
        else:
            L = [(i+1,j),(i,j-1),(i,j+1)]
    elif i == M - 1:
        if j == 0 :
            L = [(i-1,j),(i,j+1)]
        elif j == N-1:
            L = [(i-1,j),(i,j-1)]
        else:
            L = [(i-1,j),(i,j-1),(i,j+1)]
    else:
        if j == 0 :
            L = [(i-1,j),(i+1,j),(i,j+1)]
        elif j == N-1:
            L = [(i-1,j),(i+1,j),(i,j-1)]
        else:
            L = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
    return L
d = 10000
a=[]

limit = int(input('the life time of a bulb: '))
start = time.time()
print('Processing ... ')
def Test(A):
    global check
    while np.sum(A) != M*N :
        c1 = []
        for i in range(M):
            for j in range(N):
                if check[i,j] % 2 == 0:
                    c1.append(check[i,j])
        k = min(c1)

        for i in range(M):
            for j in range(N):
                if check[i,j] == k :
                    a.append([i,j])
                    A[i,j] = 1 - A[i,j]
                    check[i,j] += 1
                    if check[i,j] > d:
                        return False
                    for x in adjacent(i,j):
                        A[x[0],x[1]] = 1 - A[x[0],x[1]]
                        check[x[0],x[1]] += 1
                        if check[x[0],x[1]] > d:
                            return False
    return True
c = np.zeros((M,N), dtype=int)
def action(node):
    i, j = node[0], node[1]
    A[i, j] = 1 - A[i,j]
    for x in adjacent(i, j):
        A[x[0], x[1]] = 1- A[x[0],x[1]]
def check_limit(node):
    i,j = node[0], node[1]
    if A[i,j] == 1:
        c[i,j] += 1
        if c[i,j] > limit:
            return False
    for x in adjacent(i,j):
        if A[x[0],x[1]] == 1:
            c[x[0],x[1]] += 1
            if c[x[0],x[1]] > limit:
                return False
    return True

real_a=[]
if Test(A):
    A[:,:] = A1[:,:]
    for i in a:
        if a.count(i) % 2 == 1 and i not in real_a:
            real_a.append(i)
    real_a.sort()
    for x in real_a:
        action(x)
        if not check_limit(x):
            print('Exceed limit:\n ',c)
            print('Failure!')
            break
        print('PRESS', x)
        print(A)
    print(real_a)

else:
    print('Failure!')
end = time.time()
print('Running time: %.4f'%(end-start))
