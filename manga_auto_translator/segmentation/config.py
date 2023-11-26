# import the necessary packages
import torch
import os

# base path of the dataset
DATASET_PATH = 'data/Manga109/'
# define the path to the images and masks dataset
IMAGE_DATASET_PATH = DATASET_PATH+'images_only/'
MASK_DATASET_PATH = os.path.join(DATASET_PATH, "Mask_only/")
# define the test split
TEST_SPLIT = 0.1
# determine the device to be used for training and evaluation
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# determine if we will be pinning memory during data loading
PIN_MEMORY = True if DEVICE == "cuda" else False

# define the number of channels in the input, number of classes,
# and number of levels in the U-Net model
NUM_CHANNELS = 1
NUM_CLASSES = 1
NUM_LEVELS = 4
# initialize learning rate, number of epochs to train for, and the
# batch size
INIT_LR = 0.001
NUM_EPOCHS = 40
BATCH_SIZE = 2
# define the input image dimensions
# INPUT_IMAGE_WIDTH = 566
# INPUT_IMAGE_HEIGHT = 400
#INPUT MODEL 7
INPUT_IMAGE_WIDTH = 1654
INPUT_IMAGE_HEIGHT = 1170
# define threshold to filter weak predictions
THRESHOLD = 0.3
# define the path to the base output directory
BASE_OUTPUT = "../Outputs"
# define the path to the output serialized model, model training
# plot, and testing image paths
MODEL_PATH = os.path.join(BASE_OUTPUT, "unet_tgs_salt.pth")
PLOT_PATH = os.path.sep.join([BASE_OUTPUT, "plotUnet_loss.png"])
PLOT_SCORE_PATH = os.path.sep.join([BASE_OUTPUT, "plotUnet_score.png"])
TEST_PATHS = os.path.sep.join([BASE_OUTPUT, "test_paths.txt"])
SCORE_PATH = os.path.sep.join([BASE_OUTPUT, "Unet_score.csv"])