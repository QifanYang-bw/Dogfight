# coding: utf-8

from envi import *
from interface_dup import *

import math
import random
# import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

Input_Dim = 18
Output_Dim = 5

file_path = 'checkpoint.pth.tar'

class Net(nn.Module):

    def __init__(self, input_size, hidden1_size, hidden2_size, output_size):
        super().__init__()

        self.linear1 = nn.Linear(input_size, hidden1_size)
        self.linear2 = nn.Linear(hidden1_size, hidden2_size)
        self.linear3 = nn.Linear(hidden2_size, output_size)

    def forward(self, x):
        x = torch.sigmoid(self.linear1(x))
        x = torch.sigmoid(self.linear2(x))
        x = torch.sigmoid(self.linear3(x))
        return x

class Agent(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.eval_net = Net(self.state_space_dim, 64, 256, self.action_space_dim)
        self.optimizer = optim.Adam(self.eval_net.parameters(), lr = self.lr)
        self.buffer = []
        self.steps = 0

        self.epsi = self.epsi_high
        
    def act(self, s0):
        self.epsi = self.epsi_low + (self.epsi_high - self.epsi_low) * (math.exp(-1.0 * self.steps/self.decay))

        if random.random() < self.epsi:
            a0 = [random.random() for _ in range(self.action_space_dim)]
        else:
            s0 = torch.tensor(s0, dtype=torch.float).view(1,-1)
            a0 = self.eval_net(s0).flatten().tolist()

        return a0

    def put(self, *transition):
        self.steps += 1

        if len(self.buffer)==self.capacity:
            self.buffer.pop(0)
        self.buffer.append(transition)
        
    def learn(self):
        if (len(self.buffer)) < self.batch_size:
            return

        '''
            s0: state before;
            a0: action;
            r1: reward(after);
            s1: state after.
        '''
        
        samples = random.sample(self.buffer, self.batch_size)
        s0, a0, r1, s1 = zip(*samples)
        s0 = torch.tensor(s0, dtype=torch.float)
        a0 = torch.tensor(a0, dtype=torch.long).view(self.batch_size, -1)
        r1 = torch.tensor(r1, dtype=torch.float).view(self.batch_size, -1)
        s1 = torch.tensor(s1, dtype=torch.float)
        
        y_true = r1 + self.gamma * torch.max( self.eval_net(s1).detach(), dim=1)[0].view(self.batch_size, -1)
        y_pred = self.eval_net(s0).gather(1, a0)

        print(self.eval_net(s1).detach(), torch.max( self.eval_net(s1).detach(), dim=1))
        print('---')
        print(y_true)
        print('----')
        print(y_pred)
        print('####')
        
        loss_fn = nn.MSELoss()
        loss = loss_fn(y_pred, y_true)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
    
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

params = {
    'gamma': 0.8,
    'epsi_high': 0.65,
    'epsi_low': 0.05,
    'decay': int(1e5), # Need edit
    'lr': 0.001,
    'capacity': 10000,
    'batch_size': 4,
    'state_space_dim': Input_Dim,
    'action_space_dim': Output_Dim  
}

def main():

    env = Game()

    agent = Agent(**params)

    score = []
    mean = []


    for episode in range(1000):
        env.reset()

        total_reward_p1 = 0 
        total_reward_p2 = 0

        s0_1 = env.state(serial = 1)
        s0_2 = env.state(serial = 2)

        r1_1 = env.reward(1)
        r1_2 = env.reward(2)

        # while True:
        print('Episode', episode)
        print('Epsi', agent.epsi)
        print('Buffer', len(agent.buffer))

        _ = 0
        while True:
            _ += 1

            env.clear()

            if env.close:
                break

            env.draw()

            a0_1 = agent.act(s0_1)
            a0_2 = agent.act(s0_2)

            env.make_move(1, a0_1)
            env.make_move(2, a0_2)

            env.update()

            s1_1, s1_2 = env.state(1), env.state(2)

            r1_1 = env.reward(1)
            r1_2 = env.reward(2)

            if _ % 50 == 0:

                print('Trial', _, end = ' [')

                for data in a0_1:
                    print('{:.3f}  '.format(data), end = '')

                print('] {:.3f} {:.1f}  ['.format(r1_1, env.players[0].hp), end = '')

                for data in a0_2:
                    print('{:.3f}  '.format(data), end = '')

                print('] {:.3f} {:.1f}'.format(r1_2, env.players[1].hp))

            if r1_1 != 0:
                agent.put(s0_1, a0_1, r1_1, s1_1)
            if r1_2 != 0:
                agent.put(s0_2, a0_2, r1_2, s1_2)
            
            done = env.done()
            if done:
                break

            total_reward_p1 += r1_1
            total_reward_p2 += r1_2

            s0_1, s0_2 = s1_1, s1_2

            agent.learn()

        if env.close:
            break

        if episode % 10 == 0:
            print('Saving checkpoint to', 'checkpoint.pth.tar')
            torch.save(agent.eval_net.state_dict(), 'checkpoint.pth.tar')

        # model = TheModelClass(*args, **kwargs)
        # model.load_state_dict(torch.load(PATH))
        # model.eval()


        # score.append(total_reward_1)
        # mean.append( sum(score[-100:])/100)

        # agent.plot(score, mean)



    pg.quit()
    sys.exit()

'''
Check if main.py is the called program.
'''
if __name__ == '__main__':
    main()
