from boxoban_environment import BoxobanEnvironment

def worker(master):
    level = None
    while True:
        cmd, data = master.recv()
        if cmd == 'step':
            observation, reward, done, info = env.step(data)
            if done:
                (id, room, topology) = level
                env = BoxobanEnvironment(room.copy(), topology.copy())
                observation = env.observation
            master.send((observation, reward, done, info))
        elif cmd == 'reset':
            level = data
            (id, room, topology) = level
            env = BoxobanEnvironment(room.copy(), topology.copy())
            master.send(env.observation)
        elif cmd == 'close':
            master.close()
            break
        else:
            raise NotImplementedError
