import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
import os

#Reference https://www.fuelcellstore.com/avcarb-mgl190

carb_area=(9**2)*np.pi #in mm^2
carb_v =  carb_area*0.19 #in mm^3
carb_den = 0.44*.001 #in g/mm^3
porosity = 0.78
carb_m = carb_v*carb_den*(1. - porosity) 

def graph(file):
    Data = pd.read_table(file, sep='deliminator', engine='python', header=None)
    Data.dropna(inplace = True)
    Data = Data[0].str.split("\t", expand = True)

    # This means we cut the data when the time is zero.  To look at full data, 
    # use d_row = list(D[0]).index('#') + 1
    d_row = list(Data[1]).index('0') 
    Data = Data.iloc[d_row : ,]

    #---SCD NOTE: CAN YOU PLEASE DOCUMENT WHAT EACH OF THESE ARE?---#
    Data[1] = Data[1].astype(float)
    Data[2] = Data[2].astype(float)
    Data[3] = Data[3].astype(float)

    Data['capacity'] = Data[1] * abs(Data[3])/carb_m*1000/3600 #convert to mAh/g
    title = file.split("_cycle")
    title2 = title[1]
    
    #---SCD NOTE: IN GENERAL, CAN YOU DOCUMENT THESE LINES? WHAT DO THEY DO?---#
    for cell in Data[2]:
        if cell > Data.iloc[0,2]:
            row = list(Data[2]).index(cell)
            newc=Data.iloc[row:,2]
            Data['adjust']=newc
            Data['charge']=Data['adjust'].shift(-1*row)
            break
   
    Data['discharge'] =Data[2].where(Data[2]<=Data.iloc[0,2]) 
            
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
    plt.scatter(Data['capacity'], Data['charge'], marker='o', label = title2 +"charge")
    plt.scatter(Data['capacity'], Data['discharge'], marker='o', label = title2 +"discharge")
    plt.xlabel('Capacity (mAh/g)', fontsize=12)
    plt.ylabel('voltage (V)', fontsize=12)
    plt.legend(framealpha=1, frameon=True);
    
    
    Data['Voltgap'] = Data['charge'] -Data['discharge']
    
    Voltgap = Data.Voltgap.mean()
    Voltgap2 = 5
    return [Voltgap, Voltgap2]
    plt.scatter(Data['capacity'], Data['Voltgap'], marker='o', label = title2)
#    plt.figure(1)
#    plt.scatter(D[1], D[3], marker='o')
#    plt.xlabel('time (s)', fontsize=12)
#    plt.ylabel('current (A)', fontsize=12)

path = 'C:/Users/Amy LeBar/Documents/Data'

i=0
iform =[]
V = []
V2 = []

for file in os.listdir(path):
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

