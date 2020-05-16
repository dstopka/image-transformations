import numpy as np
import cv2
import math

class ImageTransform:
    @staticmethod
    def gauss_hist(img):
        pass

    @staticmethod
    def filt_entropy(img):
        pass

    @staticmethod
    def imopen(img):
        pass

    @staticmethod
    def convex_surr(img):
        mask0 = np.array([[1, 1, 0], [1, -1, 0], [1, 0, -1]], dtype=np.int)
        mask45 = np.array([[1, 1, 1], [1, -1, 0], [0, -1, 0]], dtype=np.int)
        compare = np.zeros_like(img)
        while not np.array_equal(img, compare):
            compare = img
            for i in range(4):
                img = img | ImageTransform.hit_miss(img, mask0)
                img = img | ImageTransform.hit_miss(img, mask45)
                mask0 = np.rot90(mask0)
                mask45 = np.rot90(mask45)
        return img

    @staticmethod
    def erode(img, mask):
        res = np.zeros_like(img)
        x, y = img.shape
        P, Q = mask.shape
        for i in range(math.ceil(P/2), x-math.floor(P/2)):
            for j in range(math.ceil(Q / 2), y - math.floor(Q / 2)):
                on = img[i - math.floor(P / 2):i + math.floor(P / 2)+1, j - math.floor(Q / 2): j + math.floor(Q / 2)+1]
                bool_idx = (mask == 1)
                res[i, j] = min(on[bool_idx])
        return res

    @staticmethod
    def hit_miss(img, mask):
        true_mask = mask * (mask == 1)
        false_mask = mask * (mask == -1) * -1
        res = ImageTransform.erode(img, true_mask) & ImageTransform.erode(~img, false_mask)
        return res


