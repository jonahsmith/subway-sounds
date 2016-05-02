'''
SPL.py

Calculate Sound Pressure Levels

'''
import numpy as np
from math import log10, sqrt

from A_weighting import A_weighting
import wavio

def plot_data(y, factor=2, interpolate=True):
	'''
	Plot the data using the matplotlib library.

	Arguments:
	interpolate : Wheter we so
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


def rms_flat(a):  # from matplotlib.mlab
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
		y = lfilter(b, a, x)
		dbs_a.append(20*np.log10(rms_flat(y)))

	dbs_orig = [20*log10( sqrt(np.mean(chunk**2)) ) for chunk in chunks]

	return dbs,dbs_a,dbs_orig

if __name__ == '__main__':
	# Uncomment the next line to use precalculated values.
	#from data import concourse_2_60, train_1_2_3_day_1_60, train_1_2_3_day_2_60, weekday_day1

	dbs,dbs_a,dbs_orig = getdecibels('/Users/sag47/Downloads/Cecilia.WAV', chunk_factor=60)
	print dbs
	print dbs_a
	print dbs_orig
	# plot_data(weekday_day1, factor=5, interpolate=True)
