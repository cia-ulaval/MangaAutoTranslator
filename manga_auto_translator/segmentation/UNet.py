from torch.nn import ConvTranspose2d
from torch.nn import Conv2d
from torch.nn import MaxPool2d
from torch.nn import Module
from torch.nn import ModuleList
from torch.nn import ReLU
from torchvision.transforms import CenterCrop
from torch.nn import functional as F
import torch
import cv2
import numpy as np

class Block(Module):
	def __init__(self, inChannels, outChannels):
		super().__init__()
		self.conv1 = Conv2d(inChannels, outChannels, 3)
		self.relu = ReLU()
		self.conv2 = Conv2d(outChannels, outChannels, 3)
	def forward(self, x):
		return self.conv2(self.relu(self.conv1(x)))


class Encoder(Module):
	def __init__(self, channels=(3, 16, 32, 64)):
		super().__init__()
		self.conv1 = Conv2d(3,3,7)
		self.conv2 = Conv2d(3, 3, 5)
		self.relu = ReLU()
		self.encBlocks = ModuleList(
			[Block(channels[i], channels[i + 1])
			 	for i in range(len(channels) - 1)])
		self.pool = MaxPool2d(2)

	def forward(self, x):
		x = self.relu(self.conv1(x))
		x = self.pool(self.relu(self.conv2(x)))

		blockOutputs = []
		for block in self.encBlocks:
			x = block(x)
			blockOutputs.append(x)
			x = self.pool(x)
		return blockOutputs


class Decoder(Module):
    def __init__(self, channels=(64, 32, 16)):
        super().__init__()
        self.channels = channels
        self.upconvs = ModuleList(
			[ConvTranspose2d(channels[i], channels[i + 1], 2, 2)
			 	for i in range(len(channels) - 1)])
        self.dec_blocks = ModuleList(
			[Block(channels[i], channels[i + 1])
			 	for i in range(len(channels) - 1)])
    def forward(self, x, encFeatures):
        for i in range(len(self.channels) - 1):
            x = self.upconvs[i](x)
            encFeat = self.crop(encFeatures[i], x)
            x = torch.cat([x, encFeat], dim=1)
            x = self.dec_blocks[i](x)

        return x
    def crop(self, encFeatures, x):
        (_, _, H, W) = x.shape
        encFeatures = CenterCrop([H, W])(encFeatures)
        return encFeatures


class UNet(Module):
	def __init__(self, encChannels=(3, 16, 32, 64),
		decChannels=(64, 32, 16),
		nbClasses=1, retainDim=True,
		outSize=(1170,  1654)):
		super().__init__()
		self.encoder = Encoder(encChannels)
		self.decoder = Decoder(decChannels)
		self.head = Conv2d(decChannels[-1], nbClasses, 1)
		self.retainDim = retainDim
		self.outSize = outSize
  
  



	def forward(self, x):
		encFeatures = self.encoder(x)
		decFeatures = self.decoder(encFeatures[::-1][0],
								   encFeatures[::-1][1:])
		map = self.head(decFeatures)
		if self.retainDim:
			map = F.interpolate(map, self.outSize)
		return map

	def computePrecisionAndRecall(self,pred,y):
		predMask = torch.sigmoid(pred)
		pred05=predMask>=0.5
		pred3 = 3*pred05
		diff = pred3-y
		TP = torch.sum(diff==2)
		FN = torch.sum(diff==-1)
		FP = torch.sum(diff==3)
		precision = TP/((TP+FP)+0.0000001)
		recall = TP/((TP+FN)+0.000001)
		F1Score = (2*(precision*recall))/(precision+recall+0.000001)
		return TP,FN,FP

	def predict(self,image):
		self.eval()
		self.to('cuda')
		with torch.no_grad():
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			image = image.astype("float32") / 255.0
			image = cv2.resize(image, dsize=(1654, 1170))
			image = np.transpose(image, (2, 0, 1))
			image = np.expand_dims(image, 0)
			image = torch.from_numpy(image).to('cuda')
			predMask = self.forward(image).squeeze()
			predMask = torch.sigmoid(predMask)
			predMask = predMask.cpu().numpy()
			predMask = (predMask > 0.3) * 255
			predMask = predMask.astype(np.uint8)
			return predMask