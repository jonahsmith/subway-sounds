'''
SPL.py

Calculate Sound Pressure Levels

'''
import numpy as np
from math import log10, sqrt
import json

from A_weighting import A_weighting
import wavio
from scipy.signal import lfilter

def plot_data(y, factor=4, interpolate=True):
	'''
	Plot the data using the matplotlib library.

	Arguments:
	interpolate : Wheter we do linear and cubic interpolation to see more refined trends in data
	factor : the interpolation factor. This is basically the number of points we would add between two samples
			 to smooth things out. Higher is better, but computationally more intense. Practically, a value
			 between 3-5 should be fine.
	'''
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


def rms_flat(a):
    """
    Return the root mean square of all the elements of *a*, flattened out.
    """
    return np.sqrt(np.mean(np.absolute(a)**2))

def getdecibels(filename, chunks=None, chunk_factor=1):
	'''
	getdecibels function takes a filename and produces the decibel readings from it.

	TODO : It returns a list right now, it would be nice if it could be converted into a generator

	Arguments :
	chunks: default None. The number of chunks to divide the audio file into.

	chunk_factor : If chunks is not provided, we split the audio files according to the
					chunk_factor. This essentially refers to number of chunks per minute.
					If the total duration is less than a minute, we will take 2 chunks.
	'''

	#get data from the wavio.
	#NOTE : The original wavio module does not return the duration.
	duration, samprate, sampwidth, wavdata = wavio.readwav(filename)


	#figure out exactly how many chunks we need to split it.
	if chunks==None:
		chunks = max(int(duration/60),2)*chunk_factor


	#we need to convert the wavdata into 64 bits because calculating the decibels require squaring it
	# If it's stored as a 32 bit int, the integer will overflow.
	wavdata = wavdata.astype('int64')

	#Split the dataset into chunks
	chunks = np.array_split(wavdata, chunks)

	# clear out about a gig of data. This simple line saved a ton of trouble while dealing with large files.
	wavdata = 0

	#dB SPL is basically dB = 20 * log10(amplitude)
	dbs = []
	b,a = A_weighting(samprate)

	dbs_a = []
	for chunk in chunks:
		dbs.append(20*np.log10(rms_flat(chunk)))

		y = lfilter(b, a, chunk)
		dbs_a.append(20*np.log10(rms_flat(y)))


	return dbs,dbs_a

if __name__ == '__main__':

	path = '/Users/sag47/Downloads/snippets/5yards.wav'


	dbs, dbs_a = getdecibels(path, chunk_factor=60)
	data = {'path': path, "Original":dbs, "A-weighted": dbs_a}
	with open(path+'.json','w') as outfile:
		json.dump(data, outfile)
