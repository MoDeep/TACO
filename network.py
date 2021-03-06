import torch 
import torchvision 
import torch.nn as nn
import numpy as np 

from torch.utils.data import DataLoader
from collections import OrderedDict

from dataset import TextDataset


class Prenet(nn.Module):
    def __init__(self, vocab_size, hidden_size):
        super(Prenet, self).__init__()
        
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.net = nn.Sequential(OrderedDict([
            ('fc1', nn.Linear(256, 256)),
            ('relu1', nn.ReLU()),
            ('dropout1', nn.Dropout(0.5)),
            ('fc2', nn.Linear(256, 128)),
            ('relu2', nn.ReLU()),
            ('dropout2', nn.Dropout(0.5))
        ]))

    def forward(input):
        output = nn.utils.rnn.pad_sequence(input)
        output = self.embedding(output)
        output = self.net(output)

        return output


class CBHG(nn.Module):
    def __init__(self, K, hidden_size):
        self.K = K
        self.hidden_size = hidden_size
        pass 

    def build(self):
        conv_bank = list()
        batch_norm_list = list()

        conv_bank.append(nn.Conv1d(1, self.hidden_size, 1))
        batch_norm_list.append(nn.BatchNorm1d(self.hidden_size))
        for k in range(2, self.K + 1):
            conv_bank.append(nn.Conv1d(self.hidden_size, self.hidden_size, k))
            batch_norm_list.append(nn.BatchNorm1d(self.hidden_size))

    def forward(self, x):
        pass 


if __name__ == '__main__':
    transcript_path = 'kss/transcript.txt'
    
    txt_dataset = TextDataset(transcript_path)
    data_loader = DataLoader(dataset=txt_dataset, 
                             batch_size=32, 
                             shuffle=True,
                             num_workers=2)
    
    print('Dataset making and Loading Success')
    
    prenet = Prenet()