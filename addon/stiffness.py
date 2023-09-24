# port example of ode in https://ww2.mathworks.cn/help/matlab/math/solve-stiff-odes.html?lang=en
# to python and compare performance
#%%
import numpy as np
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp

def rhs(t,y):
    dydt = [y[1],1000*(1-y[0]**2)*y[1]-y[0]]
    return dydt

#%%
sol=solve_ivp(rhs,[0,3000],np.array([2,0]))
plt.figure()
plt.plot(sol.t,sol.y[1,:],'-o')
plt.title('Solution of van der Pol Equation, \mu = 1000')
plt.xlabel('Time t')
plt.ylabel('Solution y_1')

#%%
# sol=solve_ivp(rhs,[0,3000],np.array([2,0]), method='Radau')
sol=solve_ivp(rhs,[0,3000],np.array([2,0]), method='BDF')
plt.figure()
plt.plot(sol.t,sol.y[1,:],'-o')
plt.title('Solution of van der Pol Equation, \mu = 1000')
plt.xlabel('Time t')
plt.ylabel('Solution y_1')

# %%
