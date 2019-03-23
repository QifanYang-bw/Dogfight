# coding: utf-8

from const import *
from envi import *

import math
import random
# import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

file_path = 'checkpoint.pth.tar'

def bar():
    print('-' * 30)

class Net(nn.Module):

    def __init__(self, input_size, output_size):
        super().__init__()

        hidden_size = [72, 324, 72]

        self.linear1 = nn.Linear(input_size, hidden_size[0])
        self.linear2 = nn.Linear(hidden_size[0], hidden_size[1])
        self.linear3 = nn.Linear(hidden_size[1], hidden_size[2])
        self.linear4 = nn.Linear(hidden_size[2], output_size)

    def forward(self, x):
        x = torch.sigmoid(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = F.relu(self.linear3(x))
        x = self.linear4(x)
        return x


class Agent_RL(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.eval_net = Net(self.state_space_dim, self.action_space_dim)

        if self.training:

            self.optimizer = optim.Adam(self.eval_net.parameters(), lr = self.lr)
            self.buffer = []#ExperienceReplay(buffer_size = self.buffer_size, unusual_sample_factor = self.unusual_sample_factor)
            self.steps = 0

            self.epsi = self.epsi_high

        else:

            self.epsi = 0
        
    def act(self, s0, epsi = None):
        if self.training:
            self.epsi = self.epsi_low + (self.epsi_high - self.epsi_low) * (math.exp(-1.0 * self.steps/self.decay))

        if epsi == None:
            epsi = self.epsi 

        if random.random() < epsi:
            a0 = np.random.choice(self.action_space_dim, p = net_random_prior)
            # print('r', a0)
        else:
            s0 = torch.tensor(s0, dtype = torch.float).view(1, -1)
            a0 = torch.argmax(self.eval_net(s0)).item()
            # print('a', a0)

        return a0

    def put(self, *transition):
        self.steps += 1

        # self.buffer.add(transition)

        if len(self.buffer)==self.buffer_size:
            self.buffer.pop(0)
        self.buffer.append(transition)

    def __lr_modify(self):
        if self.steps < 32000:
            self.lr = 0.001
        else:
            self.lr = 0.0001

    def learn(self):
        if len(self.buffer) < self.batch_size:
            return

        '''
            s0: state before;
            a0: action;
            r1: reward(after);
            s1: state after.
        '''

        # samples = self.buffer.sample(self.batch_size)

        samples = random.sample(self.buffer, self.batch_size)

        s0, a0, r1, s1 = zip(*samples)
        s0 = torch.tensor(s0, dtype=torch.float)
        a0 = torch.tensor(a0, dtype=torch.long).view(self.batch_size, -1)
        r1 = torch.tensor(r1, dtype=torch.float).view(self.batch_size, -1)
        s1 = torch.tensor(s1, dtype=torch.float)

        y_true = r1 + self.gamma * torch.max( self.eval_net(s1).detach(), dim=1)[0].view(self.batch_size, -1)
        y_pred = self.eval_net(s0).gather(1, a0)

        loss_fn = nn.MSELoss()
        loss = loss_fn(y_pred, y_true)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.__lr_modify()

    def save(self):
        if not self.training:
            print('Can\'t save because of testing mode')
            return 

        bar()
        print('Saving checkpoint to', 'checkpoint.pth.tar')

        try:

            torch.save({
                'epoch': self.steps,
                'model_state_dict': self.eval_net.state_dict(),
                'optimizer_state_dict': self.optimizer.state_dict(),
                'lr': self.lr,
            }, file_path)

        except Exception as the_exception:

            print("Checkpoint saving error:", the_exception)

        else:

            print('Checkpoint Saved')

        bar()
        print()

    def load(self):
        bar()
        print('Load checkpoint from', 'checkpoint.pth.tar')

        try:

            checkpoint = torch.load(file_path)

            self.eval_net.load_state_dict(checkpoint['model_state_dict'])

            if self.training:
                self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
                self.steps = checkpoint['epoch']
                self.lr = checkpoint['lr']

            self.eval_net.eval()

        except Exception as the_exception:

            print("Checkpoint loading error:", the_exception)
            print("The AI will run based on an untrained model")

        else:

            print("Checkpoint loaded successfully")
            print("Steps:", checkpoint['epoch'])

        bar()
        print()
    
    '''
    def plot(self, score, mean):
        from IPython import display
        display.clear_output(wait=True)
        display.display(plt.gcf())
        plt.figure(figsize=(20,10))
        plt.clf()
    
        plt.title('Training...')
        plt.xlabel('Episode')
        plt.ylabel('Duration')
        plt.plot(score)
        plt.plot(mean)
        plt.text(len(score)-1, score[-1], str(score[-1]))
        plt.text(len(mean)-1, mean[-1], str(mean[-1]))
    '''
