#%%
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
import sys

# Define the model
class Pendulum:
    def __init__(self,a,b,epsilon,ahat=None,bhat=None) -> None:
        self.a=a;self.b=b
        self.ahat=ahat if ahat!=None else a
        self.bhat=bhat if bhat!=None else b
        self.epsilon=epsilon
    def rhs(self,t:float,x:np.ndarray):
        a,b,ahat,bhat=(self.a,self.b,self.ahat,self.bhat)
        epsilon=self.epsilon
        x1,x2,xhat1,xhat2 = x.tolist()
        y=x1
        dx1=x2 
        dx2=-x1-2*x2+a*x1**2*x2+b*np.sin(2*t)
        dxhat1=xhat2+2/epsilon*(y-xhat1)
        dxhat2=-xhat1-2*xhat2+ahat*xhat1**2*xhat2 + bhat * np.sin(2*t) + 1/(epsilon**2)*(y-xhat1)
        return np.array([dx1,dx2,dxhat1,dxhat2])
    
#[test]
def test():
    p=Pendulum(0.25,0.2,0.001)
    dx=p.rhs(0,np.array([1,0,0,0]))
    print(dx)


#%% adsfa
p=Pendulum(0.25,0.2,0.001)
if "test" in sys.argv:
    dx=p.rhs(np.array([1,0,0,0]),0)
    print(dx)
x0=np.array([1,-0.4,0,0])
tspan=[0,10]
t=np.linspace(0,10,10000)

# case 1 ahat=a bhat=b epsilon=0.01
p11=Pendulum(0.25,0.2,0.001)
# case 1 ahat=a bhat=b epsilon=0.1
p12=Pendulum(0.25,0.2,0.01)
# case 2 ahat=0 bhat=0 epsilon=0.01
p21=Pendulum(0.25,0.2,0.001,0,0)
# case 2 ahat=0 bhat=0 epsilon=0.1
p22=Pendulum(0.25,0.2,0.01,0,0)

sol=solve_ivp(p11.rhs,tspan,x0,t_eval=t);dx11=sol.y
sol=solve_ivp(p12.rhs,tspan,x0,t_eval=t);dx12=sol.y
sol=solve_ivp(p21.rhs,tspan,x0,t_eval=t);dx21=sol.y
sol=solve_ivp(p22.rhs,tspan,x0,t_eval=t);dx22=sol.y

#%% Plot
plt.subplot(2,2,1)
plt.plot(t,dx11[0,:],"k",label="$x_1$")
plt.plot(t,dx11[2,:],"--",label=r"$\hat{x}_1\ (\varepsilon=0.001)$")
plt.plot(t,dx12[2,:],"--",label=r"$\hat{x}_1\ (\varepsilon=0.01)$")
plt.xlim(0,0.5)
plt.ylabel("$x_1$ and Estimates")
plt.xlabel("time")
plt.legend()

plt.subplot(2,2,2)
plt.plot(t,dx11[1,:],"k",label="$x_2$")
plt.plot(t,dx11[3,:],"--",label=r"$\hat{x}_2\ (\varepsilon=0.001)$")
plt.plot(t,dx12[3,:],"--",label=r"$\hat{x}_2\ (\varepsilon=0.01)$")
plt.xlim(0,0.5)
plt.ylabel("$x_2$ and Estimates")
plt.xlabel("time")
plt.legend()

plt.subplot(2,2,3)
plt.plot(t,dx21[1,:]-dx21[3,:],"r",label=r"$x_2-\hat{x}_2\ (\varepsilon=0.001)$")
plt.plot(t,dx22[1,:]-dx22[3,:],"b",label=r"$x_2-\hat{x}_2\ (\varepsilon=0.01)$")
plt.xlim(0,0.4)
plt.ylabel("Estimation Error of $x_2$")
plt.xlabel("time")
plt.legend()

plt.subplot(2,2,4)
plt.plot(t,dx21[1,:]-dx21[3,:],"r",label=r"$x_2-\hat{x}_2\ (\varepsilon=0.001)$")
plt.plot(t,dx22[1,:]-dx22[3,:],"b",label=r"$x_2-\hat{x}_2\ (\varepsilon=0.01)$")
plt.xlim(5,10);plt.ylim(-0.04,0.04)
plt.ylabel("Estimation Error of $x_2$")
plt.xlabel("time")
plt.legend()

plt.tight_layout()
plt.savefig("main.pdf")
plt.show()
# %%
# %%
