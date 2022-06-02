import numpy as np
import sys
import time


def input_file(filename):
    global M,N,A
    with open(filename) as f:
        M=int(f.readline())
        N=int(f.readline())
        A=np.array([[int(num) for num in line.split()] for line in f])
input_file('2x3(5).txt')
print(A)
print('='*(3*N))
check=np.zeros((M,N),dtype='int')

lim=int(input('Enter the bulb life:'))
print('Processing...\n')

def check_complete(B):
   if all(i==1 for i in np.nditer(B)):
       return True
   return False

def change_node(x,y,A,B):
    if A[x,y]==0:
        B[x,y]=B[x,y]+1
        if B[x,y]>lim:
            A[x,y]=-1
        else:
            A[x,y]=1
    elif A[x,y]==1:
        A[x,y]=0
    
def change(x,y,A,countA):                   #changing and counting
    count=np.zeros((M+2,N+2),dtype='int')
    count[1:M+1,1:N+1]=countA
    B=np.zeros((M+2,N+2),dtype='int')
    B[1:M+1,1:N+1]=A
    change_node(x,y,B,count)
    change_node(x+1,y,B,count)
    change_node(x-1,y,B,count)
    change_node(x,y+1,B,count)
    change_node(x,y-1,B,count)
    A=B[1:M+1,1:N+1]
    countA=count[1:M+1,1:N+1]
    return [A,countA]

XY=[]                                       #List of nodes
for i in range(1,M+1):
    for j in range(1,N+1):
        XY.append((i,j))

b=[]
n=M*N
start=time.time()
count_state=0

def Try(a,i):                       #back_tracking
        global count_state                        
        if check_complete(checkA[0]):
            print(checkA[0])
            print('The current state is completed.')
            sys.exit()
        elif any(i==-1 for i in np.nditer(checkA[0])):
            print(checkA[0])
            print('The current state is broken.')
        else:
            
            for v in range(lst_ind[a-1]+1,M*N-i+a+2):
                x,y=XY[v-1]
                if (all(i!=-1 for i in np.nditer(change(x,y,checkA[a],count[a])[0]))):
                    count_state+=1
                    checkA[a+1],count[a+1]=change(x,y,checkA[a],count[a])[0],change(x,y,checkA[a],count[a])[1]
                    solu[a]=XY[v-1]
                    lst_ind[a]=v
                    if count_state<=2000000:
                        if a>=i-1:                        
                            if check_complete(checkA[a+1]):                            
                                b.append([solu[i] for i in range(a+1)])
                                print(checkA,'\n')
                                print(solu)
                                end=time.time()
                                print('running time:',end-start,'s')
                                print(count_state)
                                sys.exit()
        
                        else:
                            Try(a+1,i)
                    else:
                        print('Time out!')
                        end3=time.time()
                        print('running time:',end3-start,'s')
                        sys.exit()

for i in range(1,M*N+1):
    checkA=np.zeros((i+1,M,N),dtype='int')
    count=np.zeros((i+1,M,N),dtype='int')
    checkA[0]=A
    solu=[(0,0)]*i
    lst_ind=[0]*i
    Try(0,i)
if len(b)==0:
    print('Failure')
    end2=time.time()
    print('running time:',end2-start,'s')