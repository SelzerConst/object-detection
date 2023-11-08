#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np


def get_steer_matrix_left_lane_markings(shape):
    """
        Args:
            shape: The shape of the steer matrix (tuple of ints)
        Return:
            steer_matrix_left_lane: The steering (angular rate) matrix for Braitenberg-like control
                                    using the masked left lane markings (numpy.ndarray)
    """
    h, w = shape
    w_half = w // 2
    steer_matrix_left_lane = np.zeros(shape=shape, dtype="float32")
    # Steer matrix
    steer_matrix_left_lane[int(h * 5 / 8):, :w_half] = -0.01  #  Nav
    # steer_matrix_left_lane[int(h * 4 / 8):, :w_half] = -0.01  # Obs

    return steer_matrix_left_lane


def get_steer_matrix_right_lane_markings(shape):
    """
        Args:
            shape: The shape of the steer matrix (tuple of ints)
        Return:
            steer_matrix_right_lane: The steering (angular rate) matrix for Braitenberg-like control
                                     using the masked right lane markings (numpy.ndarray)
    """
    h, w = shape
    w_half = w // 2
    steer_matrix_right_lane = np.zeros(shape=shape, dtype="float32")
    # Steer matrix
    steer_matrix_right_lane[int(h * 5 / 8):, w_half:] = 0.01  # Nav
    # steer_matrix_right_lane[int(h * 4 / 8):, w_half:] = 0.01  # Obs

    return steer_matrix_right_lane


# def detect_lane_markings(mask, label_mask, class2int, avoid):
#     """
#         Args:
#             mask: Segmentation result after masking (numpy.ndarray)
#         Return:
#             left_masked_img:   Masked image for the dashed-yellow line (numpy.ndarray)
#             right_masked_img:  Masked image for the solid-white line (numpy.ndarray)
#     """

#     h, w = mask.shape

#     # ####### Edge based masking #######
#     mask_left = np.ones(mask.shape)
#     mask_left[:, int(np.floor(w / 2)):w + 1] = 0
#     mask_right = np.ones(mask.shape)
#     mask_right[:, 0:int(np.floor(w / 2))] = 0

#     # ####### Edge based masking #######
#     if avoid:
#         # ####### Edge based masking #######
#         object_mask_left = np.ones(mask.shape)
#         right_mask_left = np.ones(mask.shape)
#     else:
#         # ####### Edge based masking #######
#         object_mask_left = label_mask == class2int['yellow-lane']
#         right_mask_left = label_mask == class2int['white-lane']

#     # ####### Final edge masking #######
#     mask_left_edge = mask * mask_left * object_mask_left
#     mask_right_edge = mask * mask_right * right_mask_left

#     return mask_left_edge, mask_right_edge


def detect_lane_markings(mask, label_mask, class2int, avoid):
    """
    Args:
        mask: Segmentation result after masking (numpy.ndarray)
    Return:
        left_masked_img:   Masked image for the dashed-yellow line (numpy.ndarray)
        right_masked_img:  Masked image for the solid-white line (numpy.ndarray)
    """

    h, w = mask.shape

    # Calculate the row index for two-thirds of the height
    upper_half_h = int(np.floor( h / 2))

    # Edge based masking
    mask_left = np.ones(mask.shape)
    mask_left[:, int(np.floor(w / 2)):w + 1] = 0
    mask_right = np.ones(mask.shape)
    mask_right[:, 0:int(np.floor(w / 2))] = 0

    # Edge based masking
    if avoid:
        object_mask_left = np.ones(mask.shape)
        right_mask_left = np.ones(mask.shape)
    else:
        object_mask_left = label_mask == class2int['yellow-lane']
        right_mask_left = label_mask == class2int['white-lane']

    # Final edge masking
    mask_left_edge = mask * mask_left * object_mask_left
    mask_right_edge = mask * mask_right * right_mask_left

    # Set the upper two thirds of the return matrices to zero
    mask_left_edge[:upper_half_h, :] = 0
    mask_right_edge[:upper_half_h, :] = 0




    return mask_left_edge, mask_right_edge




def rescale(a: float, L: float, U: float):
    if np.allclose(L, U):
        return 0.0
    return (a - L) / (U - L)


def vanilla_servoing_mask(mask, class2int):
    weighted_mask = np.zeros(mask.shape)
    weighted_mask[:] = (mask == class2int['white-lane']) * 1.5 + (mask == class2int['yellow-lane']) * 3.5
    return weighted_mask



def obstables_servoing_mask(mask, class2int):
    # TODO add weights?
    weighted_mask = np.zeros(mask.shape)
    weighted_mask[:] = (mask == class2int['white-lane']) * 1.5 + (mask == class2int['duckiebot']) * 1.5 + \
                       (mask == class2int['duck']) * 2.0 + (mask == class2int['sign'])
    return weighted_mask


# def obstables_servoing_mask(mask, class2int):
#     # TODO add weights?
#     weighted_mask = np.zeros(mask.shape)
#     weighted_mask[:] = (mask == class2int['white-lane']) * 1.5 + \
#                        (mask == class2int['duck']) * 3 + (mask == class2int['yellow-lane']) * 2
#     return weighted_mask