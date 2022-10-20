import cv2
import numpy as np

from os import path

from .blending import (gaussPyramid, laplPyramid, blend, collapse)

MIN_DEPTH = 4
    

def normalize(img):
    return cv2.normalize(img, img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)


def viz_pyramid(stack, shape, name, norm=False):
    layers = [normalize(np.dstack(imgs)) if norm else np.clip(np.dstack(imgs), 0, 255) for imgs in zip(*stack)]
    stack = [cv2.resize(layer, shape, interpolation=3) for layer in layers]
    img = np.vstack(stack).astype(np.uint8)
    #cv2.imwrite(name + ".png", img)
    return img


def mix(black_image, white_image, mask, out_path, min_depth=MIN_DEPTH):
    black_image = np.atleast_3d(black_image).astype('float64')
    white_image = np.atleast_3d(white_image).astype('float64')
    mask_img = np.atleast_3d(mask).astype('float64') / 255.

    shape = mask_img.shape[1::-1]
    min_size = min(black_image.shape[:2])
    depth = int(np.log2(min_size)) - min_depth

    gauss_pyr_mask = [gaussPyramid(ch, depth) for ch in np.rollaxis(mask_img, -1)]
    gauss_pyr_black = [gaussPyramid(ch, depth) for ch in np.rollaxis(black_image, -1)]
    gauss_pyr_white = [gaussPyramid(ch, depth) for ch in np.rollaxis(white_image, -1)]
    '''
    viz_pyramid(gauss_pyr_mask, shape, path.join(out_path, 'gauss_pyr_mask'), norm=True)
    viz_pyramid(gauss_pyr_black, shape, path.join(out_path, 'gauss_pyr_black'))
    viz_pyramid(gauss_pyr_white, shape, path.join(out_path, 'gauss_pyr_white'))
    '''

    lapl_pyr_black = [laplPyramid(ch) for ch in gauss_pyr_black]
    lapl_pyr_white = [laplPyramid(ch) for ch in gauss_pyr_white]
    '''
    viz_pyramid(lapl_pyr_black, shape, path.join(out_path, 'lapl_pyr_black'), norm=True)
    viz_pyramid(lapl_pyr_white, shape, path.join(out_path, 'lapl_pyr_white'), norm=True)
    '''
    
    outpyr = [blend(*x) for x in zip(lapl_pyr_white, lapl_pyr_black, gauss_pyr_mask)]
    result = [[collapse(x)] for x in outpyr]
    #viz_pyramid(outpyr, shape, path.join(out_path, 'outpyr'), norm=True)
    img = viz_pyramid(result, shape, path.join(out_path, 'result'))
    
    return img
    

