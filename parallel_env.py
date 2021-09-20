import numpy as np
import torch
from torch.distributions import Categorical
import torch.multiprocessing as mp
from worker import worker

class ParallelEnv:
    def __init__(self, n_workers):
        self.n_workers = n_workers
        self.workers = []

        self.master_ends, worker_ends = zip(*[mp.Pipe() for _ in range(n_workers)])

        for worker_end in worker_ends:
            p = mp.Process(target=worker, args=(worker_end,))
            p.daemon = True
            p.start()
            self.workers.append(p)

    def reset(self, level):
        for master_end in self.master_ends:
            master_end.send(('reset', level))
        return np.stack([master_end.recv() for master_end in self.master_ends])

    def step(self, actions):
        for master_end, action in zip(self.master_ends, actions):
            master_end.send(('step', action))
            
        results = [master_end.recv() for master_end in self.master_ends]
        observations, rewards, dones, infos = zip(*results)

        return np.stack(observations), np.stack(rewards), np.stack(dones), infos

    def close(self):
        for master_end in self.master_ends:
            master_end.send(('close', None))
        for worker in self.workers:
            worker.join()

    def solve(self, level, model):
        observation = torch.tensor(self.reset(level))
        actions = torch.zeros((self.n_workers, 300), dtype=torch.uint8)

        for t in range(300):
            with torch.no_grad():
                pi, _ = model(observation)

                p = Categorical(pi)
                action = p.sample()
                actions[:, t] = action

            observation, reward, done, info = self.step(action.tolist())
            observation = torch.tensor(observation)
            dones = [env["finished"] for env in info]

            if any(dones) == True:
                index = [i for i,done in enumerate(dones) if done == True][0]

                return True, actions[index, 0:t+1]

        return False, actions[0]
