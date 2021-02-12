import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d
import codecs, json

#bounds of our grid 
xbounds1 = 29.979508
xbounds2 = 30.660661
ybounds1 = -97.980544
ybounds2 = -97.299391

#space between points
xwidth = abs(xbounds1-xbounds2)/16
ywidth = abs(ybounds1-ybounds2)/16
#space between the interpolated points
xwidth_fine = abs(xbounds1-xbounds2)/48
ywidth_fine = abs(ybounds1-ybounds2)/48

#create numpy arrays
x = np.arange(xbounds1, xbounds2, xwidth)
y = np.arange(ybounds1, ybounds2, ywidth)

x_fine = np.arange(xbounds1, xbounds2, xwidth_fine)
y_fine = np.arange(ybounds1, ybounds2, ywidth_fine)

#the original meshgrid
X,Y = np.meshgrid(x,y)

#with this information we can start creating requests
#but we already have ready made results

file_path = "Z_array.json" 
obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
Z_array = json.loads(obj_text)
Z_array = np.array(Z_array)
Z=Z_array

#we can use the interp2d function to find values for the interpolated grid
f = interp2d(X, Y, Z, kind='linear')

#the interpolated meshgrid
X_fine,Y_fine = np.meshgrid(x_fine,y_fine, sparse=True)
#interp2d creates an array of interpolated values
Z_fine = f(x_fine, y_fine)

#plotting a graph of our interpolated model
fig = plt.figure()
ax = fig.gca(projection='3d')
plt.gca().invert_xaxis()
surf = ax.plot_surface(X_fine, Y_fine, Z_fine, rstride=1, cstride=1, cmap=cm.plasma)
plt.show()