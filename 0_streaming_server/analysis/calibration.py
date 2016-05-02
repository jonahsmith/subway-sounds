'''
Calibration.py file to calibrate the sensor

The calibration is done using a set of audio files taken at fixed distances.

As we know, the Sound intesity varies as a squared-inverse factor of distance,
and therefore, we should see a linear decline in the SPL with distance. We 
calculate this linear decline and use linear regression to find out the intensity
at the nozzle
'''


files = ['/Users/sag47/Downloads/snippets/5yards.wav','/Users/sag47/Downloads/snippets/10yards.wav','/Users/sag47/Downloads/snippets/15yards.wav','/Users/sag47/Downloads/snippets/20yards.wav','/Users/sag47/Downloads/snippets/25yards.wav', '/Users/sag47/Downloads/snippets/30yards.wav']
x = [5,10,15,20,25,30]


from spl import getdecibels, plot_data

from sklearn import linear_model

import matplotlib.pyplot as plt
import numpy as np

print '\n'.join(files)
dbs = []
for f in files:

	#getdecibels send out the normal as well as A weighted version of the decibel reading
	# We use the A weighted one
	db,dba = getdecibels(f, chunks=1)
	dbs.append(dba)


# Linear Regression to figure out the sound at the nozzle.
X = np.array(x)
X = X.reshape(6,1)
Y = np.array(dbs)

regr = linear_model.LinearRegression()
regr.fit(X, Y)
print 
print('Coefficients: \n', regr.coef_)
print "at zero distance :",regr.predict([0])


# Plot the original data along with the regression line
plt.scatter(X, Y,  color='black')
plt.plot(X, regr.predict(X), color='blue',
         linewidth=3)

print 
plt.show()
# plot_data(dbs, factor=5, interpolate=False)