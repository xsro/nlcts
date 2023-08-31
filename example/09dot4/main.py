# plot the RHS for Delta_m
#%%
import numpy as np
import matplotlib.pyplot as plt

# %%
from sympy.abc import x,sigma
from sympy import sqrt,latex
num=2*sigma**3
den1=1+sigma*sqrt(sigma**2+4)
den2=sqrt(4*sigma**2+(sigma**2+1)**2)
rhs=num/den1/den2

x=np.linspace(0,10,1000)
y=np.array(list(map(lambda x: rhs.subs(sigma,x),x)))
max_index=np.argmax(y)

# %%
plt.figure(figsize=(8,4))
plt.plot(x,y,"b-")
plt.plot(x[max_index],y[max_index],"ro")
plt.text(x[max_index],y[max_index]+0.01,"({:.4f},{:.4f})".format(x[max_index],y[max_index]))
plt.text(4,0.17,'$'+latex(rhs)+'$',fontsize=20,color="blue")
plt.grid()
plt.xlabel(r'$\sigma$')
plt.ylabel(r'$RHS$')
plt.ylim(0,0.45)
plt.savefig("rhs.pdf",transparent=True)
# %%
