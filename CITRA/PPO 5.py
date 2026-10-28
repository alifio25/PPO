# ROTASI

import cv2
import numpy as np
import math

# Baca gambar
img = cv2.imread('C:/Users/User/OneDrive/Desktop/CODE PPO_Alifio Eren/image.png')
img = cv2.resize(img, (200, 200))
h, w = img.shape[:2]

# Sudut rotasi (misal 45 derajat)
theta = math.radians(90)

# Titik pusat rotasi
x_c, y_c = w // 2, h // 2

# Buat canvas kosong 
rotated =np.zeros_like (img)

for y_new in range (h):
    for x_new in range (w):
        # Hitung koordinat asal (inverse rotation)
        X_old = (x_new - x_c) * math.cos(theta) + (y_new - y_c) * math.sin(theta) + y_c
        y_old = (x_new - x_c) * math.sin(theta) + (y_new - y_c) * math.cos(theta) + y_c

        # Cek apakah masih dalam batas gambar asli 
        if 0 <= int (X_old) < w and 0 <= int (y_old) < h:
            rotated[y_new, x_new] = img[int(y_old), int(X_old)]

# Tampilkan hasil 
cv2.imshow('Asli', img)
cv2.imshow('Rotasi manual', rotated)
cv2.waitKey (0)
cv2.destroyAllWindows()