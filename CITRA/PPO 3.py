import cv2

img = cv2.imread('C:/Users/User/OneDrive/Desktop/CODE PPO_Alifio Eren/image.png')
resize = cv2.resize(img, (200, 200), interpolation=cv2.INTER_NEAREST)

cv2.imshow('Asli 2', img)
cv2.imshow('Resize Manual 2', resize)
cv2.waitKey(0)
cv2.destroyAllWindows()