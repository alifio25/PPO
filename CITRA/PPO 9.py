import cv2
import numpy as np

#================#
# CAMERA SETUP   #
#================#
pixel_per_cm = None
locked_area = None
cap = cv2.VideoCapture(1, cv2.CAP_MSMF)

if not cap.isOpened():
    print("Droidcam tidak dapat dibuka!")
    exit()

#====================================#
# PREPROCCESSING WITH OUTPUT STAGES  #
#====================================#
def preproccessing(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _,  thresh = cv2.threshold(
        blur, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    closing = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel)

    return gray, blur, thresh, opening, closing

#============#
# MAIN LOOP  #
#============#
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray, blur, thresh, opening, closing = preproccessing(frame)

    edges = cv2.Canny(closing, 50, 150)

#==============================#
# FIXED CONTOUR FOR HOLED LEAF #
#==============================#
countours, hierarchy = cv2.findContours(
    proccessed,
    cv2.RETR_TREE,
    cv2.CHAIN_APPROX_SIMPLE
)

area_cm2 = None
if countours is not None and hierarchy is not None:

    area_pixels = 0

    for i, cnt in enumerate(countours):
        area = cv2.contourArea(cnt)

        #Kontur tama (Luar daun)
        if hierarchy[0][i][3] == -1:
            area_pixels += area
        # Kontur lubang (di dalam daun)
        else:
            area_pixels -= area

    cv2.drawContours(frame, countours, -1, (0, 255, 0), 2)
    
    if pixel_per_cm is not None:
        area_cm2 = area_pixels / (pixel_per_cm ** 2)

#==============================#
# DISPLAY AREA #
#==============================#
if pixel_per_cm is not None and area_cm2 is not None:
    cv2.putText(
        frame,
        f"Area: {area_cm2:.2f} cm^2",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )