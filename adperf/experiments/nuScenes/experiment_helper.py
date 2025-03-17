import numpy as np
from sklearn.metrics import mean_squared_error


def read_dropped_frames():
    dropped_frames = []
    with open('frames_dropped.txt', 'r') as fd:
        dropped_frames = fd.read().strip().split(',')

    dropped_frames = [int(x) - 1 for x in dropped_frames]
    return dropped_frames


def get_gt_modification():
    modification = 0
    with open('trajectory_modification.txt', 'r') as fd:
        mod = fd.read().strip().split(',')
        if 'left' in mod[0]:
            modification = -1 * float(mod[1])
        else:
            modification = float(mod[1])
    return modification


def compute_error(data):
    ade = []
    fde = []

    for sc, _ in data.items():
        # print('scene name:', sc)
        for obs, _ in data[sc].items():
            if 'ego' not in obs:
                orig = data[sc][obs]['original'][0][0]
                pert = data[sc][obs]['perturbed'][0][0]

                ade.append(mean_squared_error(orig, pert))
                fde.append(mean_squared_error(orig[-1], pert[-1]))

    ade = [x for x in ade if x >= 0.01]
    fde = [x for x in fde if x >= 0.01]
    print(f'ade: {round(np.mean(ade), 2)}, fde: {round(np.mean(fde),2)}')
