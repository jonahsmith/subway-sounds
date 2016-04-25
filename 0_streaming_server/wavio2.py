from scikits.audiolab import Sndfile
import numpy as np


def readwav(fname):
	f = Sndfile(fname, 'r')
	data = np.array(f.read_frames(f.nframes), dtype=np.float64)
	f.close()
	return data
