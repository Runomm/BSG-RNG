import cv2
import hashlib
import time


def collatz_step(n):
    """
    Collatz kuralının tek bir adımı.
    Çift ise yarısı, Tek ise 3 katının 1 fazlası.
    """
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1


def collatz_chaos_generator(min_deger=1, max_deger=100):
    print("Kamera başlatılıyor (Collatz Modu)...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Hata: Kamera açılamadı.")
        return None

    time.sleep(0.5)  # Işık ayarı için bekle
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Görüntü alınamadı.")
        return None

    # --- 1. GÖRÜNTÜYÜ GÖSTER ---
    print("Görüntü ekranda. Devam etmek için resim penceresinde bir tuşa basın.")
    cv2.imshow("Collatz Entropi Kaynagi", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # --- 2. FİZİKSEL TOHUMU (SEED) OLUŞTUR ---
    # Görüntüyü SHA-256 ile özetle
    frame_bytes = frame.tobytes()
    hash_object = hashlib.sha256(frame_bytes)
    hex_dig = hash_object.hexdigest()

    # Bu devasa sayıyı başlangıç noktamız (n) olarak alıyoruz
    baslangic_sayisi = int(hex_dig, 16)

    # --- 3. ADIM SAYISINI BELİRLE ---
    # Collatz algoritmasını kaç adım çalıştıracağız?
    # Bunu da görüntünün hash'inden türetelim ki her seferinde farklı olsun.
    # Örn: Hash'in son 4 hanesini alıp 100 ekleyelim (en az 100 adım dönsün)
    adim_sayisi = (baslangic_sayisi % 1000) + 100

    print(f"\n--- HESAPLAMA BAŞLIYOR ---")
    print(f"Başlangıç Sayısı (Seed): ...{str(baslangic_sayisi)[-10:]} (Devasa bir sayı)")
    print(f"Collatz Adım Sayısı: {adim_sayisi}")

    # --- 4. COLLATZ TÜNELİ (MATEMATİKSEL KAOS) ---
    mevcut_sayi = baslangic_sayisi

    for i in range(adim_sayisi):
        mevcut_sayi = collatz_step(mevcut_sayi)

        # Sadece görselleştirmek için ilk 5 ve son 5 adımı yazdıralım
        if i < 3 or i > adim_sayisi - 3:
            print(f"Adım {i + 1}: {mevcut_sayi} (İşleniyor...)")
        elif i == 3:
            print("... (Matematiksel karıştırma devam ediyor) ...")

    # --- 5. SONUÇ İNDİRGEME ---
    # Collatz sürecinden çıkan son sayıyı istediğimiz aralığa (min-max) sığdırıyoruz
    aralik = max_deger - min_deger + 1
    final_rastgele_sayi = (mevcut_sayi % aralik) + min_deger

    return final_rastgele_sayi


# --- ÇALIŞTIRMA ---
if __name__ == "__main__":
    sayi = collatz_chaos_generator(1, 100)

    if sayi:
        print("\n" + "#" * 50)
        print(f"COLLATZ + KAMERA İLE ÜRETİLEN SAYI: {sayi}")
        print("#" * 50)