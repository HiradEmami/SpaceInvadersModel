import numpy as np


def distance(a, b):
   return abs(a - b)

##assumes data to be a N x D matrix, where N is # samples, and D the dimensionality 
def kmeans(data, k, nIters):
   nData = len(data)
   dims = len(data[0])
   np.random.shuffle(data)
   protos = np.zeros((k, dims), dtype = float)
   protos2 = np.zeros((k, dims), dtype = float)
   nMembers = np.zeros((k, dims), dtype = float)
   
   for proto in range(k):
      protos[proto] = data[proto]
   
   for epoch in range(nIters):
      for dIdx in range(nData):
         minDist = 99999999
         bestCluster = -1
         for cluster in range(k):
            dist = distance(protos[cluster], data[dIdx])
            if dist < minDist:
               minDist = dist
               bestCluster = cluster
         if bestCluster == -1:
            raise "Invalid cluster allocation"
         protos2[bestCluster] += data[dIdx]
         nMembers[bestCluster] += 1
      for cluster in range(k):
         protos2[cluster] /= nMembers[cluster]
      protos = protos2.copy()
      protos2 = np.zeros((k, dims), dtype = float)
      nMembers = np.zeros((k, dims), dtype = float)
   return protos

def lvq(protos, data, learningRate = 0.002):
   k = len(protos)
   dims = len(protos[0])
   minDist = 99999999
   nearestCluster = -1
   for cluster in range(k):
      dist = distance(protos[cluster], data)
      if dist < minDist:
         minDist = dist
         nearestCluster = cluster
   if nearestCluster == -1:
      raise "invalid cluster allocation in LVQ.."
   protos[nearestCluster] += learningRate * data
   return protos, nearestCluster
 
if __name__ == "__main__":
  randomStuff = np.random.randint(0,1200, (2000, 1))
  
  protos = kmeans(randomStuff, 2, 20)
  for idx in range(2000):
    pupil = np.random.randint(0,1200,(1,1))
    protos, nearest = lvq(protos, pupil[0])
    print nearest