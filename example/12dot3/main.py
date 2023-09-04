#%% example 12.3 
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

class Model:
    def __init__(self,epsilon=None,sat=False) -> None:
        def sat_(x):
            return np.sign(x)*np.minimum(np.abs(x),1)
        self.sat = sat_ if sat else lambda x:x
        self.epsilon = epsilon
    def system(x:np.ndarray,u:float):
        x1,x2 = x[0:2].tolist()
        x1_dot = x2
        x2_dot = x2**3 + u
        return np.array([x1_dot,x2_dot])
    def state_feedback_control(x:np.ndarray):
        x1,x2 = x.tolist()
        u = -x2**3-x1-x2
        return u
    def state_observer(self,x:np.ndarray):
        x1,x2 = x[0:2].tolist()
        xhat1,xhat2 = x[2:4].tolist()
        y=x1
        dxhat1 = xhat2 + (2/self.epsilon)*(y-xhat1)
        dxhat2 = (1/self.epsilon**2)*(y-xhat1)
        return np.array([dxhat1,dxhat2])
    def rhs1(self,t,x:np.ndarray):
        u = Model.state_feedback_control(x)
        u=self.sat(u)
        dx = Model.system(x,u)
        return dx
    def rhs2(self,t,x:np.ndarray):
        u = Model.state_feedback_control(x[2:4])
        u=self.sat(u)
        dx = Model.system(x,u)
        dxhat = self.state_observer(x)
        return np.concatenate([dx,dxhat])
    
x0=np.array([0.1,0])
xhat0=np.array([0,0])
t_eval=np.linspace(0,10,10000)

model = Model()
sol1=solve_ivp(model.rhs1,[0,10],x0,t_eval=t_eval)
model = Model(epsilon=0.1)
sol2=solve_ivp(model.rhs2,[0,10],np.concatenate([x0,xhat0]),t_eval=t_eval)
model = Model(epsilon=0.01)
sol3=solve_ivp(model.rhs2,[0,10],np.concatenate([x0,xhat0]),t_eval=t_eval)
model = Model(epsilon=0.005)
sol4=solve_ivp(model.rhs2,[0,10],np.concatenate([x0,xhat0]),t_eval=t_eval)
#%% compare SFB and OFB
plt.figure()
plt.subplot(3,1,1)
plt.plot(sol1.t,sol1.y[0,:],'-')
plt.plot(sol2.t,sol2.y[0,:],'--')
plt.plot(sol3.t,sol3.y[0,:],'--')
plt.plot(sol4.t,sol4.y[0,:],'--')
plt.ylabel("$x_1$")
plt.subplot(3,1,2)
plt.plot(sol1.t,sol1.y[1,:])
plt.plot(sol2.t,sol2.y[1,:],'--')
plt.plot(sol3.t,sol3.y[1,:],'--')
plt.plot(sol4.t,sol4.y[1,:],'--')
plt.ylabel("$x_2$")
  
plt.subplot(3,1,3)
def generate_u(sol):
    return np.array([Model.state_feedback_control(sol.y[-2:,j]) for j in range(sol.y.shape[1])])
u={k:generate_u(v) for k,v in {"1":sol1,"2":sol2,"3":sol3, "4":sol4}.items()}
plt.plot(sol1.t,u["1"])
plt.plot(sol2.t,u["2"],'--')
plt.plot(sol3.t,u["3"],'--')
plt.plot(sol4.t,u["4"],'--')
plt.ylabel("$u$")
plt.xlim(0,0.1)
plt.tight_layout()
plt.legend([
    "SFB","OFB $\epsilon=0.1$","OFB $\epsilon=0.01$","OFB $\epsilon=0.005$"
    ])
plt.savefig("SFB_vs_OFB.pdf")
# %% Simuate OFB with epsilon=0.004
model = Model(epsilon=0.004)
sol5=solve_ivp(model.rhs2,[0,10],np.concatenate([x0,xhat0]),t_eval=t_eval)
plt.figure()
plt.subplot(3,1,1)
plt.plot(sol5.t,sol5.y[0,:],'-')
plt.ylabel("$x_1$")
plt.subplot(3,1,2)
plt.plot(sol5.t,sol5.y[1,:],'-')
plt.ylabel("$x_2$")
plt.subplot(3,1,3)
plt.plot(sol5.t,generate_u(sol5),'-')
plt.ylabel("$u$")
plt.savefig("OFB_epsilon_0.004.pdf")
# %% OFB with saturation
model1 = Model(sat=True)
model2 = Model(epsilon=0.1,sat=True)
model3 = Model(epsilon=0.01,sat=True)
model4 = Model(epsilon=0.001,sat=True)
models={"2":model2,"3":model3, "4":model4}
sols={"1":solve_ivp(model1.rhs1,[0,10],x0,t_eval=t_eval)}
for k,v in models.items():
    sols[k]=solve_ivp(v.rhs2,[0,10],np.concatenate([x0,xhat0]),t_eval=t_eval)
#%% Plot 
plt.figure()
plt.subplot(3,1,1)
plt.plot(sols['1'].t,sols['1'].y[0,:],'-')
plt.plot(sols['2'].t,sols['2'].y[0,:],'--')
plt.plot(sols['3'].t,sols['3'].y[0,:],'--')
plt.plot(sols['4'].t,sols['4'].y[0,:],'--')
plt.ylabel("$x_1$")
plt.legend([
    "SFB","OFB $\epsilon=0.1$","OFB $\epsilon=0.01$","OFB $\epsilon=0.001$"
    ],loc="upper right")
plt.subplot(3,1,2)
plt.plot(sols['1'].t,sols['1'].y[1,:])
plt.plot(sols['2'].t,sols['2'].y[1,:],'--')
plt.plot(sols['3'].t,sols['3'].y[1,:],'--')
plt.plot(sols['4'].t,sols['4'].y[1,:],'--')
plt.ylabel("$x_2$")
  
plt.subplot(3,1,3)
def generate_u(sol):
    u=np.zeros((sol.y.shape[1],))
    for i in range(sol.y.shape[1]):
        u[i] = Model.state_feedback_control(sol.y[-2:,i])
        u[i]=model1.sat(u[i])
    return u
plt.plot(sols['1'].t,generate_u(sols['1']))
plt.plot(sols['2'].t,generate_u(sols['2']),'--')
plt.plot(sols['3'].t,generate_u(sols['3']),'--')
plt.plot(sols['4'].t,generate_u(sols['4']),'--')
plt.ylabel("$u$")
plt.xlim(0,0.1)
plt.tight_layout()

plt.savefig("SFB_vs_OFB_sat.pdf")

# %%
