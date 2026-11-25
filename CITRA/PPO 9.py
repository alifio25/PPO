import cv2
import numpy as np

# =========================
# CAMERA SETUP
# =========================
pixel_per_cm = None
locked_area = None

# Kamera DroidCam
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Kamera/DroidCam tidak dapat dibuka!")
    exit()

print("DroidCam berhasil dibuka")


# =========================
# PREPROCESSING
# =========================
def preprocess(image):

    # 1. Grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # 2. Gaussian Blur
    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    # 3. Otsu Threshold
    _, thresh = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # 4. Morphology
    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (9, 9)
    )

    # Opening
    opening = cv2.morphologyEx(
        thresh,
        cv2.MORPH_OPEN,
        kernel
    )

    # Closing
    closing = cv2.morphologyEx(
        opening,
        cv2.MORPH_CLOSE,
        kernel
    )

    # Closing kedua untuk menutup lubang kecil
    closing = cv2.morphologyEx(
        closing,
        cv2.MORPH_CLOSE,
        kernel
    )

    return (
        gray,
        blur,
        thresh,
        opening,
        closing
    )


# =========================
# MAIN LOOP
# =========================
while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame kamera tidak terbaca!")
        break

    # =========================
    # PREPROCESSING
    # =========================
    gray, blur, thresh, opening, processed = preprocess(frame)

    # =========================
    # CANNY EDGE
    # =========================
    edges = cv2.Canny(
        processed,
        50,
        150
    )

    # =========================
    # FIND CONTOUR
    # =========================
    contours, hierarchy = cv2.findContours(
        processed,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    area_cm2 = None
    area_pixels = 0

    # =========================
    # CALCULATE AREA
    # =========================
    if hierarchy is not None and len(contours) > 0:

        for i, cnt in enumerate(contours):

            area = cv2.contourArea(cnt)

            # Kontur luar
            if hierarchy[0][i][3] == -1:
                area_pixels += area

            # Kontur di dalam / lubang
            else:
                area_pixels -= area

        # Gambar semua kontur
        cv2.drawContours(
            frame,
            contours,
            -1,
            (0, 255, 0),
            2
        )

        # =========================
        # CONVERT PIXEL TO CM
        # =========================
        if pixel_per_cm is not None:

            area_cm2 = (
                area_pixels /
                (pixel_per_cm ** 2)
            )

    # =========================
    # DISPLAY AREA
    # =========================
    if (
        pixel_per_cm is not None
        and area_cm2 is not None
    ):

        if locked_area is not None:
            display_area = locked_area
        else:
            display_area = area_cm2

        cv2.putText(
            frame,
            f"Area: {display_area:.2f} cm2",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # =========================
    # INSTRUCTION
    # =========================
    cv2.putText(
        frame,
        "C=Kalibrasi | S=Kunci | R=Reset | Q=Keluar",
        (10, 460),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    # =========================
    # SHOW PROCESSING
    # =========================
    cv2.imshow(
        "Kamera",
        frame
    )

    cv2.imshow(
        "Grayscale",
        gray
    )

    cv2.imshow(
        "Gaussian Blur",
        blur
    )

    cv2.imshow(
        "Otsu Threshold",
        thresh
    )

    cv2.imshow(
        "Opening",
        opening
    )

    cv2.imshow(
        "Closing (Final Segment)",
        processed
    )

    cv2.imshow(
        "Canny Edge",
        edges
    )

    # =========================
    # KEYBOARD INPUT
    # =========================
    key = cv2.waitKey(1) & 0xFF

    # =========================
    # CALIBRATION
    # =========================
    if key == ord('c'):

        print("\nKalibrasi dimulai...")
        print("Arahkan kamera ke objek/penggaris 10 cm.")

        if len(contours) > 0:

            # Ambil kontur terbesar
            ref = max(
                contours,
                key=cv2.contourArea
            )

            # Minimum bounding rectangle
            rect = cv2.minAreaRect(ref)

            box = cv2.boxPoints(rect)
            box = box.astype(int)

            # Hitung dua sisi kotak
            d1 = np.linalg.norm(
                box[0] - box[1]
            )

            d2 = np.linalg.norm(
                box[1] - box[2]
            )

            # Ambil sisi terpanjang
            pixel_length = max(
                d1,
                d2
            )

            # Panjang sebenarnya
            known_length_cm = 10.0

            # Pixel per cm
            pixel_per_cm = (
                pixel_length /
                known_length_cm
            )

            print("--------------------------")
            print(
                "Panjang piksel :",
                pixel_length
            )
            print(
                "Panjang asli   :",
                known_length_cm,
                "cm"
            )
            print(
                "Pixel per cm   :",
                pixel_per_cm
            )
            print("Kalibrasi berhasil!")
            print("--------------------------")

        else:

            print("Kontur tidak ditemukan!")
            print("Pastikan objek terlihat jelas.")

    # =========================
    # LOCK AREA
    # =========================
    elif key == ord('s'):

        if area_cm2 is not None:

            locked_area = area_cm2

            print(
                f"Luas dikunci: "
                f"{locked_area:.2f} cm2"
            )

        else:

            print(
                "Luas belum tersedia. "
                "Lakukan kalibrasi terlebih dahulu."
            )

    # =========================
    # RESET
    # =========================
    elif key == ord('r'):

        locked_area = None

        print(
            "Luas kembali ke realtime."
        )

    # =========================
    # EXIT
    # =========================
    elif key == ord('q'):

        print(
            "Program dihentikan."
        )

        break


# =========================
# RELEASE CAMERA
# =========================
cap.release()
cv2.destroyAllWindows()