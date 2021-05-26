# ## 101 On how easy you can steal someones net. But u shouldn't

# ## Imports and Magic

import art
import torch
import torchvision
import torchvision.transforms as transforms
from torchvision.models import alexnet as alexnet
import pandas
from art.estimators.classification import PyTorchClassifier as art_torch


# +
# %load_ext autoreload
# %autoreload 2

from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"
# -

torch.cuda.is_available() 
torch.cuda.current_device()
torch.cuda.get_device_name(0)

# +
#alex = alexnet(num_classes = 10).cuda()
#next(alex.parameters()).is_cuda
#alex
# -

# ## A simple CNN straight from the Pytorch Website - Aka. the net to be stolen

# +
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        if type(x) == np.ndarray:
            x = torch.from_numpy(x)
            x = x.cuda()
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


net = Net()
net = net.cuda()
# -

next(net.parameters()).is_cuda

# +
transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

batch_size = 4

trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True, num_workers=0)

testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=False, num_workers=0)
stealloader = torch.utils.data.DataLoader(testset, batch_size=10_000,
                                         shuffle=False, num_workers=0)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# +
import matplotlib.pyplot as plt
import numpy as np

# functions to show an image


def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()


# get some random training images
dataiter = iter(trainloader)
images, labels = dataiter.next()
images.shape
# show images
imshow(torchvision.utils.make_grid(images))
# print labels
print(' '.join('%5s' % classes[labels[j]] for j in range(batch_size)))

# +
import torch.optim as optim
import torch.nn as nn

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

# +
for epoch in range(2):  # loop over the dataset multiple times

    running_loss = 0.0
    #print("1")
    for i, data in enumerate(trainloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data
        inputs = inputs.cuda()
        labels = labels.cuda()
        # zero the parameter gradients
        optimizer.zero_grad()
        #print("2")
        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        #print("3")
        # print statistics
        running_loss += loss.item()
        if i % 2000 == 1999:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0

print('Finished Training')
# -

dataiter = iter(testloader)

images, labels = dataiter.next()

# +
#images.cuda()
# -

# print images
imshow(torchvision.utils.make_grid(images))
print('GroundTruth: ', ' '.join('%5s' % classes[labels[j]] for j in range(4)))

outputs = net(images.cuda())
np.argmax(outputs.detach().cpu().numpy(),axis=1)

# ## Extraction Attack

images.shape


def one_hot_output(image):
    return np.argmax(net(image).detach().cpu().numpy(),axis=1)


# A Blackbox to build a new net
art_net = art.estimators.classification.BlackBoxClassifier(one_hot_output, input_shape=[1, 3, 32, 32], nb_classes=10)

ex = art.attacks.extraction

cat = ex.CopycatCNN(art_net, batch_size_fit=50, batch_size_query=50, nb_epochs=10)

# Loading the net-to-be-stolen aka our prey into the framework
prey = art.estimators.classification.PyTorchClassifier(model=net, loss=criterion, input_shape=images.shape, optimizer=optimizer, nb_classes=10)

trained_cat = cat.extract(iter(stealloader).next()[0], thieved_classifier=prey)

trained_cat

net




