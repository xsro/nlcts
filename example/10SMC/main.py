import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# Define the model
class Pendulum:
    def __init__(self,b,c) -> None:
        self.b=b;self.c=c
    def rhs(self,t:float,x:np.ndarray):
        x1,x2 = x.tolist()
        dx1=x2 
        dx2=-np.cos(x1)-self.b*x2+self.c*self.control(x1,x2)
        return np.array([dx1,dx2])
    def rhs2(self,t:float,x:np.ndarray):
        # pass sliding model control to a filter 1/(0.1s+1)
        x1,x2,u = x.tolist()
        dx1=x2
        u0=self.control(x1,x2)
        du=1/0.1*(u0-u)
        #TODO: Should we use the filtered u as control input? 
        # The textbook only discusses the filtered u and doesn't mention 
        # whether we should use the filtered u in simulation or not.
        # From simulation, we can see the chattering phenomenon still exists
        # and even worse when use the filtered u 
        # change u0 to u in the next line to see the difference
        dx2=-np.cos(x1)-self.b*x2+self.c*u0
        return np.array([dx1,dx2,du])
    def control(self,x1,x2):
        s=x1+x2
        u=-(2.5+2*np.abs(x2))*np.sign(s)
        return u
    def state_to_output(x1,x2):
        theta=x1+np.pi/2
        dtheta=x2
        return (theta,dtheta)
    def output_to_state(theta,dtheta):
        x1=theta-np.pi/2
        x2=dtheta
        return (x1,x2)
    
b=0.01
c=0.5
theta0=dtheta0=0
x0=Pendulum.output_to_state(theta0,dtheta0)
p=Pendulum(b,c)
#%%
sol=solve_ivp(p.rhs,[0,10],np.array(x0),t_eval=np.linspace(0,10,int(1e5)))
#%%
sol2=solve_ivp(p.rhs2,[0,10],np.array([*x0,0]),t_eval=np.linspace(0,10,int(1e6)))

#%%
plt.subplot(2,2,1)
(theta,dtheta)=Pendulum.state_to_output(sol.y[0,:],sol.y[1,:])
plt.plot(sol.t,theta)
plt.ylabel("$\\theta$")
plt.xlabel("time")
plt.yticks([0,np.pi/4,np.pi/2],["0","$\\pi$/4","$\\pi$/2"])
plt.grid(axis="y")

plt.subplot(2,2,2)
s=sol.y[0,:]+sol.y[1,:]
plt.plot(sol.t,s)
plt.ylabel("$s$")
plt.xlabel("time")
plt.xlim(0,1)

plt.subplot(2,2,3)
u=np.array(list(map(lambda x:p.control(x[0],x[1]),zip(sol.y[0,:],sol.y[1,:]))))
plt.plot(sol.t,u)
plt.xlim(0,1)
plt.ylim(-5,5)
plt.ylabel("$u$")
plt.xlabel("time")

plt.subplot(2,2,4)
plt.plot(sol2.t,sol2.y[2,:])
plt.xlim(0,10)
plt.ylabel("Filtered $u$")
plt.xlabel("time")

plt.tight_layout()
plt.savefig("basic.pdf", transparent = True)
#%%