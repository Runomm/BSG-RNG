import cv2
import numpy as np
import scipy.fftpack
import hashlib
import time
import os


# --- 1. TRNG MOTORU (Rastgelelik Kaynağı) ---
def von_neumann_temizle(bit_dizisi):
    temiz_bitler = ""
    for i in range(0, len(bit_dizisi) - 1, 2):
        cift = bit_dizisi[i: i + 2]
        if cift == "01":
            temiz_bitler += "0"
        elif cift == "10":
            temiz_bitler += "1"
    return temiz_bitler


def collatz_adimi(n):
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1


def trng_tablo_uretici():
    print("\n[SİSTEM] TRNG Kuantalama Tablosu için fiziksel entropi toplanıyor (Kamera)...")
    tablo_degerleri = []

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("HATA: Kamera bulunamadı, varsayılan tablo kullanılıyor.")
        return np.ones((8, 8)) * 50

    ret, frame = cap.read()
    cap.release()

    if not ret: return np.ones((8, 8)) * 50

    seed = int(hashlib.sha256(frame.tobytes()).hexdigest(), 16)
    curr = seed

    while len(tablo_degerleri) < 64:
        ham_bitler = ""
        for _ in range(50):
            curr = collatz_adimi(curr)
            ham_bitler += "1" if curr % 2 != 0 else "0"

        temiz_bitler = von_neumann_temizle(ham_bitler)

        if len(temiz_bitler) >= 8:
            sayi = int(temiz_bitler[:8], 2)
            # 1-100 arası normalizasyon
            normalize_deger = (sayi % 99) + 1
            tablo_degerleri.append(normalize_deger)

    return np.array(tablo_degerleri[:64]).reshape(8, 8)


# --- 2. JPEG SİMÜLASYON MOTORU ---

standart_tablo = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
])


def dct2(a):
    return scipy.fftpack.dct(scipy.fftpack.dct(a, axis=0, norm='ortho'), axis=1, norm='ortho')


def idct2(a):
    return scipy.fftpack.idct(scipy.fftpack.idct(a, axis=0, norm='ortho'), axis=1, norm='ortho')


def jpeg_simule_et(goruntu, kuantalama_tablosu):
    h, w = goruntu.shape
    h = (h // 8) * 8
    w = (w // 8) * 8
    img = goruntu[:h, :w].astype(float)

    sikistirilmis_img = np.zeros_like(img)
    sifir_olmayan_katsayi = 0

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            blok = img[i:i + 8, j:j + 8]

            dct_blok = dct2(blok - 128)
            kuante_blok = np.round(dct_blok / kuantalama_tablosu)
            sifir_olmayan_katsayi += np.count_nonzero(kuante_blok)

            dekuante_blok = kuante_blok * kuantalama_tablosu
            ters_dct_blok = idct2(dekuante_blok) + 128

            sikistirilmis_img[i:i + 8, j:j + 8] = ters_dct_blok

    sikistirilmis_img = np.clip(sikistirilmis_img, 0, 255)
    return sikistirilmis_img, sifir_olmayan_katsayi


def psnr_hesapla(orijinal, islenmis):
    mse = np.mean((orijinal - islenmis) ** 2)
    if mse == 0: return 100
    max_pixel = 255.0
    return 20 * np.log10(max_pixel / np.sqrt(mse))


# --- GÖRÜNTÜ KAYNAĞI SEÇİMİ ---
def goruntu_kaynagi_al():
    print("\n" + "=" * 40)
    print("GÖRÜNTÜ KAYNAĞI SEÇİNİZ")
    print("=" * 40)
    print("1. Kameradan anlık fotoğraf çek")
    print("2. Bilgisayardan dosya yolu (Path) gir")

    secim = input("Seçiminiz (1 veya 2): ")
    img_gray = None

    if secim == '1':
        print("Kamera başlatılıyor...")
        cap = cv2.VideoCapture(0)
        time.sleep(1)
        ret, frame = cap.read()
        cap.release()
        if ret:
            img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            print("Hata: Görüntü alınamadı.")

    elif secim == '2':
        dosya_yolu = input("\nLütfen dosya yolunu yapıştırın: ")
        dosya_yolu = dosya_yolu.strip('"').strip("'").strip()

        if os.path.exists(dosya_yolu):
            print(f"Dosya okunuyor: {dosya_yolu}")
            try:
                # Türkçe karakter sorunu için numpy ile okuma
                with open(dosya_yolu, "rb") as f:
                    bytes_data = bytearray(f.read())
                    numpy_array = np.asarray(bytes_data, dtype=np.uint8)
                    img = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)

                if img is not None:
                    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    h, w = img_gray.shape
                    if w > 1024:
                        scale = 1024 / w
                        img_gray = cv2.resize(img_gray, (0, 0), fx=scale, fy=scale)
                else:
                    print("Hata: Dosya formatı bozuk veya resim değil.")
            except Exception as e:
                print(f"Okuma hatası: {e}")
        else:
            print("Hata: Belirtilen yolda dosya bulunamadı.")

    return img_gray


# --- 3. ANA TEST ---
if __name__ == "__main__":

    test_resmi = goruntu_kaynagi_al()

    if test_resmi is not None:

        # A) Standart Tablo
        print("\n--- STANDART JPEG TABLOSU UYGULANIYOR ---")
        img_std, boyut_std = jpeg_simule_et(test_resmi, standart_tablo)
        psnr_std = psnr_hesapla(test_resmi[:img_std.shape[0], :img_std.shape[1]], img_std)

        # AÇIKLAMALI ÇIKTILAR
        print(f"-> Kalite (PSNR): {psnr_std:.2f} dB  (Yüksek değer = Daha İyi Görüntü Kalitesi)")
        print(f"-> Veri Boyutu  : {boyut_std}       (Düşük değer = Daha İyi Sıkıştırma/Daha Küçük Dosya)")

        # B) TRNG Tablo
        print("\n--- TRNG (FİZİKSEL KAOS) TABLOSU UYGULANIYOR ---")
        trng_tablo = trng_tablo_uretici()
        print("-> Üretilen Tablo (İlk satır):", trng_tablo[0])

        img_trng, boyut_trng = jpeg_simule_et(test_resmi, trng_tablo)
        psnr_trng = psnr_hesapla(test_resmi[:img_trng.shape[0], :img_trng.shape[1]], img_trng)

        # AÇIKLAMALI ÇIKTILAR
        print(f"-> Kalite (PSNR): {psnr_trng:.2f} dB  (Yüksek değer = Daha İyi Görüntü Kalitesi)")
        print(f"-> Veri Boyutu  : {boyut_trng}       (Düşük değer = Daha İyi Sıkıştırma/Daha Küçük Dosya)")

        # --- Görselleştirme ---
        cv2.imshow("1. Orjinal", test_resmi)
        cv2.imshow(f"2. Standart JPEG (PSNR: {psnr_std:.1f} dB)", img_std.astype('uint8'))
        cv2.imshow(f"3. TRNG JPEG (PSNR: {psnr_trng:.1f} dB)", img_trng.astype('uint8'))

        print("\nSonuçları görmek için pencerelere bakın.")
        print("Çıkmak için HERHANGİ BİR RESİM PENCERESİNDE bir tuşa basın.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Program sonlandırıldı.")