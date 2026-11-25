import cv2
import numpy as np
import os
import csv

# =====================================================
# 1. PENGATURAN LOKASI FILE DAN FOLDER
# =====================================================

# Lokasi gambar referensi kalibrasi
PATH_REFERENSI = r"C:/Users/User/OneDrive\Desktop/CODE PPO_Alifio Eren/img_Daun\daun & penggaris.png"

# Folder utama dataset
FOLDER_DATASET = r"C:/Users/User/OneDrive\Desktop/CODE PPO_Alifio Eren/img_Daun"

# Folder kategori dataset
FOLDER_KATEGORI = {
    "Sempurna": os.path.join(FOLDER_DATASET, "SEMPURNA"),
    "Berlubang": os.path.join(FOLDER_DATASET, "BERLUBANG"),
    "Rusak": os.path.join(FOLDER_DATASET, "RUSAK")
}

# Folder penyimpanan hasil
FOLDER_HASIL = os.path.join(
    FOLDER_DATASET,
    "HASIL PENGUKURAN"
)

os.makedirs(FOLDER_HASIL, exist_ok=True)

# Panjang penggaris untuk kalibrasi
PANJANG_REFERENSI_CM = 10.0

# Ekstensi gambar yang didukung
EKSTENSI = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")


# =====================================================
# 2. MEMERIKSA FILE DAN FOLDER
# =====================================================

if not os.path.isfile(PATH_REFERENSI):
    raise FileNotFoundError(
        "Gambar kalibrasi tidak ditemukan:\n" + PATH_REFERENSI
    )

for kategori, folder in FOLDER_KATEGORI.items():
    if not os.path.isdir(folder):
        raise FileNotFoundError(
            f"Folder {kategori} tidak ditemukan:\n{folder}"
        )

print("Gambar kalibrasi ditemukan.")
print("Semua folder dataset ditemukan.")


# =====================================================
# 3. MEMBACA GAMBAR REFERENSI
# =====================================================

img_ref = cv2.imread(PATH_REFERENSI)

if img_ref is None:
    raise ValueError("Gambar referensi tidak dapat dibaca!")

print("\nGambar referensi berhasil dibaca.")


# =====================================================
# 4. PROSES KALIBRASI
# =====================================================

titik = []

tinggi, lebar = img_ref.shape[:2]

# Mengatur ukuran tampilan tanpa mengubah gambar asli
skala = min(1200 / lebar, 800 / tinggi, 1.0)

lebar_tampil = int(lebar * skala)
tinggi_tampil = int(tinggi * skala)

img_tampil = cv2.resize(
    img_ref,
    (lebar_tampil, tinggi_tampil)
)


def pilih_titik(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN and len(titik) < 2:

        x_asli = int(round(x / skala))
        y_asli = int(round(y / skala))

        titik.append((x_asli, y_asli))

        print("Titik dipilih:", titik[-1])


cv2.namedWindow("KALIBRASI")
cv2.setMouseCallback("KALIBRASI", pilih_titik)

print("\n=== PROSES KALIBRASI ===")
print("1. Klik garis 0 cm pada penggaris.")
print("2. Klik garis 10 cm pada penggaris.")

while True:

    tampilan = img_tampil.copy()

    for p in titik:

        px = int(round(p[0] * skala))
        py = int(round(p[1] * skala))

        cv2.circle(
            tampilan,
            (px, py),
            6,
            (0, 0, 255),
            -1
        )

    if len(titik) == 2:

        p1 = tuple(
            int(round(v * skala)) for v in titik[0]
        )

        p2 = tuple(
            int(round(v * skala)) for v in titik[1]
        )

        cv2.line(
            tampilan,
            p1,
            p2,
            (0, 255, 0),
            2
        )

    cv2.imshow("KALIBRASI", tampilan)

    tombol = cv2.waitKey(20) & 0xFF

    if len(titik) == 2:
        cv2.waitKey(500)
        break

    if tombol == 27:
        break

cv2.destroyAllWindows()

if len(titik) != 2:
    raise ValueError("Kalibrasi dibatalkan. Jalankan ulang program.")


# Menghitung jarak piksel
jarak_pixel = float(
    np.linalg.norm(
        np.array(titik[0], dtype=float) -
        np.array(titik[1], dtype=float)
    )
)

if jarak_pixel <= 0:
    raise ValueError("Jarak kalibrasi tidak valid!")

# Menghitung pixel per cm
pixel_per_cm = jarak_pixel / PANJANG_REFERENSI_CM

print("\n=== HASIL KALIBRASI ===")
print("Panjang referensi:", PANJANG_REFERENSI_CM, "cm")
print("Jarak piksel:", jarak_pixel)
print("Pixel per cm:", pixel_per_cm)


# =====================================================
# 5. MEMBACA 50 GAMBAR DATASET
# =====================================================

daftar_gambar = []

for kategori, folder in FOLDER_KATEGORI.items():

    file_kategori = sorted([
        nama for nama in os.listdir(folder)
        if nama.lower().endswith(EKSTENSI)
    ])

    print(
        f"Jumlah gambar {kategori}:",
        len(file_kategori)
    )

    for nama_file in file_kategori:

        daftar_gambar.append({
            "kategori": kategori,
            "nama_file": nama_file,
            "path": os.path.join(folder, nama_file)
        })


if len(daftar_gambar) == 0:
    raise FileNotFoundError(
        "Tidak ada gambar dataset. Periksa isi folder kategori."
    )

print("\nTotal gambar ditemukan:", len(daftar_gambar))

if len(daftar_gambar) != 50:
    print(
        "PERHATIAN: Jumlah gambar bukan 50. "
        "Periksa kembali isi folder dataset."
    )


# =====================================================
# 6. PROSES PENGOLAHAN CITRA
# =====================================================

hasil_pengukuran = []

for nomor, data in enumerate(daftar_gambar, start=1):

    kategori = data["kategori"]
    nama_file = data["nama_file"]
    path_gambar = data["path"]

    print("\n------------------------------------")
    print(f"Data ke-{nomor} dari {len(daftar_gambar)}")
    print("Kategori:", kategori)
    print("Nama file:", nama_file)

    img = cv2.imread(path_gambar)

    if img is None:

        print("Gagal membaca gambar.")

        hasil_pengukuran.append([
            kategori,
            nama_file,
            "",
            round(pixel_per_cm, 4),
            "",
            "Gagal membaca gambar"
        ])

        continue

    # ---------------------------------------------
    # A. PRA-PEMROSESAN
    # ---------------------------------------------

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    # ---------------------------------------------
    # B. SEGMENTASI OTSU
    # ---------------------------------------------

    _, thresh = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # ---------------------------------------------
    # C. MORFOLOGI OPENING
    # ---------------------------------------------

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (3, 3)
    )

    opening = cv2.morphologyEx(
        thresh,
        cv2.MORPH_OPEN,
        kernel,
        iterations=2
    )

    # ---------------------------------------------
    # D. DETEKSI KONTUR
    # ---------------------------------------------

    contours, hierarchy = cv2.findContours(
        opening.copy(),
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if hierarchy is None or len(contours) == 0:

        print("Kontur tidak ditemukan.")

        hasil_pengukuran.append([
            kategori,
            nama_file,
            "",
            round(pixel_per_cm, 4),
            "",
            "Kontur tidak ditemukan"
        ])

        continue

    hierarchy = hierarchy[0]

    # Mengambil kontur luar
    kontur_luar = [
        i for i in range(len(contours))
        if hierarchy[i][3] == -1
    ]

    if len(kontur_luar) == 0:

        print("Kontur luar tidak ditemukan.")

        hasil_pengukuran.append([
            kategori,
            nama_file,
            "",
            round(pixel_per_cm, 4),
            "",
            "Kontur luar tidak ditemukan"
        ])

        continue

    # Memilih kontur luar terbesar
    indeks_daun = max(
        kontur_luar,
        key=lambda i: cv2.contourArea(contours[i])
    )

    area_outer = cv2.contourArea(
        contours[indeks_daun]
    )

    # ---------------------------------------------
    # E. MENGHITUNG LUAS LUBANG DAUN
    # ---------------------------------------------

    area_inner = 0.0

    for i in range(len(contours)):

        if hierarchy[i][3] == indeks_daun:

            area_inner += cv2.contourArea(
                contours[i]
            )

    # Luas aktual = luas luar - luas lubang
    area_pixel = max(
        area_outer - area_inner,
        0
    )

    # ---------------------------------------------
    # F. KONVERSI KE CM PERSEGI
    # ---------------------------------------------

    area_cm2 = area_pixel / (pixel_per_cm ** 2)

    print("Luas kontur luar:", area_outer, "piksel²")
    print("Luas lubang:", area_inner, "piksel²")
    print("Luas daun:", round(area_cm2, 4), "cm²")

    # ---------------------------------------------
    # G. MENYIMPAN HASIL PENGUKURAN
    # ---------------------------------------------

    hasil_pengukuran.append([
        kategori,
        nama_file,
        round(area_pixel, 2),
        round(pixel_per_cm, 4),
        round(area_cm2, 4),
        "Berhasil"
    ])

    # Folder hasil berdasarkan kategori
    folder_hasil_kategori = os.path.join(
        FOLDER_HASIL,
        kategori.upper()
    )

    os.makedirs(
        folder_hasil_kategori,
        exist_ok=True
    )

    nama_dasar = os.path.splitext(nama_file)[0]

    # Menyimpan hasil segmentasi
    cv2.imwrite(
        os.path.join(
            folder_hasil_kategori,
            nama_dasar + "_segmentasi.png"
        ),
        opening
    )

    # Menyimpan hasil kontur
    gambar_kontur = img.copy()

    cv2.drawContours(
        gambar_kontur,
        [contours[indeks_daun]],
        -1,
        (0, 0, 255),
        2
    )

    cv2.imwrite(
        os.path.join(
            folder_hasil_kategori,
            nama_dasar + "_kontur.png"
        ),
        gambar_kontur
    )


# =====================================================
# 7. MENYIMPAN HASIL KE FILE CSV
# =====================================================

path_csv = os.path.join(
    FOLDER_HASIL,
    "hasil_pengukuran_luas_daun.csv"
)

with open(
    path_csv,
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:

    writer = csv.writer(
        file,
        delimiter=";"
    )

    writer.writerow([
        "Kategori",
        "Nama File",
        "Luas Piksel Persegi",
        "Kalibrasi Pixel per CM",
        "Luas Daun CM Persegi",
        "Status"
    ])

    writer.writerows(hasil_pengukuran)


# =====================================================
# 8. RINGKASAN HASIL
# =====================================================

jumlah_berhasil = sum(
    1 for baris in hasil_pengukuran
    if baris[-1] == "Berhasil"
)

jumlah_gagal = len(hasil_pengukuran) - jumlah_berhasil

print("\n========================================")
print("PENGUKURAN LUAS DAUN SELESAI")
print("========================================")

print("Total gambar ditemukan:", len(daftar_gambar))
print("Berhasil diproses:", jumlah_berhasil)
print("Gagal diproses:", jumlah_gagal)
print("Kalibrasi:", round(pixel_per_cm, 4), "pixel/cm")
print("Lokasi hasil:", FOLDER_HASIL)
print("File CSV:", path_csv)

print("========================================")
print("Silakan periksa hasil segmentasi dan kontur.")