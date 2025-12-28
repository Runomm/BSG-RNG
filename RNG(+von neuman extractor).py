import cv2
import hashlib
import time


def von_neumann_debias(bit_stream):
    """
    Gelen bit dizisini (string) Von Neumann kuralına göre temizler.
    Geriye temizlenmiş bit dizisini döndürür.
    """
    clean_bits = ""
    # Bitleri ikişer ikişer al (0,1), (2,3), ...
    for i in range(0, len(bit_stream) - 1, 2):
        pair = bit_stream[i: i + 2]

        if pair == "01":
            clean_bits += "0"
        elif pair == "10":
            clean_bits += "1"
        # "00" ve "11" durumlarında hiçbir şey yapma (Discard/At)

    return clean_bits


def collatz_step(n):
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1


def vn_collatz_generator(bit_uzunlugu=8):
    """
    Belirtilen bit uzunluğunda (örn: 8 bit = 0-255 arası) sayı üretir.
    Von Neumann filtresi uygulandığı için işlem garantilidir.
    """
    print(f"Veri toplanıyor (Hedef: {bit_uzunlugu} temiz bit)...")

    cap = cv2.VideoCapture(0)
    temiz_bit_havuzu = ""
    toplam_islenen_bit = 0

    # Kamerayı bir kez başlat, döngü içinde sürekli aç-kapa yapmayalım (Hız için)
    if not cap.isOpened():
        return None

    while len(temiz_bit_havuzu) < bit_uzunlugu:
        ret, frame = cap.read()
        if not ret: continue

        # 1. Kameradan Seed (Tohum) Al
        h = hashlib.sha256(frame.tobytes()).hexdigest()
        seed = int(h, 16)

        # 2. Collatz Yörüngesinden Ham Bit Üret
        # Seed'i 100 adım boyunca Collatz'da yürütelim
        ham_bitler = ""
        current = seed
        for _ in range(100):  # Her karede 100 adım
            current = collatz_step(current)
            # Sayı Tek ise '1', Çift ise '0'
            ham_bitler += "1" if current % 2 != 0 else "0"

        toplam_islenen_bit += len(ham_bitler)

        # 3. VON NEUMANN FILTRESI (Büyü burada gerçekleşiyor)
        yeni_temizler = von_neumann_debias(ham_bitler)
        temiz_bit_havuzu += yeni_temizler

        # Kullanıcıya çalıştığını göster (nokta koy)
        print(".", end="", flush=True)

    cap.release()
    print("\n")

    # İstenilen uzunlukta kes (Fazlasını at)
    final_bits = temiz_bit_havuzu[:bit_uzunlugu]

    # Verimlilik Raporu
    verimlilik = (len(temiz_bit_havuzu) / toplam_islenen_bit) * 100
    print(f"İşlenen Ham Bit: {toplam_islenen_bit}")
    print(f"Kazanılan Saf Bit: {len(temiz_bit_havuzu)}")
    print(f"Von Neumann Verimliliği: %{verimlilik:.1f} (Normalde %25 civarıdır)")

    # Binary'den Integer'a çevir
    sonuc_sayi = int(final_bits, 2)
    return sonuc_sayi


# --- KULLANIM ---
if __name__ == "__main__":
    # 8 bitlik bir sayı üret (0 - 255 arası)
    # Daha büyük sayılar için bit_uzunlugu değerini artırın (örn: 16, 32)
    sayi = vn_collatz_generator(bit_uzunlugu=16)

    if sayi is not None:
        print("\n" + "=" * 40)
        print(f"VON NEUMANN ARITILMIŞ SAYI: {sayi}")
        print("=" * 40)