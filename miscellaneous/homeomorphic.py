# %% a sphere without north pole S^2/N is homeomorphic to R^2
import numpy as np
import matplotlib.pyplot as plt

plt.figure()
x=np.linspace(-10,10,1000)
r=np.sqrt(1-x**2)/(1-x)
plt.plot(x,r)
# %%
