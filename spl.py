# from scipy.io.wavfile import read
# samprate, wavdata = read('mitra_1.wav')

import wavio
from math import log10, sqrt
from data import concourse_2_60, train_1_2_3_day_1_60, train_1_2_3_day_2_60, weekday_day1

def plot_data(y, factor=2, interpolate=True):
	x = range(len(y))
	print x,y
	import matplotlib.pyplot as plt
	from scipy.interpolate import interp1d
	import numpy as np


	if interpolate:
		xnew = np.linspace(0, len(y), num=len(y)*factor, endpoint=True)
		f = interp1d(x, y,bounds_error=False)
		print "first interpolation"
		f2 = interp1d(x, y, kind='cubic',bounds_error=False)
		print "second interpolation"
		plt.plot(x, y, '.', xnew, f(xnew), '-', xnew, f2(xnew), '--')
		plt.legend(['data', 'linear', 'cubic'], loc='best')
	else:
		plt.plot(x, y, 'o')
	plt.xlabel('Time')
	plt.ylabel('Sound Level')
	plt.show()	
	return None

def getdecibels(filename, chunks=None, chunk_factor=1):
	duration, samprate, sampwidth, wavdata = wavio.readwav(filename)


	if chunks==None:
		chunks = max(int(duration/60),2)*chunk_factor
	wavdata = wavdata.astype('int64')
	import numpy as np
	numchunks = chunks
	chunks = np.array_split(wavdata, numchunks)
	wavdata = 0 # clear out about a gig of data
	# print chunks**2
	# a = chunks[0]
	# b = np.square(a,dtype='int64')
	# print a.dtype
	# for i,j in zip(a,b):
	# 	print i,j, i**2
	dbs = [np.mean(chunk**2) for chunk in chunks]
	print "section 1"
	dbs = [20*log10( sqrt(np.mean(chunk**2)) ) for chunk in chunks]
	print "done dbs calculation"
	return dbs

def fan_experiment():
	x = [0,2,4,6,8,10]
	y = []
	for i in x:
		fname = 'audio_data/fan/{0}.WAV'.format(i)
		print fname
		data = getdecibels(fname, 1)
		y.append(data[0])
		# print i
	# print getdecibels('fan/0.WAV', 1)
	# print getdecibels('fan/2.WAV', 1)
	# print getdecibels('fan/4.WAV', 1)
	# print getdecibels('fan/6.WAV', 1)
	# print getdecibels('fan/8.WAV', 1)
	# print getdecibels('fan/10.WAV', 1)

	import matplotlib.pyplot as plt
	from scipy.interpolate import interp1d
	import numpy as np
	xnew = np.linspace(0, 10, num=41, endpoint=True)
	f = interp1d(x, y)
	f2 = interp1d(x, y, kind='cubic')
	plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
	plt.legend(['data', 'linear', 'cubic'], loc='best')
	# plt.plot(,y)
	plt.show()

if __name__ == '__main__':
	dbs = getdecibels('/Users/sag47/Downloads/Cecilia.WAV', chunk_factor=60)
	print dbs
	# plot_data(weekday_day1, factor=5, interpolate=True)
