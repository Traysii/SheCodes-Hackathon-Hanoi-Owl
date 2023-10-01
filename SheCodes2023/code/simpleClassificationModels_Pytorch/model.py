import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as f
from torch.utils.data import DataLoader
import torchvision.datasets as datasets
import  torchvision.transforms as transforms

import torchvision
from torch.utils.tensorboard import SummaryWriter




class CNN(nn.Module):
    def __init__(self, in_channels = 1, num_classes = 10):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels = 1, out_channels=8, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(16*7*7, num_classes)

    def forward(self, x):
        x= f.relu(self.conv1(x))
        x= self.pool(x)
        x= f.relu(self.conv2(x))
        x= self.pool(x)
        x= x.reshape(x.shape[0], -1)
        x= self.fc1(x)

        return x

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


in_channels = 1
num_classes = 10
learning_rate = 0.001
batch_size = 64
epochs = 5

# Test MNIST
# train_dataset = datasets.MNIST(root='data/', train= True, transform= transforms.ToTensor(), download= True)
# train_loader = DataLoader(dataset=train_dataset, batch_size= batch_size, shuffle=True)
# test_dataset = datasets.MNIST(root='data/', train= False, transform= transforms.ToTensor(), download= True)
# test_loader = DataLoader(dataset=test_dataset, batch_size= batch_size, shuffle=True)

model = CNN().to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr= learning_rate)
writer = SummaryWriter(f'runs/MNIST/tryingout_tensorboard')
step = 0

for epoch in range(epochs):
    for batch_idx, (data, labels) in enumerate(train_loader):

        data = data.to(device)
        labels = labels.to(device)

        scores = model(data)
        loss = criterion(scores, labels)

        optimizer.zero_grad()
        loss.backward()

        optimizer.step()



def check_acc(loader, model):
    if loader.dataset.train:
        print("Checking on training loss")
    else:
        print("Checking on test loss")

    num_correct = 0
    num_samples = 0
    model.eval()

    with torch.no_grad():
        for x,y in loader:
            x = x.to(device)
            y = y.to(device)

            scores = model(x)
            _, predictions = scores.max(1)
            num_correct += (predictions == y).sum()
            num_samples += predictions.size(0)
            running_train_acc = float(num_correct)/float(data.shape[0])

            writer.add_scalar('Training Loss', loss, global_step= step)
            writer.add_scalar('Traning Accuracy', running_train_acc, global_step=step)
            step = step + 1

        print(f'Got {num_correct} / {num_samples} with accuracy {float(num_correct) / float(num_samples)*100: .2f}')

    model.train()

check_acc(train_loader, model)
check_acc(test_loader, model)
writer.flush()
