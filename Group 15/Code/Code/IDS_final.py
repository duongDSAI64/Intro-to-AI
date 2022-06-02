import numpy as np
import time


def input_file(filename):
    global w, l, r
    with open(filename) as f:
        l = int(f.readline())
        w = int(f.readline())
        r = [None, None] + [list([[int(num) for num in line.split()] for line in f])]


input_file('6x6.txt')
goal = [None, None] + [[[1 for i in range(w)] for i in range(l)]]
print(np.array(r[2], dtype=int))
print('='*(3*l))
k = int(input('the life time of a bulb: '))
start = time.time()


def action(node):
    act = []
    if node == r:
        a, b= -1, -1
    else:
        a, b = node[1]
    for i in range(l):
        for j in range(w):
            if i > a:
                act.append((i, j))
            elif i == a:
                if j > b:
                    act.append((i, j))
    return act


def change_state(u):
    if u != 0:
        u -= 1
    elif u == 0:
        u += 1
    return u


def child(action, node):
    i, j = action[0]+1, action[1]+1
    n = np.array(node[2])
    ch = [[0 for i in range(w)] for i in range(l)]
    clone = np.zeros((l+2,w+2), dtype=int)
    clone[1:l+1, 1:w+1] = n[:, :]
    clone[i, j] = change_state(clone[i, j])
    clone[i + 1, j] = change_state(clone[i + 1, j])
    clone[i - 1, j] = change_state(clone[i - 1, j])
    clone[i, j - 1] = change_state(clone[i, j - 1])
    clone[i, j + 1] = change_state(clone[i, j + 1])
    for k in range(1, l + 1):
        for h in range(1, w + 1):
            ch[k - 1][h - 1] = clone[k, h]
    return [node[2], (i-1, j-1), ch]


def update_c(node):
    global c
    for i in range(l):
        for j in range(w):
            c[i, j] += node[2][i][j] * (node[2][i][j] - node[0][i][j])


def reverse_update_c(node):
    global c
    for i in range(l):
        for j in range(w):
            c[i, j] -= node[2][i][j] * (node[2][i][j] - node[0][i][j])


def count_0(node):
    count=0
    for i in range(l):
        for j in range(w):
            if node[2][i][j] == 0:
                count += 1
    return count


def DLS(node, limit):
    global c, pressed, num
    if num>=2000000:
        return
    if node[2] == goal[2]:
        return 'Found'
    elif limit == 0 or limit < count_0(node)//5:
        return 'cut_off'
    else:
        cut_off = False
        for act in action(node):
            u = child(act, node)
            update_c(u)
            if any(i > k for i in np.nditer(c)):
                reverse_update_c(u)
            else:
                num += 1
                path[len(path)-limit] = u
                result = DLS(u, limit-1)
                reverse_update_c(u)
                if result == 'cut_off':
                    cut_off = True
                elif result != 'Failure':
                    return result
        if cut_off == True:
            return 'cut_off'
        else:
            return 'Failure'


print(' Processing ...')

num = 0
def IDS():
    global c, path
    limit = count_0(r) // 5
    while limit < l*w + 1:
        c = np.zeros((l , w), dtype=int)
        path = [0]*limit
        result = DLS(r, limit)
        if num>=2000000:
            print('time limit exceeded')
            print('stop at depth:',limit)
            break
        elif result != 'cut_off':
            print(num)
            print(result)
            if result == 'Failure':
                break
            else:
                print(np.array(r[2]))
                for i in path:
                    print('PRESS: ', (i[1][0]+1, i[1][1]+1))
                    print(np.array(i[2]))
                break
        limit+=1
    if limit >=l*w + 1:
        print ('Failure')
IDS()
print('RUN TIME = ', time.time()-start)
