# MORFOLOGI GABUNGAN

import cv2
import numpy as np

# Baca citra grayscale
gray = cv2.imread('C:/Users/User/OneDrive/Desktop/CODE PPO_Alifio Eren/img_Daun/Daun_Bolong/Daun_Bolong (2).jpeg', cv2.IMREAD_GRAYSCALE)

# Cek apakah citra berhasil dibaca
if gray is None:
    raise FileNotFoundError("Citra tidak ditemukan, periksa kembali path file")

gray = cv2.resize(gray, (400, 400))

# Thresholding untuk mendapatkan citra biner
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Structuring elemen (kernel)
kernel = np.ones((3, 3), np.uint8)

# Operasi morfologi dasar
erosi = cv2.erode(thresh, kernel, iterations=1)
dilasi = cv2.dilate(thresh, kernel, iterations=1)

# Operasi morfologi gabungan
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Tampilkan hasil
cv2.imshow('Grayscale', gray)
cv2.imshow('Thresholding', thresh)
cv2.imshow('Erosi', erosi)
cv2.imshow('Dilasi', dilasi)
cv2.imshow('Opening', opening)
cv2.imshow('Closing', closing)

cv2.waitKey(0)
cv2.destroyAllWindows()