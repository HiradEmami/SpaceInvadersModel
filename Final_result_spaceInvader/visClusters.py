import numpy as np
import sys
import matplotlib.pyplot as plt

def scatter(x, labels, participant):
	c1 = x[labels == 0]
	c1Idc = np.argwhere(labels == 0)
	c2 = x[labels == 1]
	c2Idc = np.argwhere(labels == 1)
	y = np.random.rand(len(x))
	area = np.pi*3
	colors = (1,0,0)
	fig = plt.figure()
	plt.scatter(c1, c1Idc, s=area, c=colors, alpha=0.5)
	colors = (0,1,0)
	plt.scatter(c2, c2Idc, s=area, c=colors, alpha=0.5)
	plt.title('Scatter plot: ' + participant)
	plt.xlabel('x')
	plt.ylabel('y')
	
	fig.savefig(participant + '.png')
	plt.show()


if __name__ == "__main__":
	fileDir = sys.argv[1]
	parts = fileDir.split('/')
	participant = parts[0]
	print participant
	logData = np.loadtxt(fileDir, dtype = 'str')
	
	
	values = logData[:,0].astype(float)
	label = logData[:,1].astype(float)
	cluster1 = logData[:,2].astype(float)
	cluster2 = logData[:,3].astype(float)
	
	
	scatter(values, label, participant)
