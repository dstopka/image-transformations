import numpy as np
import cv2
import math
import matplotlib.pyplot as plt


def calculate_cdf(histogram):
    cdf = histogram.cumsum()
    normalized_cdf = cdf / cdf[-1]
    return normalized_cdf


def calculate_lookup(src_cdf, ref_cdf):
    lookup_table = np.zeros(256)
    lookup_val = 0
    for src_pixel_val in range(len(src_cdf)):
        for ref_pixel_val in range(len(ref_cdf)):
            if ref_cdf[ref_pixel_val] >= src_cdf[src_pixel_val]:
                lookup_val = ref_pixel_val
                break
        lookup_table[src_pixel_val] = lookup_val
    return lookup_table


def match_histograms(src_image, ref_hist):
    src_hist, bin = np.histogram(src_image.flatten(), 256, [0, 256])
    plt.subplot(2, 2, 3)
    plt.bar(range(0, 256), src_hist)
    src_cdf = calculate_cdf(src_hist)
    ref_cdf = calculate_cdf(ref_hist)
    # plt.subplot(2, 2, 1), plt.bar(range(0, 256), src_cdf)
    # plt.subplot(2, 2, 2), plt.bar(range(0, 256), ref_cdf)
    # plt.show()  # To show figure
    lookup_table = calculate_lookup(src_cdf, ref_cdf)
    lut_image = [[lookup_table[x] for x in y] for y in src_image]
    return np.array(lut_image)


def mono_condition(i, hist):
    if i < 0:
        hist[0] += 1
        return 0
    if i >= 256:
        hist[256 - 1] += 1
        return 256 - 1
    hist[i] += 1
    return i


class ImageTransform:
    @staticmethod
    def gauss_hist(source, stdd):
        std = stdd
        gauss_values = np.zeros(256)
        for i in range(256):
            gauss_values[i] = math.exp(-(i / 255 - 0.5)**2 / (2 * std * std))
        # plt.bar(range(0, 256), gauss_values)
        # plt.subplot(2, 2, 4), plt.bar(range(0, 256), gauss_values)
        # plt.subplot(2, 2, 3), plt.bar(range(0, 256), gauss_values)
        res = match_histograms(source, gauss_values)
        src_hist1, bin1 = np.histogram(res.flatten(), 256, [0, 256])
        plt.subplot(2, 2, 1), plt.imshow(source, cmap='gray', vmin=0, vmax=255)
        plt.subplot(2, 2, 2), plt.imshow(res, cmap='gray', vmin=0, vmax=255)
        plt.subplot(2, 2, 4), plt.bar(range(0, 256), src_hist1)
        # plt.subplot(2, 2, 3), plt.bar(range(0, 256), gauss_values)
        plt.show()


    @staticmethod
    def cdf(h):
        n = np.sum(h)
        c = 0
        P = []
        for i in range(len(h)):
            c += h[i]
            P.append(c / n)
        return P

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
