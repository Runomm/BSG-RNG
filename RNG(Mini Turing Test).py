import cv2
import hashlib
import time


# --- YARDIMCI FONKSİYONLAR ---
def collatz_step(n):
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1


def collatz_process(seed_number):
    """
    Bir sayıyı alır, rastgele sayıda Collatz adımından geçirir
    ve karıştırılmış sayıyı döndürür.
    """
    # Adım sayısı da seed'e bağlı olarak dinamik olsun (100 ile 500 adım arası)
    adim_sayisi = (seed_number % 400) + 100
    current = seed_number

    for _ in range(adim_sayisi):
        current = collatz_step(current)

    return current


# --- TEST FONKSİYONU ---
def collatz_turing_test(ornek_sayisi=100):
    print(f"\n--- HİBRİT SİSTEM (COLLATZ + KAMERA) TEST EDİLİYOR ---")
    print(f"Hedef: {ornek_sayisi} adet 'kaotik sayı' üretmek ve incelemek.")
    print("Kamera 'Seri Çekim' modunda açılıyor (Lütfen bekleyin)...\n")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Hata: Kamera bulunamadı.")
        return

    toplam_sifir = 0
    toplam_bir = 0
    cift_sayi_adedi = 0
    tek_sayi_adedi = 0

    # Kameranın ısınması için bekle
    time.sleep(1)

    baslangic_zamani = time.time()

    for i in range(ornek_sayisi):
        ret, frame = cap.read()
        if not ret: continue

        # 1. FİZİKSEL TOHUM (SEED)
        hash_val = hashlib.sha256(frame.tobytes()).hexdigest()
        seed = int(hash_val, 16)

        # 2. MATEMATİKSEL KAOS (COLLATZ)
        # Seed'i alıp Collatz tüneline sokuyoruz
        final_sayi = collatz_process(seed)

        # 3. ANALİZ
        # Çıkan sayıyı Binary'ye çevirip 0 ve 1'leri sayalım
        binary_str = bin(final_sayi)[2:]
        toplam_sifir += binary_str.count('0')
        toplam_bir += binary_str.count('1')

        # Teklik/Çiftlik dengesine de bakalım
        if final_sayi % 2 == 0:
            cift_sayi_adedi += 1
        else:
            tek_sayi_adedi += 1

        # İlerleme göstergesi
        if i % 10 == 0:
            print(f"İşleniyor... (%{int((i / ornek_sayisi) * 100)})")

    cap.release()
    gecen_sure = time.time() - baslangic_zamani
    print(f"\nTest Tamamlandı! ({gecen_sure:.2f} saniye sürdü)\n")

    # --- RAPORLAMA ---
    toplam_bit = toplam_sifir + toplam_bir
    yuzde_sifir = (toplam_sifir / toplam_bit) * 100
    yuzde_bir = (toplam_bir / toplam_bit) * 100

    print("=" * 40)
    print("İSTATİSTİKSEL DENGE RAPORU")
    print("=" * 40)
    print(f"BIT DENGESİ (0 vs 1):")
    print(f"  - 0 Oranı: %{yuzde_sifir:.2f}")
    print(f"  - 1 Oranı: %{yuzde_bir:.2f}")
    print("-" * 40)
    print(f"SAYI DENGESİ (Tek vs Çift):")
    print(f"  - Çift Sayılar: {cift_sayi_adedi} adet")
    print(f"  - Tek Sayılar : {tek_sayi_adedi} adet")
    print("=" * 40)

    # --- YORUM ---
    print("\nSONUÇ DEĞERLENDİRMESİ:")
    if 49.0 < yuzde_bir < 51.0:
        print("✅ MÜKEMMEL: Collatz algoritması hash'in dengesini bozmamış.")
        print("   Sayılar hem kaotik hem de istatistiksel olarak dengeli.")
    elif 45.0 < yuzde_bir < 55.0:
        print("⚠️ KABUL EDİLEBİLİR: Hafif bir sapma var.")
        print("   Collatz yapısı gereği (3x+1) bazen belirli bit desenlerini öne çıkarabilir.")
    else:
        print("❌ DENGESİZLİK SAPTANDI: Oranlar %50'den çok uzak.")
        print("   Collatz adımları entropiyi azaltıyor olabilir.")


if __name__ == "__main__":
    collatz_turing_test(100)  # 100 Örnek ile test et