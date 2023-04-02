# TODO: define the convolutional neural network architecture

import torch
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as I


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()

        # TODO: Define all the layers of this CNN, the only requirements are:
        # 1. This network takes in a square (same width and height), grayscale image as input
        # 2. It ends with a linear layer that represents the keypoints
        # it's suggested that you make this last layer output 136 values, 2 for each of the 68 keypoint (x, y) pairs

        # As an example, you've been given a convolutional layer, which you may (but don't have to) change:
        # 1 input image channel (grayscale), 32 output channels/feature maps, 5x5 square convolution kernel
        self.conv1 = nn.Conv2d(1, 32, 8)    # (224-8)/1 + 1 = 216
        self.conv2 = nn.Conv2d(32, 64, 5)   # (108-5)/1 + 1 = 104
        self.conv3 = nn.Conv2d(64, 128, 3)  # (52-3)/1 + 1 = 50
        self.conv4 = nn.Conv2d(128, 256, 2)  # (25-2)/1 + 1 = 23
        self.conv5 = nn.Conv2d(256, 512, 1)  # (12-1)/1 + 1 = 12

        self.pool = nn.MaxPool2d(2, 2)

        self.fc1 = nn.Linear(512*6*6, 1024)
        self.fc1_drop = nn.Dropout(p=0.5)
        self.fc2 = nn.Linear(1024, 512)
        self.fc2_drop = nn.Dropout(p=0.5)
        self.fc3 = nn.Linear(512, 136)

        # Note that among the layers to add, consider including:
        # maxpooling layers, multiple conv layers, fully-connected layers, and other layers (such as dropout or batch normalization) to avoid overfitting

    def forward(self, x):
        # TODO: Define the feedforward behavior of this model
        # x is the input image and, as an example, here you may choose to include a pool/conv step:
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = self.pool(F.relu(self.conv4(x)))
        x = self.pool(F.relu(self.conv5(x)))

        x = x.view(x.size(0), -1)

        x = F.relu(self.fc1(x))
        x = self.fc1_drop(x)
        x = F.relu(self.fc2(x))
        x = self.fc2_drop(x)
        x = self.fc3(x)

        # a modified x, having gone through all the layers of your model, should be returned
        return x
