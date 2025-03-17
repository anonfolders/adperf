from enum import auto, Enum
import numpy as np


class PerturbType(Enum):
    CENTER_Y = auto()
    CENTER_XY = auto()
    PLUS_X = auto()
    MINUS_X = auto()
    OBS_RIGHT = auto()
    OBS_LEFT = auto()
    NOISE_LEFT = auto()
    NOISE_RIGHT = auto()


PT_LOOKUP = {
    # 'plus_x': PerturbType.PLUS_X,
    'obs_left': PerturbType.OBS_LEFT,
    # 'minus_x': PerturbType.MINUS_X,
    'obs_right': PerturbType.OBS_RIGHT,
    'center_y': PerturbType.CENTER_Y,
    'noise_left': PerturbType.NOISE_LEFT,
    'noise_right': PerturbType.NOISE_RIGHT,
}


def separate_quadrants(obs_pts_w_lbls):
    coords_y = obs_pts_w_lbls[:, 1]
    center_y = np.mean(coords_y)    

    coords_x = obs_pts_w_lbls[:, 0]
    center_x = np.mean(coords_x)
    return 0   

def separate_left_right_pts(obs_pts_w_lbls):
    coords_y = obs_pts_w_lbls[:, 1]
    center = np.mean(coords_y)
    # get points to the left
    mask_left = coords_y > center
    pts_right = obs_pts_w_lbls[mask_left]
    # get points to the right
    mask_right = ~mask_left
    pts_left = obs_pts_w_lbls[mask_right]
    return pts_left, pts_right


def perturb_center_y(obs_pts_w_lbls, corr_val):
    # computer the center
    pts_left, pts_right = separate_left_right_pts(obs_pts_w_lbls)
    corr_arr_left = pts_left + [0, corr_val, 0, 0, 0, 0]
    corr_arr_right = pts_right - [0, corr_val, 0, 0, 0, 0]

    # checking results
    # for idx in range(len(pts_left)):
    #     print(pts_left[idx], '---->', corr_arr_left[idx])
    # for idx in range(len(pts_right)):
    #     print(pts_right[idx], '---->', corr_arr_right[idx])
    
    corr_arr = np.concatenate((corr_arr_left, corr_arr_right), axis=0)

    return corr_arr


def perturb_center_xy(obs_pts_w_lbls):
    return 0


def separate_by_obs(arr, col):
    indices = np.argsort(arr[:, col])
    arr_temp = arr[indices]
    np.array_split(arr_temp, np.where(np.diff(arr_temp[:, col]) != 0)[0] + 1)


def add_noise(arr, val, dir):
    if dir == PerturbType.NOISE_RIGHT:
        return shift_all_obstacles(arr, val, 2)
    elif dir == PerturbType.NOISE_LEFT:
        return shift_all_obstacles(arr, val, 3)


def add_obs(arr, val, dir):
    if dir == PerturbType.OBS_RIGHT:
        return shift_all_obstacles(arr, val, 2)
    elif dir == PerturbType.OBS_LEFT:
        return shift_all_obstacles(arr, val, 3)


# add <val> noises in direction <dir> to obstacles <arr>
def shift_all_obstacles(arr, val, dir):
    corr_arr = None
    # corruptions
    if dir == 0:
        corr_arr = arr + [val, 0, 0, 0, 0]
    elif dir == 1:
        corr_arr = arr - [val, 0, 0, 0, 0]
    elif dir == 2:
        corr_arr = arr + [0, val, 0, 0, 0]
    elif dir == 3:
        corr_arr = arr - [0, val, 0, 0, 0]
    else:
        print(f'Invalid perturbation {dir}')

    return corr_arr