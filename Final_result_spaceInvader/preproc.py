import numpy as np
import os



participants = []

for root, dirs, files in os.walk(".", topdown=False):
	for dir in dirs:
		participants.append(dir)
		
		
def strarray(length, value):
	arr = np.chararray((length, 1), itemsize=10)
	for idx in range(length):
		arr[idx] = value
	return arr

def standardize(data):
	data = data.astype(float)
	m = np.mean(data)
	std = np.std(data)
	return (data - m) / std

nData = 0
totalData = []
totalLogData = []
for part in participants:
	try:
		logData = np.loadtxt(part + '/logData.csv', dtype = 'str')
		logData[:,0] = standardize(logData[:,0])
		evaluation = np.loadtxt(part + '/evaluationList.csv', dtype = 'str')
		print evaluation.shape
		responses = np.loadtxt(part + '/responseList.csv', dtype = 'str')
		responses = np.reshape(responses, (len(responses), 1))
		print responses.shape
		total = np.concatenate((evaluation, responses), axis = 1)
		names = strarray(len(total), part)
		print names.shape
		total = np.concatenate((total, names), axis = 1)
		logData = np.concatenate((logData, strarray(len(logData), part)), axis = 1)

		if nData == 0:
			totalData = total
			totalLogData = logData
		else:
			totalData = np.concatenate((totalData, total), axis = 0)
			totalLogData = np.concatenate((totalLogData, logData), axis = 0)
		nData += 1
	except:
		print part + " is invalid.."

np.savetxt('totaldata.csv', totalData, delimiter = ', ',header =  "happiness, mode, stage, rt, name", fmt = '%s', comments='')
np.savetxt('totallogdata.csv', totalLogData, delimiter = ', ',header =  "dil, label, c1, c2, mode, stage, name", fmt = '%s', comments='')


