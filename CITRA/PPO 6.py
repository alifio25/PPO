# DETEKSI TEPI CANNY

import cv2
import numpy as np

# Membaca gambar
img = cv2.imread('C:/Users/User/OneDrive/Desktop/CODE PPO_Alifio Eren/semangka 1.webp')
img = cv2.resize(img, (400, 400))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Kurangi noise
gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)

#---------------#
# 1. Canny      #
#---------------#
canny = cv2.Canny(gray_blur, 50, 150)
canny = cv2.resize(canny, (400, 400))

#---------------------------#
# Menampilkan semua hasil   #
#---------------------------#

cv2.imshow("1. Canny Edge Detection", canny)
cv2.imshow("4. Gambar Asli", img)

cv2.waitKey(0)
cv2.destroyAllWindows()