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


nData = 0
totalData = []
for part in participants:
	try:
		evaluation = np.loadtxt(part + '/evaluationList.csv', dtype = 'str')
		print evaluation.shape
		responses = np.loadtxt(part + '/responseList.csv', dtype = 'str')
		responses = np.reshape(responses, (len(responses), 1))
		print responses.shape
		total = np.concatenate((evaluation, responses), axis = 1)
		names = strarray(len(total), part)
		print names.shape
		total = np.concatenate((total, names), axis = 1)

		if nData == 0:
			totalData = total
		else:
			totalData = np.concatenate((totalData, total), axis = 0)
		nData += 1
	except:
		print part + " is invalid.."

np.savetxt('totaldata.csv', totalData, delimiter = ', ',header =  "happiness, mode, stage, rt, name", fmt = '%s', comments='')
