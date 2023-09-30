#%% example 12.4
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from numpy import pi
from dataclasses import dataclass

class Source:
    def __init__(self,omega) -> None:
        self.omega=omega
    def __call__(self,t):
        return np.sin(self.omega*t)
    def d(self,t):
        return np.cos(self.omega*t)*self.omega
    def dd(self,t):
        return -np.sin(self.omega*t)*self.omega**2
    
# Define the model
class Pendulum:
    def __init__(self,b,c) -> None:
        self.b=b;self.c=c
    def system(self,t:float,x1,x2,u):
        dx1=x2
        dx2=-np.sin(x1)-self.b*x2+self.c*u
        return np.array([dx1,dx2])

class Control:
    def __init__(self,b,c,k1,k2) -> None:
        self.b=b;self.c=c
        self.k1=k1;self.k2=k2
    def control(self,x1,x2,ddr,e1,e2):
        return 1/self.c*(np.sin(x1)+ self.b*x2 +ddr-self.k1*e1-self.k2*e2)

@dataclass
class Data:
    dx:np.ndarray
    y:float
    u:float
    r:float
    e1:float
    e2:float

class Closed:
    x0=np.array([pi/2,0])
    def __init__(self,b=0.03,c=1,k1=1,k2=1) -> None:
        self.params=(b,c,k1,k2)
    def __call__(self,t,x):
        return self.rhs(t,x).dx
    def rhs(self,t,x):
        (b,c,k1,k2)=self.params
        r=Source(omega=1/3)
        x1,x2 = x[0:2]
        control=Control(b,c,k1,k2)
        model=Pendulum(b=b,c=c)

        u=control.control(x1,x2,r.dd(t),x1-r(t),x2-r.d(t))
        dx=model.system(t,x1,x2,u)

        return Data(dx=dx,y=x1,u=u,r=r(t),e1=x1-r(t),e2=x2-r.d(t))
    def solve(self,t):
        sol=solve_ivp(self,[0,t],self.x0,dense_output=True,t_eval=np.linspace(0,t,1000))
        signals=[]
        for i,t in enumerate(sol.t):
            sig=self.rhs(t,sol.y[:,i])
            signals.append(sig)
        sol.sigs=Data(dx=np.array([sig.dx for sig in signals]),
                      y=np.array([sig.y for sig in signals]),
                      u=np.array([sig.u for sig in signals]),
                      r=np.array([sig.r for sig in signals]),
                      e1=np.array([sig.e1 for sig in signals]),
                      e2=np.array([sig.e2 for sig in signals]))
        return sol
x0=np.array([pi/2,0])

sol=dict()
nominal_low=Closed(b=0.03,c=1,k1=1,k2=1).solve(10)
nominal_high=Closed(b=0.03,c=1,k1=9,k2=3).solve(10)

perturbed_low=Closed(b=0.015,c=0.5,k1=1,k2=1).solve(10)
perturbed_high=Closed(b=0.015,c=0.5,k1=9,k2=3).solve(10)

# %%
plt.figure()
plt.subplot(2,2,1),plt.grid();plt.title("(a)")
plt.plot(nominal_low.t,nominal_low.sigs.y,'r',label='y')
plt.plot(nominal_low.t,nominal_low.sigs.r,'k',label='r')
plt.legend()
plt.subplot(2,2,2,);plt.grid();plt.title("(b)")
plt.plot(nominal_high.t,nominal_high.sigs.y,'b',label='y')
plt.plot(nominal_high.t,nominal_high.sigs.r,'k',label='r')
plt.legend()
plt.subplot(2,2,3,);plt.grid();plt.title("(c)")
plt.plot(perturbed_low.t,perturbed_low.sigs.r,'k',label='r')
plt.plot(perturbed_low.t,perturbed_low.sigs.y,'r',label='y (low gain)')
plt.plot(perturbed_high.t,perturbed_high.sigs.y,'b',label='y (high gain)')
plt.legend(fontsize=6)
plt.subplot(2,2,4);plt.grid();plt.title("(d)")
plt.plot(perturbed_low.t,perturbed_low.sigs.u,'r',label='u (low gain)')
plt.plot(perturbed_high.t,perturbed_high.sigs.u,'b',label='u (high gain)')
plt.legend()

plt.tight_layout()
plt.savefig('tracking.pdf')
# %%
