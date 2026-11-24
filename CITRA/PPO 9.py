import cv2
import numpy as np

# =========================
# CAMERA SETUP
# =========================
pixel_per_cm = None 
locked_area = None
cap = cv2.VideoCapture(None, cv2.CAP_MSMF)

if not cap.isOpened():
    print("DroidCam tidak dapat dibuka!")
    exit()

# =========================
# PREPROCESSING WITH OUTPUT STAGES
# =========================
def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    _, thresh = cv2.threshold(
        blur, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    closing = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel)

    return gray, blur, thresh, opening, closing

# =========================
# MAIN LOOP
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray, blur, thresh, opening, processed = preprocess(frame)

    edges = cv2.Canny(processed, 50, 150)

    # =========================
    # FIXED CONTOUR FOR HOLED LEAF
    # =========================
    contours, hierarchy = cv2.findContours(
        processed,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    area_cm2 = None

    if contours is not None and hierarchy is not None:

        area_pixels = 0

        for i, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)

            # kontur utama (luar daun)
            if hierarchy[0][i][3] == -1:
                area_pixels += area
            # kontur lubang (di dalam daun)
            else:
                area_pixels -= area

        cv2.drawContours(frame, contours, -1, (0,255,0), 2)

        if pixel_per_cm is not None:
            area_cm2 = area_pixels / (pixel_per_cm ** 2)

    # =========================
    # DISPLAY AREA (UNCHANGED)
    # =========================
    if pixel_per_cm is not None and area_cm2 is not None:

        display_area = locked_area if locked_area is not None else area_cm2

        cv2.putText(
            frame,
            f"Area: {display_area:.2f} cm2",
            (10,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

    cv2.putText(
        frame,
        "C=Kalibrasi | S=Kunci | R=Reset | Q=Keluar",
        (10,460),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255,255,255),
        2
    )

    # =========================
    # SHOW ALL PROCESS STAGES
    # =========================
    cv2.imshow("Kamera", frame)
    cv2.imshow("Grayscale", gray)
    cv2.imshow("Gaussian Blur", blur)
    cv2.imshow("Otsu Threshold", thresh)
    cv2.imshow("Opening", opening)
    cv2.imshow("Closing (Final Segment)", processed)
    cv2.imshow("Canny Edge", edges)

    key = cv2.waitKey(1) & 0xFF

    # =========================
    # CALIBRATION (UNCHANGED)
    # =========================
    if key == ord('c'):
        print("Kalibrasi... arahkan penggaris")

        if contours:
            ref = max(contours, key=cv2.contourArea)

            rect = cv2.minAreaRect(ref)
            box = cv2.boxPoints(rect)
            box = box.astype(int)

            d1 = np.linalg.norm(box[0] - box[1])
            d2 = np.linalg.norm(box[1] - box[2])

            pixel_length = max(d1, d2)

            known_length_cm = 10.0
            pixel_per_cm = pixel_length / known_length_cm

            print("Panjang piksel:", pixel_length)
            print("Pixel per cm:", pixel_per_cm)

    elif key == ord('s'):
        if area_cm2 is not None:
            locked_area = area_cm2
            print("Luas dikunci:", locked_area)

    elif key == ord('r'):
        locked_area = None
        print("Reset ke realtime")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()