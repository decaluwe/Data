# Useful libraries
import math as m
import numpy as np
import random as r


# Imput variables

time = 2 #hrs
dt= 0.5 #hrs

k_nuc = 9000 #reaction constant
theta = 1 # fraction of nucleation sites
a_nuc = 4.5 #activation energy
n = 2 #reaction constant
c_k = 1.5#concentration of precipitant
co_k = 1 #100% saturation
nx = 12

#Calculated variables
S = c_k/co_k
# Rough Calculation of S_nuc

S_nuc_1 = np.around(k_nuc*theta*m.exp(-a_nuc/(n*m.log(S))),0)

# populate rows of an array
srf = list(np.zeros(nx))

for t in np.arange(time/dt):
    theta=srf.count(0)/nx
    S_nuc_1 = np.around(k_nuc*theta*m.exp(-a_nuc/(n*m.log(S))),0)
    for i in range(len(srf)):
        if srf[i] ==0:
            if r.randint(1,10)*.1 <.5:
                srf[i] = S_nuc_1
                print(srf)



