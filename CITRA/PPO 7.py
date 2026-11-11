# Topologi Citra

# MORFOLOGI EROSI

import cv2
import numpy as np

# Baca citra grayscale
gray = cv2.imread('C:/Users/User/OneDrive/Desktop/CODE PPO_Alifio Eren/img_Daun/Daun_Bolong/Daun_Bolong (2).jpeg', cv2.IMREAD_GRAYSCALE)
gray = cv2.resize(gray, (400, 400))

# Thresholding untuk mendapatkan citra biner 
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
thresh = cv2.resize(thresh, (400, 400))

# Structuring elemen (kernel)
kernel = np.ones((3, 3), np.uint8)

# Operasi morfologi erosi
erosi = cv2.erode(thresh, kernel, iterations=1)
erosi = cv2.resize(erosi, (400, 400))

#Tampilkan hasil
cv2.imshow('Grayscale', gray)
cv2.imshow('Thresholding', thresh)
cv2.imshow('Erosi', erosi)

cv2.waitKey(0)
cv2.destroyAllWindows()