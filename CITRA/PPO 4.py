# GRAYSCALE KE BINARY
import cv2
import numpy as np

# Baca gambardan ubah ke grayscale
img = cv2.imread('C:/Users/User/OneDrive/Desktop/CODE PPO_Alifio Eren/image.png', cv2.IMREAD_GRAYSCALE)

# Tentukan nilai ambang (threshold)
treshold = 90 #bisa di ubah antara 0-255

# Buat array kosong untuk hasil biner
binary_manual = np.zeros_like(img)

# Terapkan proses binerisasi manual
binary_manual[img >= treshold] = 255
binary_manual[img <= treshold] = 0

# Tampilkan hasil
cv2.imshow('Grayscale', img)
cv2.imshow('Biner Manual', binary_manual)
cv2.waitKey(0)
cv2.destroyAllWindows()