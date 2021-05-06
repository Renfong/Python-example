#%% load package
import numpy as np
import matplotlib.pyplot as plt

#%% example 1: simple second order fitting
# y=2x**2
xx = np.arange(-3,3,step=0.2)
yy = 2*xx**2 

yy +=  (np.random.random(len(xx))-0.5)  # add noise
plt.figure(1, dpi=150)
plt.plot(xx, yy, 'ro')

# curve fitting
lin_fit = np.polyfit(xx, yy, 2)
print(lin_fit)

x2 = np.arange(-3,3,step=.01)
y2 = np.polyval(lin_fit, x2)
plt.figure(1)
plt.plot(x2,y2, 'k')
plt.legend(['raw data','fitting curve'])
plt.legend(['raw data','fitting curve'])
plt.plot(x2[np.argmin(y2)], np.min(y2), 'b*', markersize=10)
plt.text(x2[np.argmin(y2)], np.min(y2)-1, 'min: (%.2f, %.2f)'%(x2[np.argmin(y2)], np.min(y2)))
plt.axis([-3,3,-2,20])
plt.show()

#%%===============================================================
#%% example 2
# y-y0 = a*(x-x0)**2
# --> y = ax**2 - 2a*x0*x + a*x0**2 + y0
# let a=-1, x0=1.2, y0=0.7, i.e. the maximum value is located at (1.2, 0.7)
# --> y = -1x**2 + 2.4x - 0.74

xx = np.arange(-3,3,step=0.2)
yy = -1*xx**2 + 2.4*xx - 0.74 
yy +=  (np.random.random(len(xx))-0.5)  # add noise
plt.figure(2, dpi=150)
plt.plot(xx, yy, 'ro')

# curve fitting
lin_fit = np.polyfit(xx, yy, 2)
print(lin_fit)

x2 = np.arange(-3,3,step=.01)
y2 = np.polyval(lin_fit, x2)
plt.figure(2)
plt.plot(x2,y2, 'k')
plt.legend(['raw data','fitting curve'])
plt.plot(x2[np.argmax(y2)], np.max(y2), 'b*', markersize=10)
plt.text(x2[np.argmax(y2)], np.max(y2)+1, 'max: (%.2f, %.2f)'%(x2[np.argmax(y2)], np.max(y2)))
plt.axis([-3,3,-20,3])
plt.show()

'''
It's noted that the 
x0 = lin_fit[1] / (-2*lin_fit[0])
y0 = y0 = lin_fit[2] - lin_fit[0] * x0**2
'''
