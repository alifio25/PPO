# GRAYSCALE KE BINARY
import cv2
import numpy as np
import math

# Baca gambardan ubah ke grayscale
img = cv2.imread('C:/Users/User/OneDrive/Desktop/CODE PPO_Alifio Eren/image.png', cv2.IMREAD_GRAYSCALE)
#----------------------------------------------------------------------------------------------#
# Resize
resize = cv2.resize(img, (200, 200), interpolation=cv2.INTER_NEAREST)
#----------------------------------------------------------------------------------------------#

# Tentukan nilai ambang (threshold)
treshold = 90 #bisa di ubah antara 0-255

# Buat array kosong untuk hasil biner
binary_manual = np.zeros_like(img)

# Terapkan proses binerisasi manual
binary_manual[img >= treshold] = 255
binary_manual[img <= treshold] = 0

#----------------------------------------------------------------------------------------------#
# ROTASI
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
#----------------------------------------------------------------------------------------------#

# Tampilkan hasil
cv2.imshow('Resize Manual', resize)
cv2.imshow('Grayscale', img)
cv2.imshow('Biner Manual', binary_manual)
cv2.imshow('Rotasi Manual', rotated)
cv2.waitKey(0)
cv2.destroyAllWindows()