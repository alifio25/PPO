# MORFOLOGI DILASI

import cv2
import numpy as np

gray = cv2.imread('C:/Users/User/OneDrive/Desktop/CODE PPO_Alifio Eren/img_Daun/Daun_Bolong/Daun_Bolong (2).jpeg', cv2.IMREAD_GRAYSCALE)
if gray is None:
    raise FileNotFoundError("Citra tidak ditemukan, periksa kembali path file")

gray = cv2.resize(gray, (400, 400))

# Thresholding untuk mendapatkan citra biner
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Structuring elemen (kernel)
kernel = np.ones((3, 3), np.uint8)

# Operasi morfologi dilasi
dilasi = cv2.dilate(thresh, kernel, iterations=1)

# Tampilkan hasil
cv2.imshow('Grayscale', gray)
cv2.imshow('Thresholding', thresh)
cv2.imshow('Dilasi', dilasi)

cv2.waitKey(0)
cv2.destroyAllWindows()