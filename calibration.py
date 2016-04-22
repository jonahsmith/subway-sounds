from spl import getdecibels, plot_data

from sklearn import linear_model

import matplotlib.pyplot as plt
import numpy as np

files = ['/Users/sag47/Downloads/snippets/5yards.wav','/Users/sag47/Downloads/snippets/10yards.wav','/Users/sag47/Downloads/snippets/15yards.wav','/Users/sag47/Downloads/snippets/20yards.wav','/Users/sag47/Downloads/snippets/25yards.wav', '/Users/sag47/Downloads/snippets/30yards.wav']
x = [5,10,15,20,25,30]

print '\n'.join(files)
dbs = []
for f in files:
	dbs.append(getdecibels(f, chunks=1))


X = np.array(x)
X = X.reshape(6,1)
Y = np.array(dbs)
print X.shape, Y.shape
regr = linear_model.LinearRegression()
regr.fit(X, Y)
print 
print('Coefficients: \n', regr.coef_)

plt.scatter(X, Y,  color='black')
plt.plot(X, regr.predict(X), color='blue',
         linewidth=3)


print "at zero distance"
print regr.predict([0])
plt.show()
# plot_data(dbs, factor=5, interpolate=False)