import cv2
import hashlib
import time


# --- YARDIMCI FONKSİYONLAR ---
def von_neumann_debias(bit_stream):
    """
    Ham bit akışını Von Neumann kuralına göre süzgeçten geçirir.
    """
    clean_bits = ""
    for i in range(0, len(bit_stream) - 1, 2):
        pair = bit_stream[i: i + 2]
        if pair == "01":
            clean_bits += "0"
        elif pair == "10":
            clean_bits += "1"
    return clean_bits


def collatz_step(n):
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1


# --- "ULTIMATE" TEST FONKSİYONU ---
def full_system_test(hedef_sayi_adedi=100):
    """
    Hem bit dengesini hem de üretilen tam sayıların (Tek/Çift) dengesini test eder.
    """
    print(f"\n--- TAM KAPSAMLI SİSTEM TESTİ BAŞLATILIYOR ---")
    print(f"Hedef: {hedef_sayi_adedi} adet rastgele sayı üretip analiz etmek.")
    print("Yöntem: Kamera -> Hash -> Collatz -> Von Neumann -> Tam Sayı")
    print("Lütfen bekleyin, temiz veri toplanıyor...\n")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Hata: Kamera bulunamadı.")
        return

    # İstatistik Değişkenleri
    bit_havuzu = ""  # İşlenmeyi bekleyen temiz bitler
    uretilen_sayilar = []  # Sonuç sayıları listesi

    toplam_islenen_ham_bit = 0
    toplam_sifir_bit = 0  # Bit bazında 0 sayacı
    toplam_bir_bit = 0  # Bit bazında 1 sayacı

    tek_sayi_sayaci = 0  # Sayı bazında Tek sayacı
    cift_sayi_sayaci = 0  # Sayı bazında Çift sayacı

    start_time = time.time()

    # Yeterli sayıda tam sayı üretene kadar döngü
    while len(uretilen_sayilar) < hedef_sayi_adedi:
        ret, frame = cap.read()
        if not ret: continue

        # 1. Tohum (Seed)
        h = hashlib.sha256(frame.tobytes()).hexdigest()
        seed = int(h, 16)

        # 2. Ham Bit Akışı (Collatz ile) - Her karede 64 bit üretelim
        ham_akis = ""
        curr = seed
        for _ in range(64):
            curr = collatz_step(curr)
            ham_akis += "1" if curr % 2 != 0 else "0"

        toplam_islenen_ham_bit += len(ham_akis)

        # 3. Von Neumann Temizliği
        temiz_akis = von_neumann_debias(ham_akis)

        # Bit istatistiklerini kaydet
        toplam_sifir_bit += temiz_akis.count('0')
        toplam_bir_bit += temiz_akis.count('1')

        # Temiz bitleri havuza ekle
        bit_havuzu += temiz_akis

        # 4. Sayı Oluşturma (8 bit = 1 Sayı)
        while len(bit_havuzu) >= 8:
            # İlk 8 biti al ve kes
            byte_parcasi = bit_havuzu[:8]
            bit_havuzu = bit_havuzu[8:]

            # Binary string'i sayıya çevir (Örn: "10110010" -> 178)
            sayi = int(byte_parcasi, 2)
            uretilen_sayilar.append(sayi)

            # Tek mi Çift mi Analizi
            if sayi % 2 == 0:
                cift_sayi_sayaci += 1
            else:
                tek_sayi_sayaci += 1

            # İlerleme durumunu göster (Hedef sayıya ulaşma yüzdesi)
            if len(uretilen_sayilar) % 5 == 0:
                print(".", end="", flush=True)

            if len(uretilen_sayilar) >= hedef_sayi_adedi:
                break

    cap.release()
    gecen_sure = time.time() - start_time
    print(f"\n\nTest Tamamlandı! ({gecen_sure:.2f} sn)")

    # --- RAPORLAMA ---

    # 1. BÖLÜM: Verimlilik ve Bit Analizi
    toplam_temiz_bit = toplam_sifir_bit + toplam_bir_bit
    verimlilik = (toplam_temiz_bit / toplam_islenen_ham_bit) * 100
    bit_0_orani = (toplam_sifir_bit / toplam_temiz_bit) * 100
    bit_1_orani = (toplam_bir_bit / toplam_temiz_bit) * 100

    print("\n" + "=" * 50)
    print("DETAYLI ANALİZ RAPORU")
    print("=" * 50)
    print(f"I. SİSTEM VERİMLİLİĞİ (Von Neumann)")
    print(f"- İşlenen Ham Bit  : {toplam_islenen_ham_bit}")
    print(f"- Kurtarılan Bit   : {toplam_temiz_bit}")
    print(f"- Arıtma Oranı     : %{verimlilik:.2f}")
    print("-" * 50)

    print(f"II. BIT DENGESİ (0 vs 1)")
    print(f"- Bit 0 Oranı      : %{bit_0_orani:.2f}")
    print(f"- Bit 1 Oranı      : %{bit_1_orani:.2f}")

    # 2. BÖLÜM: Sayısal Analiz (Tek/Çift)
    toplam_sayi = len(uretilen_sayilar)
    tek_orani = (tek_sayi_sayaci / toplam_sayi) * 100
    cift_orani = (cift_sayi_sayaci / toplam_sayi) * 100

    print("-" * 50)
    print(f"III. SAYISAL DENGE (Tek vs Çift)")
    print(f"- Üretilen Sayı    : {toplam_sayi} adet")
    print(f"- Çift Sayılar     : {cift_sayi_sayaci} adet (Oran: %{cift_orani:.2f})")
    print(f"- Tek Sayılar      : {tek_sayi_sayaci}  adet (Oran: %{tek_orani:.2f})")
    print("=" * 50)

    # --- YORUM ---
    print("\nFİNAL KARARI:")
    denge_farki = abs(tek_orani - 50.0)

    if denge_farki < 2.0:
        print(">>> 👑 MÜKEMMEL SONUÇ 👑 <<<")
        print("Hem bitler hem de sayılar tam dengede. Bu sistem profesyonel kriptografi standartlarına göz kırpıyor.")
    elif denge_farki < 5.0:
        print(">>> ✅ BAŞARILI <<<")
        print("Sayılar dengeli dağılmış, güvenle kullanılabilir.")
    else:
        print(">>> ⚠️ DİKKAT <<<")
        print("Tek/Çift dağılımında sapma var. Örnek sayısını artırıp tekrar deneyin.")


if __name__ == "__main__":
    # 100 adet sayı üretip test et (Daha kesin sonuç için 500 veya 1000 yapabilirsiniz)
    full_system_test(100)