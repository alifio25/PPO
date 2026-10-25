import cv2
import numpy as np

# Baca gambar
img = cv2.imread('C:/Users/User/OneDrive/Desktop/CODE PPO_Alifio Eren/image.png')
h, w = img.shape[:2]

# Tentukan ukuran baru
new_w, new_h = 200, 200

# Hitung sekala
scale_x = w / new_w
scale_y = h / new_h

# Buat array kosong untuk hasil resize
resize_manual = np.zeros((new_h, new_h, 3), dtype=np.uint8)

# Isi piksel satu persatu 
for y_new in range(new_h):
    for x_new in range(new_w):
        # Hitung koordinat asal di gambar lama
        x_old = int(x_new * scale_x)
        y_old = int(y_new * scale_y)

        # Ambil nilai dari gambar asli 
        resize_manual[y_new, x_new] = img[y_old, x_old]

# Tampilkan hasil
cv2.imshow('Asli', img)
cv2.imshow('Resize Manual', resize_manual)
cv2.waitKey(0)
cv2.destroyAllWindows()