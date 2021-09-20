import numpy as np
import pickle

def generate_room(select_map):
    room_fixed = []
    room_state = []

    targets = []
    boxes = []
    for row in select_map:
        room_f = []
        room_s = []

        for e in row:
            if e == '#':
                room_f.append(0)
                room_s.append(0)

            elif e == '@':
                room_f.append(1)
                room_s.append(5)

            elif e == '$':
                boxes.append((len(room_fixed), len(room_f)))
                room_f.append(1)
                room_s.append(3)

            elif e == '.':
                targets.append((len(room_fixed), len(room_f)))
                room_f.append(2)
                room_s.append(2)

            else:
                room_f.append(1)
                room_s.append(1)

        room_fixed.append(room_f)
        room_state.append(room_s)

    return np.array(room_fixed), np.array(room_state)

def build_levels():
    levels = []

    with open(f"storage/test_levels.txt") as f:
        content = f.read()
        content = content[1:]
        for level in content.split(";"):
            level = level.strip().split("\n", 1)
            id, room = level[0].strip(), level[1]
            topology, room = generate_room(room.split("\n"))
            levels.append([int(id), room, topology])

    return levels

def main():
    with open('storage/levels.pkl', 'wb') as file:
        levels = build_levels()
        pickle.dump(levels, file)

    with open('storage/steps.txt', 'w') as file:
        file.write("0")

if __name__ == "__main__":
    main()
