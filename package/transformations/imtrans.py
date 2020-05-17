import numpy as np
import cv2
import math
import matplotlib.pyplot as plt


def img_type(src_image):
    """
    This method checks what type the source image is based
    on number of channels and pixel values
    :param np.array src_image: The original source image
    :return: The source image type
    :rtype: str
    """
    try:
        width, height, channels = src_image.shape
    except ValueError:
        width, height = src_image.shape
        channels = None
    if channels:
        return 'BGR'
    for x in range(height):
        for y in range(width):
            if src_image[y, x] != 0 and src_image[y, x] != 255:
                return 'mono'
    return 'binary'


def calculate_cdf(histogram):
    """
    This method calculates the cumulative distribution function
    :param np.array histogram: The values of the histogram
    :return: normalized_cdf : The normalized cumula
    :rtype: np.array
    """
    # Get cumulative sum of the histogram
    cdf = histogram.cumsum()

    # Normalize the cdf
    normalized_cdf = cdf / cdf[-1]

    return normalized_cdf


def calculate_lookup(src_cdf, ref_cdf):
    """
    This method creates the lookup table
    :param np.array src_cdf: The cdf for the source image
    :param np.array ref_cdf: The cdf for the normal distribution
    :return: lookup_table : The lookup table
    :rtype: np.array
    """
    lookup_table = np.zeros(256)
    lookup_val = 0
    for src_pixel_val in range(len(src_cdf)):
        for ref_pixel_val in range(len(ref_cdf)):
            if ref_cdf[ref_pixel_val] >= src_cdf[src_pixel_val]:
                lookup_val = ref_pixel_val
                break
        lookup_table[src_pixel_val] = lookup_val
    return lookup_table


def match_histograms_mono(src_image, ref_hist):
    """
    This method matches the source monochrome image histogram
    to the reference normal distribution
    :param np.array src_image: The original source image
    :param np.array  ref_hist: The values of the normal distribution
    :return: matched_image: The image after matching
    :rtype: np.array
    """
    # Calculate image histogram
    src_hist, bin = np.histogram(src_image.flatten(), 256, [0, 256])

    # Calculate normalized cumulative distribution functions
    src_cdf = calculate_cdf(src_hist)
    ref_cdf = calculate_cdf(ref_hist)

    # Calculate lookup table
    lookup_table = calculate_lookup(src_cdf, ref_cdf)

    # Match source with lookup table
    matched_image = np.array([[lookup_table[x] for x in y] for y in src_image], dtype=np.uint8)

    return matched_image


def match_histograms_rgb(src_image, ref_hist):
    """
    This method matches the source BGR image histogram
    to the reference normal distribution
    :param np.array src_image: The original source image
    :param np.array  ref_hist: The values of the normal distribution
    :return: matched_image: The image after matching
    :rtype: np.array
    """
    # Split channels
    src_b = src_image[:, :, 0]
    src_g = src_image[:, :, 1]
    src_r = src_image[:, :, 2]

    # Calculate image histograms
    src_hist_blue, bins = np.histogram(src_b.flatten(), 256, [0, 256])
    src_hist_green, bins = np.histogram(src_g.flatten(), 256, [0, 256])
    src_hist_red, bins = np.histogram(src_r.flatten(), 256, [0, 256])

    # Calculate normalized cumulative distribution functions
    src_cdf_blue = calculate_cdf(src_hist_blue)
    src_cdf_green = calculate_cdf(src_hist_green)
    src_cdf_red = calculate_cdf(src_hist_red)
    ref_cdf = calculate_cdf(ref_hist)

    # Calculate lookup tables
    blue_lut = calculate_lookup(src_cdf_blue, ref_cdf)
    green_lut = calculate_lookup(src_cdf_green, ref_cdf)
    red_lut = calculate_lookup(src_cdf_red, ref_cdf)

    # Match source with lookup tables
    res = np.array([[[blue_lut[b], green_lut[g], red_lut[r]] for b, g, r in x] for x in src_image], dtype=np.uint8)
    return res


def histogram_match(source, std):
    # calculate normal distribution histogram
    gauss_values = np.zeros(256)
    for i in range(256):
        gauss_values[i] = math.exp(-(i / 255 - 0.5) ** 2 / (2 * std * std))

    # check if mono or rgb
    source_type = img_type(source)
    if source_type == 'mono' or source_type == 'binary':
        res = match_histograms_mono(source, gauss_values)
    else:
        res = match_histograms_rgb(source, gauss_values)

    return res


def filt_entropy(img):
    pass


def imopen(img, se_length, se_angle):
    # create linear se
    se = liner_se(se_length, se_angle)

    # perform dilation over erosion
    return dilate(erode(img, se), se)


def convex_hull(source):
    # create structural elements
    se_0deg = np.array([[1, 1, 0], [1, -1, 0], [1, 0, -1]], dtype=np.int)
    se_45deg = np.array([[1, 1, 1], [1, -1, 0], [0, -1, 0]], dtype=np.int)

    # allocate comparison image to enter while
    compare = np.zeros_like(source)

    # perform hit-or-miss until no change
    while not np.array_equal(source, compare):
        compare = source

        # hit-or-miss for each se position
        for i in range(4):
            source = source | hit_miss(source, se_0deg)
            source = source | hit_miss(source, se_45deg)
            se_0deg = np.rot90(se_0deg)
            se_45deg = np.rot90(se_45deg)

    return source


def erode(img, mask):
    res = np.zeros_like(img)
    # x, y = img.shape
    # P, Q = mask.shape
    img_width, img_height = img.shape[:2]
    mask_x, mask_y = mask.shape[:2]
    mask_half_x = math.floor(mask_x / 2)
    mask_half_y = math.floor(mask_y / 2)
    for i in range(math.ceil(mask_x / 2), img_width - math.floor(mask_x / 2)):
        for j in range(math.ceil(mask_y / 2), img_height - mask_half_y):
            on = img[i - mask_half_x:i + mask_half_x + 1, j - mask_half_y: j + mask_half_y + 1]
            bool_idx = (mask == 1)
            res[i, j] = min(on[bool_idx])
    return res


def dilate(img, mask):
    res = np.zeros_like(img)
    # x, y = img.shape
    # P, Q = mask.shape
    img_width, img_height = img.shape[:2]
    mask_x, mask_y = mask.shape[:2]
    mask_half_x = math.floor(mask_x / 2)
    mask_half_y = math.floor(mask_y / 2)
    for i in range(math.ceil(mask_x / 2), img_width - math.floor(mask_x / 2)):
        for j in range(math.ceil(mask_y / 2), img_height - mask_half_y):
            on = img[i - mask_half_x:i + mask_half_x + 1, j - mask_half_y: j + mask_half_y + 1]
            bool_idx = (mask == 1)
            res[i, j] = max(on[bool_idx])
    return res


def hit_miss(img, mask):
    # create mask [0, 1] from [-1, 0, 1]
    true_mask = mask * (mask == 1)
    false_mask = mask * (mask == -1) * -1

    # perform two erosion to get hit-or-miss
    res = erode(img, true_mask) & erode(~img, false_mask)

    return res


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
        el = bresenham(0, ny - 1, nx - 1, 0)
    else:
        el = bresenham(nx - 1, ny - 1, 0, 0)
    for x in el:
        mask[x[1], x[0]] = 1

    return mask


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
