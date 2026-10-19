import cv2

CITRA = cv2.imread ("C:/Users/User/OneDrive/Desktop/CODE PPO_Alifio Eren/Pigai.webp")

print (CITRA[:,:,0])
print (CITRA[:,:,1])
print (CITRA[:,:,2])
print (CITRA)

cv2.imshow ("blue", CITRA[:,:,2])
cv2.imshow ("green", CITRA[:,:,1])
cv2.imshow ("red", CITRA[:,:,0])
cv2.imshow ("asli", CITRA)
cv2.waitKey()



# python -m pip install opencv-python