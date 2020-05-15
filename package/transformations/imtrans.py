import numpy as np
import cv2

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
        mask = [[1, 1, 0], [1, -1, 0], [1, 0, -1]]
        mask = np.asarray(mask)
        compare = np.zeros_like(img)
        while not np.array_equal(img, compare):
            compare = img
            for i in range(9):
                img = img | ImageTransform.hit_miss(img, mask)
                ImageTransform.rotate_mask(mask)
            ImageTransform.rotate_mask(mask)
        return img

    @staticmethod
    def hit_miss(img, mask):
        res = np.zeros_like(img)
        print(img.shape)
        for i in range(len(img)):
            for j in range(len(img[0])):
                temp_mask = mask
                if j == 0:
                    temp_mask = temp_mask[1:]
                    cut = img[:, j:j+2]
                elif j == len(img) - 1:
                    temp_mask = temp_mask[:-1]
                    cut = img[:, j-1:j+1]
                else:
                    cut = img[:, j - 1:j + 2]
                if i == 0:
                    temp_mask = temp_mask[:, 1:]
                    cut = cut[i:i+2, :]
                elif i == len(img[0]) - 1:
                    temp_mask = temp_mask[:, :-1]
                    cut = cut[i-1:i+1, :]
                else:
                    cut = cut[i - 1:i + 2, :]
                res[i, j] = ImageTransform.compare(cut, temp_mask)
        return res

    @staticmethod
    def compare(a, b):
        x, y = len(a[0]), len(a)
        for i in range(x):
            for j in range(y):
                if b[i, j] == 1 and a[i, j] != 255:
                    return 0
                if b[i, j] == -1 and a[i, j] != 0:
                    return 0
        return 255

    @staticmethod
    def rotate_mask(mask):
        rows, columns = (len(mask), len(mask[0]))
        border = mask[0] + [i[-1] for i in mask[1:-1]] + list(reversed(mask[-1])) + [i[0] for i in mask[-2:0:-1]]
        np.insert(border, 0, border[-1])
        border = border[:-1]
        for i in range(columns):
            mask[0][i] = border[i]
            mask[-1][-(1+i)] = border[i + rows + columns - 2]
        for i in range(rows - 1):
            mask[i][-1] = border[columns + i - 1]
            mask[-(1 + i)][0] = border[-rows + i + 1]

