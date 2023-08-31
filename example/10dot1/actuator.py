import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from functools import partial

# Define the model
class Pendulum:
    def __init__(self,b,c) -> None:
        self.b=b;self.c=c
        def control1(x1,x2):
            s=x1+x2
            u=-(2.5+2*np.abs(x2))*np.sign(s)
            return u
        def control2(x1,x2):
            s=x1+x2
            u=1.2*np.cos(x1)-1.2*x2-(1+0.8*np.abs(x2))*np.sign(s)
            return u
        self.rhs1=partial(self.rhs,control=control1)
        self.rhs2=partial(self.rhs,control=control2)
    def rhs(self,t:float,x:np.ndarray,control=lambda x1,x2:0):
        # pass sliding model control to a filter 1/(0.01s+1)^2
        x1,x2,u,du = x.tolist()
        dx1=x2
        u0=control(x1,x2)
        ddu=1/(1e-4)*(u0-u-0.02*du)
        dx2=-np.cos(x1)-self.b*x2+self.c*u
        return np.array([dx1,dx2,du,ddu])
    
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
sol=solve_ivp(p.rhs1,[0,10],np.array([*x0,0,0]))
#%%
sol2=solve_ivp(p.rhs2,[0,10],np.array([*x0,0,0]),method="RK45",t_eval=np.linspace(0,10,int(1e6)))

#%%
plt.subplot(2,2,1)
(theta,dtheta)=Pendulum.state_to_output(sol.y[0,:],sol.y[1,:])
(theta2,dtheta2)=Pendulum.state_to_output(sol2.y[0,:],sol2.y[1,:])
plt.plot(sol.t,theta)
plt.plot(sol2.t,theta2)
plt.ylabel("$\\theta$")
plt.xlabel("time")
plt.yticks([0,np.pi/4,np.pi/2],["0","$\\pi$/4","$\\pi$/2"])
plt.grid(axis="y")

plt.subplot(2,2,2)
s=sol.y[0,:]+sol.y[1,:]
s2=sol2.y[0,:]+sol2.y[1,:]
plt.plot(sol.t,s)
plt.plot(sol2.t,s2)
plt.ylabel("$s$")
plt.xlabel("time")
plt.xlim(0,3)
plt.grid(axis="y")

plt.subplot(2,2,3)
(theta,dtheta)=Pendulum.state_to_output(sol.y[0,:],sol.y[1,:])
(theta2,dtheta2)=Pendulum.state_to_output(sol2.y[0,:],sol2.y[1,:])
plt.plot(sol.t,theta)
plt.plot(sol2.t,theta2)
plt.ylabel("$\\theta$")
plt.xlabel("time")
plt.xlim(9,10)
plt.ylim(1.563,1.572)
values=np.arange(1.563,1.572,0.003).tolist()
labels=list(map(lambda x:format(x,".3f"),values))
plt.yticks([*values,np.pi/2],[*labels,"$\\pi$/2"])
plt.grid(axis="y")

plt.subplot(2,2,4)
s=sol.y[0,:]+sol.y[1,:]
s2=sol2.y[0,:]+sol2.y[1,:]
plt.plot(sol.t,s)
plt.plot(sol2.t,s2)
plt.ylabel("$s$")
plt.xlabel("time")
plt.xlim(9,10)
plt.ylim(-15e-3,5e-3)
plt.grid(axis="y")

plt.tight_layout()
plt.savefig("unmodeled_actuator.pdf", transparent = True)
#%%