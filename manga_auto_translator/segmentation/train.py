from trainingDatasets import SegmentationDataset
from UNet import UNet
import config
from torch.nn import BCEWithLogitsLoss
from torch.optim import Adam
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from torchvision import transforms
from imutils import paths
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import torch
import time



if __name__ == '__main__':
	print('is cuda available  : ')
	print(torch.cuda.is_available())

	imagePaths = sorted(list(paths.list_images(config.IMAGE_DATASET_PATH)))
	maskPaths = sorted(list(paths.list_images(config.MASK_DATASET_PATH)))

	split = train_test_split(imagePaths, maskPaths,
							 test_size=config.TEST_SPLIT,train_size=1-config.TEST_SPLIT, random_state=42)

	(trainImages, testImages) = split[:2]
	(trainMasks, testMasks) = split[2:]

	print("[INFO] saving testing image paths...")
	f = open(config.TEST_PATHS, "w")
	f.write("\n".join(testImages))
	f.close()





	transforms = transforms.Compose([transforms.ToPILImage(),
transforms.Resize((config.INPUT_IMAGE_HEIGHT,
				   config.INPUT_IMAGE_WIDTH)),			transforms.ToTensor()])


	trainDS = SegmentationDataset(imagePaths=trainImages, maskPaths=trainMasks,
		transforms=transforms)
	testDS = SegmentationDataset(imagePaths=testImages, maskPaths=testMasks,
		transforms=transforms)
	print(f"[INFO] found {len(trainDS)} examples in the training set...")
	print(f"[INFO] found {len(testDS)} examples in the test set...")


	trainLoader = DataLoader(trainDS, shuffle=True,
							 batch_size=config.BATCH_SIZE, pin_memory=config.PIN_MEMORY,
							 num_workers=4)
	testLoader = DataLoader(testDS, shuffle=False,
							batch_size=config.BATCH_SIZE, pin_memory=config.PIN_MEMORY,
							num_workers=4)


	unet = UNet().to(config.DEVICE)
	pytorch_total_params = sum(p.numel() for p in unet.parameters() if p.requires_grad)
	print('nombre de params : ' + str(pytorch_total_params))

	lossFunc = BCEWithLogitsLoss()
	opt = Adam(unet.parameters(), lr=config.INIT_LR)
	scheduler = ReduceLROnPlateau(opt,'min',verbose=True)

	trainSteps = len(trainDS) // config.BATCH_SIZE
	testSteps = len(testDS) // config.BATCH_SIZE

	H = {"train_loss": [], "test_loss": []}
	Score = {"precision_train":[],"precision_test":[],"recall_train":[],"recall_test":[],"F1_train":[],"F1_test":[],'Time':0}


	print("[INFO] training the network...")
	startTime = time.time()
	for e in tqdm(range(config.NUM_EPOCHS)):
		unet.train()

		totalTrainLoss = 0
		totalTestLoss = 0
		precision_train=0
		precision_test=0
		recall_train=0
		recall_test=0
		F1_train=0
		F1_test=0
		TPTrain=0
		FNTrain=0
		FPTrain=0
		TPTest=0
		FNTest=0
		FPTest=0
		nbIter = 0
		for (i, (x, y)) in enumerate(trainLoader):
			(x, y) = (x.to(config.DEVICE), y.to(config.DEVICE))
			pred = unet(x)
			TP, FN, FP = unet.computePrecisionAndRecall(pred, y)
			TPTrain += TP
			FNTrain += FN
			FPTrain += FP
			loss = lossFunc(pred, y)
			print(np.round(nbIter/len(trainLoader),2))
			nbIter+=1
			opt.zero_grad()
			loss.backward()

			opt.step()

			totalTrainLoss += loss
		with torch.no_grad():
			unet.eval()
			for (x, y) in testLoader:
				(x, y) = (x.to(config.DEVICE), y.to(config.DEVICE))
				pred = unet(x)
				TP,FN,FP = unet.computePrecisionAndRecall(pred, y)
				TPTest+=TP
				FNTest+=FN
				FPTest+=FP
				loss = lossFunc(pred, y)
				totalTestLoss += lossFunc(pred, y)
		avgTrainLoss = totalTrainLoss / trainSteps

		precision_train = TPTrain/((TPTrain+FPTrain)+0.0000001)
		recall_train = TPTrain/((TPTrain+FNTrain)+0.000001)
		F1_train = (2*(precision_train*recall_train))/(precision_train+recall_train+0.000001)

		avgTestLoss = totalTestLoss / testSteps
		precision_test = TPTest/((TPTest+FPTest)+0.0000001)
		recall_test = TPTest/((TPTest+FNTest)+0.000001)
		F1_test = (2*(precision_test*recall_test))/(precision_test+recall_test+0.000001)
		H["train_loss"].append(avgTrainLoss.cpu().detach().numpy())
		H["test_loss"].append(avgTestLoss.cpu().detach().numpy())
		Score["precision_train"].append(precision_train.cpu().detach().numpy())
		Score["precision_test"].append(precision_test.cpu().detach().numpy())
		Score["recall_train"].append(recall_train.cpu().detach().numpy())
		Score["recall_test"].append(recall_test.cpu().detach().numpy())
		Score["F1_train"].append(F1_train.cpu().detach().numpy())
		Score["F1_test"].append(F1_test.cpu().detach().numpy())
		torch.save(unet.state_dict(), config.MODEL_PATH)
		print("[INFO] EPOCH: {}/{}".format(e + 1, config.NUM_EPOCHS))
		print("Train loss: {:.6f}, Test loss: {:.4f}".format(
			avgTrainLoss, avgTestLoss))
		print("Precision train: {:.6f}, Precision test: {:.4f}, Recall train: {:.6f}, Recall test: {:.4f},F1 train: {:.6f}, F1 test: {:.4f}".format(
			precision_train, precision_test,recall_train,recall_test,F1_train,F1_test))
	endTime = time.time()
	print("[INFO] total time taken to train the model: {:.2f}s".format(
		endTime - startTime))
	Score['Time'] = endTime - startTime

	plt.style.use("ggplot")
	fig1 = plt.figure()
	plt.plot(H["train_loss"], label="train_loss")
	plt.plot(H["test_loss"], label="test_loss")
	plt.title("Training Loss on Dataset")
	plt.xlabel("Epoch #")
	plt.ylabel("Loss")
	plt.legend(loc="lower left")
	fig1.savefig(config.PLOT_PATH)

	plt.style.use("ggplot")
	fig2 = plt.figure()
	plt.plot(Score["precision_train"], label="precision_train")
	plt.plot(Score["precision_test"], label="precision_test")
	plt.plot(Score["recall_train"], label="recall_train")
	plt.plot(Score["recall_test"], label="recall_test")
	plt.plot(Score["F1_train"], label="F1_train")
	plt.plot(Score["F1_test"], label="F1_test")
	plt.title("Performance measures")
	plt.xlabel("Epoch #")
	plt.ylabel("score")
	plt.legend(loc="lower left")
	fig2.savefig(config.PLOT_SCORE_PATH)
	torch.save(unet.state_dict(), config.MODEL_PATH)

	with open(config.SCORE_PATH, 'w') as f:
		for key in Score.keys():
			f.write("%s,%s\n" % (key, Score[key]))