import torch
import torch.nn as nn
import torch.nn.functional as F

# Residual Block
class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()   

        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)

        if in_channels != out_channels or stride != 1:
            self.downsample = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False)
        else:
            self.downsample = None

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.relu(out)

        out = self.conv2(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out

# Model
class GAIL(nn.Module):
    def __init__(self):
        super(GAIL, self).__init__()

        self.encoder = nn.Sequential(
            ResidualBlock(7, 16),
            ResidualBlock(16, 16),
            ResidualBlock(16, 16),
            ResidualBlock(16, 32),
            ResidualBlock(32, 32),
            ResidualBlock(32, 32),
            ResidualBlock(32, 64),
            ResidualBlock(64, 64),
            ResidualBlock(64, 64),
        )  

        self.linear = nn.Sequential(
            nn.Linear(6400, 256),  # 64, 10, 10
            nn.ReLU()
        )

        self.actor_head = nn.Linear(256, 8)
        self.critic_head = nn.Linear(256, 1)

        self.discriminator_encoder = nn.Sequential(
            ResidualBlock(7, 16),
            ResidualBlock(16, 16),
            ResidualBlock(16, 16),
            ResidualBlock(16, 32),
            ResidualBlock(32, 32),
            ResidualBlock(32, 32),
            ResidualBlock(32, 64),
            ResidualBlock(64, 64),
            ResidualBlock(64, 64),
            nn.Flatten(),
            nn.Linear(6400, 256),  # 64, 10, 10
            nn.ReLU()
        )

        self.discriminator = nn.Sequential(
            nn.Linear(264, 128),  # 256 + 8
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
        )

    def forward(self, x):
        x = self.encoder(x)
        x = x.view(x.size(0), -1)

        x = self.linear(x)

        actor = F.softmax(self.actor_head(x), dim=-1)
        critic = self.critic_head(x)

        return actor, critic
    
    """
    Expert -> 0
    Policy -> 1
    """
    def discriminate(self, states, actions):
        states = self.discriminator_encoder(states)
        actions = F.one_hot(actions, num_classes=8).float()

        x = torch.cat((states, actions), dim=1)

        x = self.discriminator(x)

        return x

    # Compute discriminator reward
    def discriminator_reward(self, states, actions):
        with torch.no_grad():
            logits = self.discriminate(states, actions)

            return -F.logsigmoid(logits)