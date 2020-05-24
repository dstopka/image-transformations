import numpy as np
import cv2
import math
import matplotlib.pyplot as plt


def image_type(src_image):
    """
    This method checks what type the source image is based
    on number of channels and pixel values
    :param np.array src_image: The original source image
    :return: The source image type
    :rtype: str
    """
    try:
        height, width, channels = src_image.shape
    except ValueError:
        height, width = src_image.shape
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


def calculate_histogram(src_channel):
    """
    This method calculates the histogram of given image channel
    as a flat array
    :param np.array src_channel: The image channel
    :return: histogram : The histogram
    :rtype: np.array
    """
    histogram = np.zeros(256)
    for y in src_channel:
        histogram[y] += 1

    return histogram


def calculate_lookup(src_cdf, ref_cdf):
    """
    This method creates the lookup table
    :param np.array src_cdf: The cdf for the source image
    :param np.array ref_cdf: The cdf for the normal distribution
    :return: lookup_table : The lookup table
    :rtype: np.array
    """
    n = 0
    max_n = 10
    lookup_table = np.zeros(256)
    for idx in range(256):
        if src_cdf[idx] >= ref_cdf[round(255 / max_n * (n + 1))]:
            n += 1
            if n >= max_n:
                n = max_n - 1
        lookup_table[idx] = int(((256 - 1) * n) / (max_n - 1))

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
    src_hist = calculate_histogram(src_image.flatten())
    # Calculate normalized cumulative distribution functions
    src_cdf = calculate_cdf(src_hist)
    ref_cdf = calculate_cdf(ref_hist)

    # Calculate lookup table
    lookup_table = calculate_lookup(src_cdf, ref_cdf)

    # Match source with lookup table
    matched_image = np.array([[lookup_table[x] for x in y] for y in src_image], dtype=np.uint8)
    hist_m = calculate_histogram(matched_image)
    plt.bar(range(256), hist_m)
    plt.show()
    # print(matched_image[:1, :])
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
    src_hist_blue = calculate_histogram(src_b.flatten())
    src_hist_green = calculate_histogram(src_g.flatten())
    src_hist_red = calculate_histogram(src_r.flatten())

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


def histogram_matching(src_image, std):
    """
    This method performs histogram matching of
    the source image and the reference normal distribution
    of specified standard deviation
    :param np.array src_image: The original source image
    :param int  std: The value of the standard deviation
    :return: matched_image: The image after matching
    :rtype: np.array
    """
    # Calculate normal distribution histogram
    normal_distribution = np.zeros(256)
    for i in range(256):
        normal_distribution[i] = math.exp(-(i / 255 - 0.5) ** 2 / (2 * std * std)) / 10

    # Check if mono or rgb
    source_type = image_type(src_image)
    if source_type == 'mono' or source_type == 'binary':
        matched_image = match_histograms_mono(src_image, normal_distribution)
    else:
        matched_image = match_histograms_rgb(src_image, normal_distribution)

    return matched_image


def entropy_filter(src_image, mask_size):
    """
    This method creates the entropy filter on
    the given source image with the mask
    of the given size
    :param np.array src_image: The source image
    :param int mask_size: The size of the mask
    :return: result_image: The image after filtering
    :rtype: np.array
    """
    mask_half = math.floor(mask_size/2)
    img_height, img_width = src_image.shape[:2]
    result_image = np.zeros((img_height, img_width))

    for i in range(img_height):
        for j in range(img_width):
            Lx = np.max([0, j - mask_half])
            Ux = np.min([img_width, j + mask_half])
            Ly = np.max([0, i - mask_half])
            Uy = np.min([img_height, i + mask_half])
            region = src_image[Ly:Uy, Lx:Ux]
            res = entropy(region)
            result_image[i, j] = res

    min_entropy = min(result_image.flatten())
    max_entropy = max(result_image.flatten())
    result_image = (result_image - min_entropy) / (max_entropy - min_entropy) * 255
    result_image = result_image.astype(np.uint8)

    return result_image


def entropy(region):
    """
    This method calculates entropy in
    the given region of the source image
    :param np.array region: The region to calculate entropy in
    :return: entropy_value: The value of the entropy
    :rtype: float
    """

    # calculate histograms of all channels
    if image_type(region) == 'BGR':
        histogram = (calculate_histogram(region[:, :, 0].flatten()) +
                    calculate_histogram(region[:, :, 1].flatten()) +
                    calculate_histogram(region[:, :, 2].flatten())) / (region.shape[0] * region.shape[1] * 3)
    else:
        histogram = calculate_histogram(region.flatten()) / (region.shape[0] * region.shape[1])

    # calculate the entropy
    histogram = list(filter(lambda p: p > 0, histogram))
    entropy_value = -np.sum(np.multiply(np.log(histogram), histogram))

    return entropy_value


def imopen(src_image, se_length, se_angle):
    """
    This method performs image opening based on
    the angled linear structuring element created
    based on given values
    :param np.array src_image: The original source image
    :param int se_length: The structuring element length
    :param int se_angle: The structuring element angle
    :return: result_image: The image after opening
    :rtype: np.array
    """
    # Create linear se
    se = liner_se(se_length, se_angle)

    # Compute dilation over erosion
    result_image = dilate(erode(src_image, se), se)

    return result_image


def convex_hull(src_image):
    """
    This method computes convex hull
    on the input image
    :param np.array src_image: The original source image
    :return: result_image: The image after convex hull
    :rtype: np.array
    """
    # create structural elements
    se_0deg = np.array([[1, 1, 0], [1, -1, 0], [1, 0, -1]], dtype=np.int)
    se_45deg = np.array([[1, 1, 1], [1, -1, 0], [0, -1, 0]], dtype=np.int)

    # allocate comparison image to enter while
    compare = np.zeros_like(src_image)
    result_image = src_image

    # perform hit-or-miss until no change
    while not np.array_equal(result_image, compare):
        compare = result_image

        # hit-or-miss for each se position
        for i in range(4):
            result_image = result_image | hit_miss(result_image, se_0deg)
            result_image = result_image | hit_miss(result_image, se_45deg)
            se_0deg = np.rot90(se_0deg)
            se_45deg = np.rot90(se_45deg)

    return result_image


def erode(src_image, se):
    """
    This method performs morphological erosion
    based on given structuring element
    :param np.array src_image: The original source image
    :param np.array se: The structuring element
    :return: result_image: The image after erosion
    :rtype: np.array
    """
    result_image = np.zeros_like(src_image)
    img_width, img_height = src_image.shape[:2]
    mask_x, mask_y = se.shape[:2]
    mask_half_x = math.floor(mask_x / 2)
    mask_half_y = math.floor(mask_y / 2)
    for i in range(math.ceil(mask_x / 2), img_width - math.floor(mask_x / 2)):
        for j in range(math.ceil(mask_y / 2), img_height - mask_half_y):
            on = src_image[i - mask_half_x:i + mask_half_x + 1, j - mask_half_y: j + mask_half_y + 1]
            bool_idx = (se == 1)
            result_image[i, j] = min(on[bool_idx])

    return result_image


def dilate(src_image, se):
    """
    This method performs morphological dilation
    based on given structuring element
    :param np.array src_image: The original source image
    :param np.array se: The structuring element
    :return: result_image: The image after dilation
    :rtype: np.array
    """
    result_image = np.zeros_like(src_image)
    img_width, img_height = src_image.shape[:2]
    mask_x, mask_y = se.shape[:2]
    mask_half_x = math.floor(mask_x / 2)
    mask_half_y = math.floor(mask_y / 2)
    for i in range(math.ceil(mask_x / 2), img_width - math.floor(mask_x / 2)):
        for j in range(math.ceil(mask_y / 2), img_height - mask_half_y):
            on = src_image[i - mask_half_x:i + mask_half_x + 1, j - mask_half_y: j + mask_half_y + 1]
            bool_idx = (se == 1)
            result_image[i, j] = max(on[bool_idx])

    return result_image


def hit_miss(src_image, se):
    """
    This method performs hit-or-miss operation
    based on given structuring element
    using logical and of two erosion
    :param np.array src_image: The original source image
    :param np.array se: The structuring element
    :return: result_image: The image after dilation
    :rtype: np.array
    """
    # create mask [0, 1] from [-1, 0, 1]
    true_mask = se * (se == 1)
    false_mask = se * (se == -1) * -1

    # perform two erosion to get hit-or-miss
    result_image = erode(src_image, true_mask) & erode(~src_image, false_mask)

    return result_image


def liner_se(length, angle):
    """
    This method creates linear structuring element
    of given length and angle
    :param int length: The structuring element length
    :param int angle: The structuring element angle
    :return: result_se: The crated SE
    :rtype: np.array
    """
    theta = math.radians(angle)
    dx = abs(math.cos(theta))
    dy = abs(math.sin(theta))

    lgx = length * dx
    n2x = round((lgx - 1) / 2)
    nx = 2 * n2x + 1

    lgy = length * dy
    n2y = round((lgy - 1) / 2)
    ny = 2 * n2y + 1

    result_se = np.zeros([ny, nx])
    if math.cos(theta) >= 0:
        points = bresenham(0, ny - 1, nx - 1, 0)
    else:
        points = bresenham(nx - 1, ny - 1, 0, 0)

    for x in points:
        result_se[x[1], x[0]] = 1

    return result_se


def bresenham(x1, y1, x2, y2):
    """
    This method performs bresenham algorithm of
    creating line between two points
    :param int x1: The first point x coordinate
    :param int y1: The first point y coordinate
    :param int x2: The second point x coordinate
    :param int y2: The second point y coordinate
    :return: points: indexes of line points
    :rtype: np.array
    """
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
