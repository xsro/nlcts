#%%
import numpy as np
import matplotlib.pyplot as plt

x=np.arange(-8,8,0.01)
y=np.arange(-3,3,0.01)
X,Y=np.meshgrid(x,y)
V=X**2/(1+X**2)+Y**2 

#%% Plot
plt.figure(figsize=(7,3))
plt.contourf(X,Y,V,
    cmap="summer")
CS=plt.contour(X,Y,V,
    levels=[0,0.1,0.5,1,2,4,6,9,12],
    colors='k',)
plt.xlim(-8,8)
plt.ylim(-3,3)
plt.clabel(CS,inline=1,fontsize=10)
plt.xlabel(r'$x_1$')
plt.ylabel(r'$x_2$')
plt.tight_layout()
plt.savefig("radial_unboundedness.pdf",transparent=True,bbox_inches='tight',pad_inches=0)
# %%
