#%% example 12.4
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from numpy import pi
from functools import partial

def sat(y):
    return np.clip(y,-1,1)

# Define the model
class Pendulum:
    def state_to_output(x1,x2):
        theta=x1+pi
        dtheta=x2
        return (theta,dtheta)
    def output_to_state(theta,dtheta):
        x1=theta-pi
        x2=dtheta
        return (x1,x2)
    
    def __init__(self,b,c,mu=0.1) -> None:
        self.b=b;self.c=c
        self.mu=mu
        assert 0<=b and b<=0.2
        assert 0.5<=c and c<=2
    def system(self,t:float,x:np.ndarray,u):
        x1,x2 = x[0:2].tolist()
        theta,dtheta=Pendulum.state_to_output(x1,x2)
        dx1=dtheta
        dx2=self.c*u-np.sin(theta)-self.b*dtheta
        return np.array([dx1,dx2])
    def rhs(self,t:float,x:np.ndarray):
        x1,x2 = x.tolist()
        s=x1+x2
        u=-2*(abs(x1)+abs(x2)+1)*sat(s/self.mu)
        dx=self.system(t,x,u)
        return dx
    def rhs2(self,t:float,x:np.ndarray,epsilon=0,phi0=lambda xhat1,xhat2,u:0):
        # sliding mode control with high-gain observer
        x1,x2,xhat1,xhat2 = x.tolist()
        shat=xhat1+xhat2
        u=-2*(2.5*pi*sat(abs(xhat1)/(2.5*pi))+4.5*pi*sat(abs(xhat2)/(4.5*pi))+1)*sat(shat/self.mu)
        dx=self.system(t,x,u)
        dxhat1=xhat2+(2/epsilon)*(x1-xhat1)
        dxhat2=phi0(xhat1,xhat2,u)+(1/epsilon**2)*(x1-xhat1)
        return np.array([dx[0],dx[1],dxhat1,dxhat2])
    
    
b=0.01
c=0.5
theta0=pi
dtheta0=0
x0=np.array([-pi,0])
p=Pendulum(b,c)


#%%
SF=p.rhs 
OF1=partial(p.rhs2,epsilon=0.05)
OF2=partial(p.rhs2,epsilon=0.01)
sol=dict()
sol["SF"]=solve_ivp(SF,[0,3],np.array(x0))
sol["OF1"]=solve_ivp(OF1,[0,3],np.array([*x0,0,0]))
sol["OF2"]=solve_ivp(OF2,[0,3],np.array([*x0,0,0]))

#%%
SF=p.rhs 
def phi0(xhat1,xhat2,u):
    return -np.sin(xhat1+pi)-0.1*xhat2+1.25*u
OF1=partial(p.rhs2,epsilon=0.05,phi0=phi0)
OF2=partial(p.rhs2,epsilon=0.01,phi0=phi0)
sol2=dict()
sol2["SF"]=solve_ivp(SF,[0,3],np.array(x0))
sol2["OF1"]=solve_ivp(OF1,[0,3],np.array([*x0,0,0]))
sol2["OF2"]=solve_ivp(OF2,[0,3],np.array([*x0,0,0]))
# %%
plt.figure()
for key in ["SF","OF1","OF2"]:
    theta,dtheta=Pendulum.state_to_output(sol[key].y[0,:],sol[key].y[1,:])
    plt.subplot(2,2,1)
    plt.plot(sol[key].t,theta,label=key)
    plt.subplot(2,2,2)
    plt.plot(sol[key].t,dtheta,label=key)
for key in ["SF","OF1","OF2"]:
    theta,dtheta=Pendulum.state_to_output(sol2[key].y[0,:],sol2[key].y[1,:])
    plt.subplot(2,2,3)
    plt.plot(sol2[key].t,theta,label=key)
    plt.subplot(2,2,4)
    plt.plot(sol2[key].t,dtheta,label=key)

for i in range(1,5):
    plt.subplot(2,2,i)
    plt.grid()
    plt.legend(["SF",r"OF1 $\varepsilon=0.05$",r"OF2 $\varepsilon=0.01$"])
    plt.title("("+chr(ord("a")+i-1)+")")
    if i in [1,3]:
        plt.ylabel("$\\theta$")
    if i in [2,4]:
        plt.ylabel("$\\omega=\\dot{\\theta}$")
    plt.xlabel("Time")
plt.tight_layout()
plt.savefig("SFvsOF.pdf")
# %%
