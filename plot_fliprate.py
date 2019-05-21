import numpy as np
from matplotlib import pyplot as plt

data = np.load('sensordata.npz')
samplet_rec = data['samplet_rec']
val_rec = data['val_rec']
flipt_rec = data['flipt_rec']


plt.plot(samplet_rec-samplet_rec[0], val_rec)
plt.title("Light sensor value")
plt.ylabel("Intensity (0-1)")
plt.xlabel("Time(s)")

plt.figure()
fh = plt.hist(np.diff(flipt_rec), 20) #create a histogram of the duration bewteen flips
plt.title("%d flips detected in %.3f secs."%(len(flipt_rec), samplet_rec[-1]-samplet_rec[0]))
plt.ylabel("Frequency")
plt.xlabel("Duration")
plt.show()
