import math
import numpy as np

Reuse=list()
#Erlang=pd.read_excel("C:/Users/Amora/OneDrive/Desktop/ErlangB.xlsx").dropna().drop(labels=("(N)"),axis=1)
#Erlang.index = np.arange(1, len(Erlang) + 1)

def Initialize_N():
    for i in range(1,6):
        for j in range(0,i+1):
            N = i**2 + i*j + j**2
            print("N ="+str(N)+"        i = "+str(i)+" , j = "+str(j))
            if(i==j):
                Reuse.append([N,i,j,1,3,4])
            else:
                Reuse.append([N,i,j,1,2,3])
    Reuse.sort()
    print("=================================")
  # print("[N,i,j,10',120',180']\n")        
  # print(Reuse)
    
def erlang(load, channels):
    L = (load ** channels) / math.factorial(channels)
    sum_ = 0
    for n in range(channels + 1): sum_ += (load ** n) / math.factorial(n)
    
    p=L / sum_
    return p

def Find_Cells(City_size,pop,landa_Day,E,Blocking_prop,C_Cluster,C_Cell,CperI,TDM_ratio,Sec):
    
    Blocking_prop=Blocking_prop/100
    No_SubsPerCity=math.floor(City_size*pop)
    landa=landa_Day/(24*60)
    a_user=landa*E              #Avg.load/user  
    
    if (Sec==360):                                
        N=C_Cluster/C_Cell         #Reuse Factor
        C_Cell=math.floor(C_Cell*TDM_ratio)
        a_cell,p=0,0
        
        while (p<Blocking_prop):
            a_cell+=0.01
            p=erlang(a_cell, C_Cell)
            
        No_SubsPerCell=math.floor(a_cell/a_user)
        Cells=math.ceil(No_SubsPerCity/No_SubsPerCell)
        
    else:
        
        No_sectors=360/Sec
        if (Sec==10):
            s=3
        elif(Sec==120):
            s=4
        else:s=5  
        
        for i in range(len(Reuse)):
            N=Reuse[i][0]
            n=Reuse[i][s]
            if ((N/n)>=(CperI/3)):
                break
            
        C_Cell =  (C_Cluster/N )*TDM_ratio
        a_Sec,p=0,0
        C_Sec=math.ceil(C_Cell/No_sectors)
        
        while (p<Blocking_prop):
            a_Sec+=0.01
            p=erlang(a_Sec, C_Sec)    
        
        No_SubsPerCell=math.floor(a_Sec*No_sectors/a_user)
        Cells=math.ceil(No_SubsPerCity/No_SubsPerCell)
    return Cells 
    
def main():
    Initialize_N()
    
    City_size=eval(input("Enter City_size in km2 \n"))
    pop=eval(input("Enter population in 1 km2 \n"))
    landa_Day=eval(input("Enter No.of calls/day \n"))
    E=eval(input("Enter Avg call Duration in min \n"))
    Blocking_prop=eval(input("Enter Blocking_prop in %\n"))
    C_Cluster=int(input("Enter Channels/cluster \n"))
    C_Cell=int(input("Enter Max Channels/cell \n"))
    CperI=eval(input("Enter Carrier to interferance ratio \n"))
    TDM_ratio=eval(input("Enter TDM_ratio \n"))
    
    '''
    City_size=450
    pop=718.667
    landa_Day=10
    E=1
    Blocking_prop=2
    C_Cluster=125
    C_Cell=10
    CperI=6.5
    TDM_ratio=4
    '''
    Sectoring=[10,120,180,360]
    c=list()
    
    c.append(Find_Cells(City_size, pop, landa_Day, E, Blocking_prop, C_Cluster, C_Cell, CperI, TDM_ratio, 10))
    print("10 degree Sectoring ------------>  Cells = "+str(c[0])+'\n')
    c.append(Find_Cells(City_size, pop, landa_Day, E, Blocking_prop, C_Cluster, C_Cell, CperI, TDM_ratio, 120)) 
    print("120 degree Sectoring ------------>  Cells = "+str(c[1])+'\n')
    c.append(Find_Cells(City_size, pop, landa_Day, E, Blocking_prop, C_Cluster, C_Cell, CperI, TDM_ratio, 180))
    print("180 degree Sectoring ------------>  Cells = "+str(c[2])+'\n')
    c.append(Find_Cells(City_size, pop, landa_Day, E, Blocking_prop, C_Cluster, C_Cell, CperI, TDM_ratio, 360)) 
    print("No sectoring ------------>  Cells = "+str(c[3])+'\n')
    m=np.max(c)
    i=c.index(m)
    print("The best secctoring is "+str(Sectoring[i])+" degree , Cells = "+str(m))
       
main()
          