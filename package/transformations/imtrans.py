import numpy as np
import cv2
import math

class ImageTransform:
    @staticmethod
    def gauss_hist(img):
        gauss = np.random.normal()

    @staticmethod
    def filt_entropy(img):
        pass

    @staticmethod
    def imopen(img, params):
        se = ImageTransform.liner_se(params[0], params[1])
        return ImageTransform.dilate(ImageTransform.erode(img, se), se)

    @staticmethod
    def convex_hull(img):
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
    def dilate(img, mask):
        res = np.zeros_like(img)
        x, y = img.shape
        P, Q = mask.shape
        for i in range(math.ceil(P/2), x-math.floor(P/2)):
            for j in range(math.ceil(Q / 2), y - math.floor(Q / 2)):
                on = img[i - math.floor(P / 2):i + math.floor(P / 2)+1, j - math.floor(Q / 2): j + math.floor(Q / 2)+1]
                bool_idx = (mask == 1)
                res[i, j] = max(on[bool_idx])
        return res

    @staticmethod
    def hit_miss(img, mask):
        true_mask = mask * (mask == 1)
        false_mask = mask * (mask == -1) * -1
        res = ImageTransform.erode(img, true_mask) & ImageTransform.erode(~img, false_mask)
        return res

    @staticmethod
    def liner_se(length, angle):
        theta = math.radians(angle)
        dx = abs(math.cos(theta))
        dy = abs(math.sin(theta))
        lgx = length * dx
        n2x = round((lgx - 1) / 2)
        nx = 2 * n2x + 1
        lgy = length * dy
        n2y = round((lgy - 1) / 2)
        ny = 2 * n2y + 1
        mask = np.zeros([ny, nx])
        if math.cos(theta) >= 0:
            el = ImageTransform.bresenham(0, ny-1, nx-1, 0)
        else:
            el = ImageTransform.bresenham( nx-1, ny-1, 0, 0 )
        for x in el:
            mask[x[1], x[0]] = 1
        return mask


    @staticmethod
    def bresenham(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        is_steep = abs(dy) > abs(dx)

        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True

        dx = x2 - x1
        dy = y2 - y1

        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

        if swapped:
            points.reverse()
        return points
