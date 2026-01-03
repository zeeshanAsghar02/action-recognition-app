
import torch
import torch.nn as nn
from torchvision import models

class CNN_LSTM_Model(nn.Module):
    def __init__(self, num_classes):
        super(CNN_LSTM_Model, self).__init__()
        self.cnn = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        self.cnn.fc = nn.Identity()
        self.lstm = nn.LSTM(input_size=2048, hidden_size=512, num_layers=1, batch_first=True)
        self.fc = nn.Linear(512, num_classes)

    def forward(self, x):
        features = self.cnn(x)
        features = features.unsqueeze(1)
        lstm_out, _ = self.lstm(features)
        output = self.fc(lstm_out[:, -1, :])
        return output
