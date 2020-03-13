import cv2 as cv
import numpy as np
import os
from sklearn.cluster import DBSCAN
import collections

IMG_DIR = 'ground_crack_samples'
OUT_DIR = 'output_edges'


def read_img(file_name):
    path = os.path.join(IMG_DIR, file_name)
    img = cv.imread(path)
    return img


def write_img(file_name, src_img):
    path = os.path.join(OUT_DIR, file_name)
    cv.imwrite(path, img)


def cvt_to_bin_img(src_img):
    img = src_img.copy()
    img = cv.medianBlur(src_img, 7)
    img = cv.adaptiveThreshold(
        img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 2)

    return img


def img_to_points(img):
    points = []

    height, width = img.shape
    for y in range(height):
        for x in range(width):
            if img[y, x] != 0:
                points.append([y, x])
    return points

def filter_labels(img, labels):
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    avg_points = len(labels) // n_clusters
    counters = collections.Counter(labels)
    satisfied_labels = [k for k, v in counters.items() if v > 7*avg_points]

    return satisfied_labels


def remove_noise(img):
    X = img_to_points(img)

    # compute DBSCAN
    db = DBSCAN(eps=1.5, min_samples=1).fit(X)
    labels = db.labels_

    satisfied_labels = filter_labels(img, labels)

    for k, yx in zip(labels, X):
        if k == -1 or k in satisfied_labels:
            continue

        img[yx[0], yx[1]] = 0

    return img


if __name__ == "__main__":
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    for file_name in os.listdir(IMG_DIR):

        ### READ IMAGE ###
        src_img = read_img(file_name)
        img = src_img.copy()
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        img = cvt_to_bin_img(img)
        img = remove_noise(img)

        ### WRITE IMAGE ###
        write_img(file_name, img)
