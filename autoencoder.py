from engine import *
from util import *
from createTactics import *


#import matplotlib.pyplot as plt

'''
We don't really care how closely the new tactic resembles the old one
We only care if the reconstructed tactic is the correct type and is still legal
'''
def reconstructionLoss(input, output):

	if verifyKnightKingFork(output):
		return 10
	else:
		pass
def createSamples(numSamples, noIncludeSet=set()):
	numCreated = 0
	sampleSet = set()
	#sampleList = []
	while numCreated < numSamples:
		sample = createKnightKingFork()
		#print(sample)
		while sample in noIncludeSet or sample in sampleSet:
			sample = createKnightKingFork()
		# cast to pytorch tensor
		#sampleList.append(sample)
		sampleSet.add(sample)
		numCreated+=1
		#print('create ', numCreated, ' samples')

	return sampleSet

class KnightKingForkDataset(Dataset):
	def __init__(self, data):
		#trainingData, trainingSet = createSamples(10000)
		#testData, = createSamples(1000, trainingSet) 
		self.data = list(data)
	def __len__(self):
		return len(self.data)
	def __getitem__(self, i):
		return self.data[i]
#start = time.time()
trainingData = createSamples(10000)
trainingDataset = KnightKingForkDataset(trainingData)
testData = createSamples(1000, noIncludeSet=training_data)
testDataset  = KnightKingForkDataset(testData) 
#end = time.time()

print('took ', (end-start), ' seconds to create data')