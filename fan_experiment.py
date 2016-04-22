import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np

from spl import getdecibels

def fan_experiment():
	x = [0,2,4,6,8,10]
	y = []
	for i in x:
		fname = 'audio_data/fan/{0}.WAV'.format(i)
		print fname
		data = getdecibels(fname, 1)
		y.append(data[0])

	xnew = np.linspace(0, 10, num=41, endpoint=True)
	f = interp1d(x, y)
	f2 = interp1d(x, y, kind='cubic')
	plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
	plt.legend(['data', 'linear', 'cubic'], loc='best')
	# plt.plot(,y)
	plt.show()