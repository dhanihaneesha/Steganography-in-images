import numpy
import math
import cv2
import sys

original = cv2.imread(sys.argv[1])
contrast = cv2.imread("embed.png", 1)


def psnr(img1, img2):
    mse = numpy.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))


d = psnr(original, contrast)
print(d)
