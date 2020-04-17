import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
import os

#Reference https://www.fuelcellstore.com/avcarb-mgl190

carb_area=(9**2)*np.pi #in mm^2
carb_v =  carb_area*0.19 #in mm^3
carb_den = 0.44*.001 #in g/mm^3
porosity = 0.78 #percentage
carb_m = carb_v*carb_den*(1. - porosity) 

def graph(file):
    D = pd.read_table(file, sep='deliminator', engine='python', header=None)
    D.dropna(inplace = True)
    D = D[0].str.split("\t", expand = True)

    d_row = list(D[1]).index('0') #This means we cut the data when the time is zero.  To look at full data, use d_row = list(D[0]).index('#') + 1
    D = D.iloc[d_row : ,]

    D[1] = D[1].astype(float)
    D[2] = D[2].astype(float)
    D[3] = D[3].astype(float)
    


    D['capacity'] = D[1] * abs(D[3])/carb_m*1000/3600 #convert to mAh/g
    title = file.split("_cycle")
    title2 = title[1]
    
    for cell in D[2]:
        if cell > D.iloc[0,2]:
            row = list(D[2]).index(cell)
            newc=D.iloc[row:,2]
            D['adjust']=newc
            D['charge']=D['adjust'].shift(-1*row)
            break
   
    D['discharge'] =D[2].where(D[2]<=D.iloc[0,2]) 
            
# =============================================================================
#     if D.iloc[1,2] < 0:
#         D['absolute'] = D[2]*-1
#         plt.figure(3)
#         plt.scatter(D[1], D['absolute'], marker='o', label = title2)
#         plt.legend(framealpha=1, frameon=True);
#         plt.xlabel('time (s)', fontsize=12)
#         plt.ylabel('voltage (V)', fontsize=12)
#     else:
#         plt.figure(3)
#         plt.scatter(D[1], D[2], marker='o', label = title2)
#         plt.scatter(D[1], D['adjust'], marker='o', label = title2)
#         plt.legend(framealpha=1, frameon=True);
#         plt.xlabel('time (s)', fontsize=12)
#         plt.ylabel('voltage (V)', fontsize=12)
# =============================================================================
        
    plt.figure(0)
    plt.scatter(D['capacity'], D['charge'], marker='o', label = title2 +"charge")
    plt.scatter(D['capacity'], D['discharge'], marker='o', label = title2 +"discharge")
    plt.xlabel('Capacity (mAh/g)', fontsize=12)
    plt.ylabel('voltage (V)', fontsize=12)
    plt.legend(framealpha=1, frameon=True);
    
    
    D['Voltgap'] = D['charge'] -D['discharge']
    
    Voltgap = D.Voltgap.mean()
    Voltgap2 = 5
    return [Voltgap, Voltgap2]
    plt.scatter(D['capacity'], D['Voltgap'], marker='o', label = title2)
#    plt.figure(1)
#    plt.scatter(D[1], D[3], marker='o')
#    plt.xlabel('time (s)', fontsize=12)
#    plt.ylabel('current (A)', fontsize=12)

path = 'C:/Users/Amy LeBar/Documents/Data'

i=0
iform =[]
V = []
V2 = []

for file in os.listdir('C:/Users/Amy LeBar/Documents/Data'):
    if file.find('08012019') > -1:
        Voltgap =graph(path + "/"+ file)
        print(Voltgap)
        V.append(Voltgap[0])
        V2.append(Voltgap[1])
        iform.append(i)
        i=i+1
   
    
Report = pd.DataFrame()  
Report['V1'] = V
Report['V2'] = V2
plt.figure(1)
plt.scatter(iform, Report['V1'], marker='o')

