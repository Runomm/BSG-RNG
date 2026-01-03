# BSG-RNG: Kamera Tabanlı Gerçek Rastgele Sayı Üreteci (TRNG)

**True Random Number Generator (TRNG) using Camera-Based Physical Entropy**

---

## 📋 Proje Özeti

Bu proje, bilgisayar kamerasından elde edilen fiziksel entropi ile **Collatz Konjektürü** ve **Von Neumann Ekstraktörü** algoritmalarını birleştirerek yüksek kaliteli rastgele sayılar üreten bir **Gerçek Rastgele Sayı Üreteci (TRNG)** sistemidir.

Geleneksel sözde-rastgele sayı üreticilerinin (PRNG) aksine, bu sistem fiziksel dünyadan gelen öngörülemeyen veriyi entropi kaynağı olarak kullanarak kriptografik açıdan daha güvenilir rastgelelik sağlar.

---

## 🔬 Teorik Arka Plan

### 1. Collatz Konjektürü (3n+1 Problemi)
Collatz konjektürü, herhangi bir pozitif tam sayı için uygulanan basit kurallara dayanır:
- **Çift sayı** ise → `n / 2`
- **Tek sayı** ise → `3n + 1`

Bu süreç, başlangıç sayısı ne olursa olsun her zaman 1'e ulaşır (henüz kanıtlanamamış). Algoritma, kaotik bir yörünge oluşturarak sayıları matematiksel olarak "karıştırır".

### 2. Von Neumann Ekstraktörü (Bias Removal)
John von Neumann tarafından 1951'de geliştirilen bu teknik, dengesiz bit akışlarından tarafsız bitler çıkarır:

| Bit Çifti | Çıktı |
|-----------|-------|
| 00        | Atılır |
| 01        | 0 |
| 10        | 1 |
| 11        | Atılır |

Bu yöntem, kaynak ne kadar dengesiz olursa olsun %50-%50 dengeli bit akışı garanti eder.

### 3. Fiziksel Entropi Kaynağı (Kamera)
Kamera sensörleri doğal olarak şu kaynaklardan rastgele gürültü üretir:
- **Termal gürültü** (elektronik devre ısısı)
- **Shot noise** (foton istatistiği)
- **Ortam ışığı değişimleri**

Bu gürültü, SHA-256 hash fonksiyonu ile bir tohum (seed) değerine dönüştürülür.

---

## 📂 Dosya Yapısı

```
BSG-RNG/
├── RNG.py                              # Temel Collatz + Kamera uygulaması
├── RNG(+von neuman extractor).py       # Von Neumann filtreli gelişmiş versiyon
├── RNG(Mini Turing Test).py            # İstatistiksel denge testi
├── RNG(+von neuman extractor)(mini turing test).py  # Tam kapsamlı test
├── JPEG_with_RNG.py                    # JPEG sıkıştırma uygulaması
├── flow-chart.png                      # Sistem akış diyagramı
├── RNG_Rapor.pdf                       # Detaylı proje raporu
├── RNG_Rapor.docx                      # Rapor (Word formatı)
└── *.png                               # Test çıktı görselleri
```

---

## 🚀 Modüller ve Kullanım

### 1. `RNG.py` - Temel TRNG
Kameradan tek bir görüntü alarak rastgele sayı üretir.

```python
# Çalıştırma
python RNG.py

# Çıktı: 1-100 arası rastgele bir sayı
```

**Akış:**
1. Kameradan görüntü yakala
2. SHA-256 ile hash oluştur
3. Hash'i Collatz yörüngesinde 100-500 adım karıştır
4. Sonucu istenilen aralığa normalize et

---

### 2. `RNG(+von neuman extractor).py` - Gelişmiş TRNG
Von Neumann ekstraktörü ile temizlenmiş bit akışı üretir.

```python
# Çalıştırma
python "RNG(+von neuman extractor).py"

# Çıktı: 0-65535 arası (16-bit) rastgele sayı
```

**Özellikler:**
- Sürekli kamera akışından veri toplama
- Bit bazında Von Neumann filtreleme
- Verimlilik raporu (tipik: %25)

---

### 3. `RNG(Mini Turing Test).py` - Denge Testi
Üretilen sayıların istatistiksel dengesini test eder.

```python
# Çalıştırma
python "RNG(Mini Turing Test).py"

# Çıktı: 100 sayı üretip 0/1 ve Tek/Çift denge analizi
```

**Test Kriterleri:**
| Sonuç | Durum |
|-------|-------|
| %49-51 | ✅ Mükemmel |
| %45-55 | ⚠️ Kabul Edilebilir |
| Diğer | ❌ Dengesizlik |

---

### 4. `RNG(+von neuman extractor)(mini turing test).py` - Kapsamlı Test
Von Neumann + Collatz sisteminin tam performans analizi.

```python
# Çalıştırma
python "RNG(+von neuman extractor)(mini turing test).py"

# Çıktı: Detaylı verimlilik ve denge raporu
```

**Rapor İçeriği:**
- Sistem verimliliği (Ham bit → Temiz bit)
- Bit dengesi (0 vs 1 oranı)
- Sayısal denge (Tek vs Çift oranı)

---

### 5. `JPEG_with_RNG.py` - Uygulama: JPEG Sıkıştırma
TRNG'nin pratik bir uygulaması: Rastgele kuantalama tablosu ile JPEG sıkıştırma.

```python
# Çalıştırma
python JPEG_with_RNG.py

# Seçenekler:
# 1. Kameradan anlık fotoğraf
# 2. Dosyadan görüntü yükle
```

**Karşılaştırma:**
- **Standart JPEG Tablosu:** JPEG standardındaki sabit kuantalama matrisi
- **TRNG Tablosu:** Fiziksel entropiden üretilmiş dinamik matris

**Çıktı Metrikleri:**
- **PSNR (Peak Signal-to-Noise Ratio):** Görüntü kalitesi (yüksek = iyi)
- **Veri Boyutu:** Sıkıştırma oranı (düşük = iyi)

---

## 🧪 Sistem Mimarisi

```
┌─────────────────────────────────────────────────────────────────┐
│                        TRNG SİSTEM MİMARİSİ                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│  │  KAMERA  │───▶│ SHA-256  │───▶│ COLLATZ  │───▶│   VON   │  │
│  │  Çekim   │    │  Hash    │    │  Kaos    │    │ NEUMANN  │   │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘   │
│       │              │               │               │          │
│       ▼              ▼               ▼               ▼          │
│   Fiziksel      256-bit          Kaotik          Dengeli        │
│   Entropi       Tohum            Yörünge         Bit Akışı      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Performans Değerleri

| Metrik | Değer |
|--------|-------|
| Von Neumann Verimliliği | ~%25 |
| Bit Dengesi (Hedef) | %50.0 ± 2.0 |
| Collatz Adım Sayısı | 100-500 adım |
| Hash Algoritması | SHA-256 |
| Çıktı Bit Genişliği | 8-bit, 16-bit veya özel |

---

## 📦 Gereksinimler

```bash
pip install opencv-python numpy scipy
```

| Paket | Amaç |
|-------|------|
| `opencv-python` | Kamera erişimi ve görüntü işleme |
| `numpy` | Sayısal hesaplamalar |
| `scipy` | DCT/IDCT (JPEG için) |
| `hashlib` | SHA-256 (Python standart kütüphane) |

---

## ⚙️ Kurulum ve Çalıştırma

```bash
# 1. Depoyu klonla veya indir
git clone <repo-url>
cd BSG-RNG

# 2. Bağımlılıkları yükle
pip install opencv-python numpy scipy

# 3. Temel TRNG'yi çalıştır
python RNG.py

# 4. Tam sistem testini çalıştır
python "RNG(+von neuman extractor)(mini turing test).py"
```

---

## 🔒 Güvenlik Notları

> **⚠️ Dikkat:** Bu proje eğitim ve araştırma amaçlıdır.

- Bu sistem **kavram kanıtı (PoC)** niteliğindedir
- Profesyonel kriptografik uygulamalar için **NIST SP 800-90** gibi standartlara uygun TRNG'ler tercih edilmelidir
- Fiziksel entropi kaynağı olarak kamera, kontrollü ortamlarda manipüle edilebilir

---

## 📚 Referanslar

1. **Collatz Konjektürü:** Lothar Collatz (1937)
2. **Von Neumann Ekstraktörü:** John von Neumann, "Various Techniques Used in Connection With Random Digits" (1951)
3. **JPEG Standardı:** ISO/IEC 10918-1

---
