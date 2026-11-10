# DETEKSI TEPI (CANNY, PREWITT, SOBEL, LAPLACIAN)

import cv2
import numpy as np

img = cv2.imread('C:/Users/User/OneDrive/Desktop/CODE PPO_Alifio Eren/semangka 1.webp')
img = cv2.resize(img, (400, 400))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

canny = cv2.Canny(gray, 100, 200)
laplacian = cv2.Laplacian(gray, cv2.CV_64F)
laplacian =np.uint8(np.absolute(laplacian))
sobel = cv2.magnitude(
    cv2.Sobel(gray, cv2.CV_64F, 1, 0, 3),
    cv2.Sobel(gray, cv2.CV_64F, 0, 1, 3)
)
sobel = np.uint8(np.clip(sobel, 0, 255))
kernel_prewitt_x = np.array([
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1]
], dtype=np.float32)

kernel_prewitt_y = np.array([
    [1,   1 , 1],
    [0 ,  0,  0],
    [-1, -1, -1]
], dtype=np.float32)

prewittx = cv2.filter2D(gray, -1, kernel_prewitt_x)
prewitty = cv2.filter2D(gray, -1, kernel_prewitt_y)
prewitt = cv2.magnitude(prewittx.astype(np.float32), prewitty.astype(np.float32))
prewitt = np.uint8(np.clip(prewitt, 0, 255))

cv2.imshow("Asli", img)
cv2.imshow("Canny", canny)
cv2.imshow("Laplacian", laplacian)
cv2.imshow("Sobel", sobel)
cv2.imshow("Prewitt", prewitt)
cv2.waitKey(0)
cv2.destroyAllWindows()