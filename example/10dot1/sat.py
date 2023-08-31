import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from functools import partial

# Define the model
class Pendulum:
    def __init__(self,b,c,mu) -> None:
        self.b=b;self.c=c;self.mu=mu
        
        
        self.rhs1=partial(self.rhs,unmodeled_actuator=False)
        self.rhs2=partial(self.rhs,unmodeled_actuator=True)
    def rhs(self,t:float,x:np.ndarray,unmodeled_actuator=False):
        # pass sliding model control to a filter 1/(0.01s+1)^2
        x1,x2,u,du = x.tolist()
        dx1=x2
        u0=self.control(x1,x2)
        ddu=1/(1e-4)*(u0-u-0.02*du)
        u_in_use=u if unmodeled_actuator else u0
        dx2=-np.cos(x1)-self.b*x2+self.c*u_in_use
        return np.array([dx1,dx2,du,ddu])
    
    def control(self,x1,x2):
        def sat(y):
            return np.clip(y,-1,1)
        s=x1+x2
        u=-(2.5+2*np.abs(x2))*sat(s/self.mu)
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
p1=Pendulum(b,c,0.1)
p2=Pendulum(b,c,0.001)
#%%
sol=solve_ivp(p1.rhs1,[0,10],np.array([*x0,0,0]))
sol2=solve_ivp(p2.rhs1,[0,10],np.array([*x0,0,0]))
sol=solve_ivp(p1.rhs2,[0,10],np.array([*x0,0,0]))
sol2=solve_ivp(p2.rhs2,[0,10],np.array([*x0,0,0]))

#%%
plt.subplot(2,2,1)
(theta,dtheta)=Pendulum.state_to_output(sol.y[0,:],sol.y[1,:])
(theta2,dtheta2)=Pendulum.state_to_output(sol2.y[0,:],sol2.y[1,:])
plt.plot(sol.t,theta,"--",label="$\\mu=0.1$")
plt.plot(sol2.t,theta2,label="$\\mu=0.001$")
plt.legend()
plt.ylabel("$\\theta$")
plt.xlabel("time")
plt.yticks([0,np.pi/4,np.pi/2],["0","$\\pi$/4","$\\pi$/2"])
plt.grid(axis="y")
plt.title("(a)")

plt.subplot(2,2,2)
s=sol.y[0,:]+sol.y[1,:]
s2=sol2.y[0,:]+sol2.y[1,:]
plt.plot(sol.t,s,"--",label="$\\mu=0.1$")
plt.plot(sol2.t,s2,label="$\\mu=0.001$")
plt.legend()
plt.ylabel("$s$")
plt.xlabel("time")
plt.xlim(9.5,10)
plt.ylim(-0.1,0.1)
plt.grid(axis="y")
plt.title("(b)")

plt.subplot(2,2,3)
(theta,dtheta)=Pendulum.state_to_output(sol.y[0,:],sol.y[1,:])
(theta2,dtheta2)=Pendulum.state_to_output(sol2.y[0,:],sol2.y[1,:])
plt.plot(sol.t,theta,"--",label="$\\mu=0.1$")
plt.plot(sol2.t,theta2,label="$\\mu=0.001$")
plt.legend()
plt.ylabel("$\\theta$")
plt.xlabel("time")
plt.yticks([0,np.pi/4,np.pi/2],["0","$\\pi$/4","$\\pi$/2"])
plt.grid(axis="y")
plt.title("(c)")

plt.subplot(2,2,4)
s=sol.y[0,:]+sol.y[1,:]
s2=sol2.y[0,:]+sol2.y[1,:]
plt.plot(sol.t,s,"--",label="$\\mu=0.1$")
plt.plot(sol2.t,s2,label="$\\mu=0.001$")
plt.legend()
plt.ylabel("$s$")
plt.xlabel("time")
plt.xlim(9.5,10)
plt.ylim(-0.1,0.1)
plt.grid(axis="y")
plt.title("(d)")

plt.tight_layout()
plt.savefig("sat.pdf", transparent = True)
# %%
