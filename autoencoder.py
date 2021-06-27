from engine import *
from util import *
from createTactics import *
import time
import vae
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torchvision

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


start = time.time()
trainingData = createSamples(10000)

data = torch.utils.data.DataLoader(
	torchvision.datasets.MNIST('./data', transform=torchvision.transforms.ToTensor(),download=True),
	batch_size=128,
	shuffle=True
	)
for x, y in data:
	x = torch.flatten(x, start_dim=1)
	print(x.shape)
	break

trainingDataset = KnightKingForkDataset(trainingData)
testData = createSamples(1000, noIncludeSet=trainingData)

trainingDataset = list(trainingDataset)
trainingDataset = [i / 120 for i in trainingDataset]
testDataset  = KnightKingForkDataset(testData) 
end = time.time()

print('took ', (end-start), ' seconds to create data')

train_dataloader = DataLoader(trainingDataset, batch_size=128, shuffle=True)
for x in train_dataloader:
	x = torch.flatten(x, start_dim=1)
	print(x.shape)
	break

latent_dims = 2
ae = vae.VariationalAutoencoder(latent_dims)
ae = vae.train_vae(ae, train_dataloader, epochs=50)
torch.save(ae, "saved_models/chess_ae.pkl")
vae.plot_latent(ae, train_dataloader)
#ae = torch.load("saved_models/chess_ae.pkl")

for x in train_dataloader:
	print(ae.encoder(x))
	break

z = torch.Tensor([[0.3186, 0.4610]])
x_hat = ae.decoder(z)
x_hat = x_hat.reshape(8, 8)
print(x_hat * 120)