import numpy as np

class Classifier:
  
  def __init__(self, data):
    self.desiredListLength = 20
    self.protos = self.kmeans(data, 2, 5)
    
    if self.protos[0] > self.protos[1]:
      buff =  self.protos[0].copy()
      self.protos[0] = self.protos[1].copy()
      self.protos[1] = buff
    print self.protos
    self.resultList = []
  
  def getResult(self):
    return sum(self.resultList), self.desiredListLength
    
    
  def listIsready(self):
    return len(self.resultList) == self.desiredListLength
  
  def distance(self, a, b):
    return abs(a - b)
  
  
  def update(self, measurement):
    result, nearestCluster = self.lvq(measurement)
    if self.listIsready():
      self.resultList.pop(0)
    self.resultList.append(result)
    return result, nearestCluster

  ##assumes data to be a N x D matrix, where N is # samples, and D the dimensionality 
  def kmeans(self, data, k, nIters):
    nData = len(data)
    np.random.shuffle(data)
    protos = np.zeros((k), dtype = float)
    protos2 = np.zeros((k), dtype = float)
    nMembers = np.zeros((k), dtype = float)
    
    for proto in range(k):
        protos[proto] = data[proto]
    
    for epoch in range(nIters):
        for dIdx in range(nData):
          minDist = 99999999
          bestCluster = -1
          for cluster in range(k):
              dist = self.distance(protos[cluster], data[dIdx])
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
        protos2 = np.zeros((k), dtype = float)
        nMembers = np.zeros((k), dtype = float)
        
    
    return protos

  def lvq(self, data, learningRate = 0.002):
    k = len(self.protos)
    minDist = 99999999
    nearestCluster = -1
    for cluster in range(k):
        dist = self.distance(self.protos[cluster], data)
        if dist < minDist:
          minDist = dist
          nearestCluster = cluster
    if nearestCluster == -1:
        raise "invalid cluster allocation in LVQ.."
    self.protos[nearestCluster] += learningRate * (data - self.protos[nearestCluster])
    return nearestCluster, self.protos[nearestCluster]
  
if __name__ == "__main__":
  randomStuff = np.loadtxt('logdata.csv', delimiter = ',') # = np.random.randint(0,1200, (2000, 1))
  classifier = Classifier(randomStuff)
 
  #for idx in range(2000):
  #  pupil = np.random.randint(0,1200,(1,1))
  #  classifier.update(pupil[0])
 