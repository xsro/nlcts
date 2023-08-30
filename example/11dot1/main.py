import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
import sys
from pathlib import Path

# Define the model
class Pendulum:
    def __init__(self,a,b) -> None:
        self.a=a;self.b=b
    def rhs(self,t:float,x:np.ndarray):
        a,b=(self.a,self.b)
        x1,x2,xhat1,xhat2,p11,p12,p22 = x.tolist()
        y=x1
        dx1=x2 
        dx2=-x1-2*x2+a*x1**2*x2+b*np.sin(2*t)
        dxhat1=xhat2+p11*(y-xhat1)
        dxhat2=-xhat1-2*xhat2+0.25*xhat1**2*xhat2 + 0.2 * np.sin(2*t) + p12*(y-xhat1)
        dp11=2*p12+1-p11**2
        dp12=p11*(-1+0.5*xhat1*xhat2)+p12*(-2+0.25*xhat1**2)
        dp22=2*p12*(-1+0.5*xhat1*xhat2)+2*p22*(-2+0.25*xhat1**2)+1-p12**2
        return np.array([dx1,dx2,dxhat1,dxhat2,dp11,dp12,dp22])
    
#[test]
def test():
    p=Pendulum(0.25,0.2)
    dx=p.rhs(0,np.array([1,-1,0,0,1,0,1]))
    print(dx)
p=Pendulum(0.25,0.2)
x0=np.array([1,-1,0,0,1,0,1])
tspan=[0,6]
sol=solve_ivp(p.rhs,tspan,x0,t_eval=np.linspace(*tspan,10000))

#%% Plot
plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.plot(sol.t,sol.y[0,:],"r",label="$x_1$")
plt.plot(sol.t,sol.y[2,:],"r--",label=r"$\hat{x}_1$")
plt.plot(sol.t,sol.y[1,:],"g",label="$x_2$")
plt.plot(sol.t,sol.y[3,:],"g--",label=r"$\hat{x}_2$")
plt.legend()
plt.grid()
plt.ylabel("Estimation Error")
plt.xlabel("time")
plt.subplot(1,2,2)
plt.plot(sol.t,sol.y[4,:],label="$p_{11}$")
plt.plot(sol.t,sol.y[5,:],label="$p_{12}$")
plt.plot(sol.t,sol.y[6,:],label="$p_{22}$")
plt.legend()
plt.grid()
plt.ylabel("Components of $P(t)$")
plt.xlabel("time")
plt.tight_layout()
plt.savefig("extended_kalman.pdf",transparent = True)
# %%
