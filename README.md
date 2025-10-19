# Akıllı Tahta Kilit Programı

![Vertus OS](https://img.shields.io/badge/Vertus%20OS-Smart%20Lock-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI%20Framework-orange)
![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-red)

## ꩜ İçindekiler

- [Proje Hakkında](#-proje-hakkında)
- [Özellikler](#-özellikler)
- [Sistem Gereksinimleri](#-sistem-gereksinimleri)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Güvenlik Sistemi](#-güvenlik-sistemi)
- [Geliştirici Özellikleri](#-geliştirici-özellikleri)
- [Uygulama Yapısı](#-uygulama-yapısı)
- [Sıkça Sorulan Sorular](#-sıkça-sorulan-sorular)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)
- [İletişim](#-iletişim)

## ꩜ Proje Hakkında

**Vertus OS - Akıllı Tahta Kilidi**, okul ve eğitim kurumlarındaki akıllı tahtaların güvenli kullanımını sağlamak amacıyla geliştirilmiş tam ekran kilitleme uygulamasıdır. Öğretmenlerin ders süreçlerini kontrol altına almasını ve öğrencilerin tahtayı yetkisiz kullanımını engellemeyi hedefler.

### ꩜ Amaç
- Akıllı tahtaların ders dışı kullanımını engellemek
- Zaman tabanlı güvenlik sistemi ile kontrollü erişim sağlamak
- Eğitimci dostu arayüz sunmak
- Otomatik ders programı entegrasyonu ile akıllı kilitleme

## ꩜ Özellikler

### ꩜ Güvenlik Özellikleri
- **Zaman Tabanlı Şifre Sistemi**: Dakikada bir değişen 6 haneli güvenlik kodu
- **Tam Ekran Kilitleme**: Tüm sistemi bloke eden fullscreen arayüz
- **Kısayol Engelleme**: Alt+Tab, Win+D, Ctrl+Alt+Del gibi kısayolların engellenmesi
- **Otomatik Kilitleme**: Teneffüs ve öğle aralarında otomatik kilitlenme

### ꩜ Arayüz Özellikleri
- **Modern Glassmorphism Tasarım**: Şeffaf ve modern arayüz
- **Responsive Tasarım**: Farklı ekran boyutlarına uyum
- **Gerçek Zamanlı Takip**: Sistem kaynakları izleme (CPU, RAM)
- **Animasyonlu Butonlar**: Kullanıcı etkileşimli animasyonlar

### ꩜ Entegre Uygulamalar
- **Microsoft Copilot**: Yapay zeka asistanı
- **Office 365**: Online ofis uygulamaları
- **Hesap Makinesi**: Gelişmiş hesap makinesi
- **EBA**: Eğitim Bilişim Ağı

### ꩜ Sistem Özellikleri
- **Ders Programı Entegrasyonu**: Otomatik ders zamanlama
- **Geliştirici Terminali**: Sistem yönetimi için gelişmiş terminal
- **Çoklu Pencere Yönetimi**: Uygulama pencereleri yönetimi
- **Bildirim Sistemi**: Kullanıcı bildirimleri

## ꩜ Sistem Gereksinimleri

### Minimum Gereksinimler
- **İşletim Sistemi**: Windows 10/11, Ubuntu 20.04+, Pardus 21+
- **Python**: 3.8 veya üzeri
- **RAM**: 4 GB
- **Depolama**: 100 MB boş alan
- **Ekran Çözünürlüğü**: 1024x768

### Önerilen Gereksinimler
- **İşletim Sistemi**: Windows 11, Ubuntu 22.04 LTS
- **Python**: 3.10+
- **RAM**: 8 GB veya üzeri
- **İnternet**: Uygulamalar için internet bağlantısı

## ꩜ Kurulum

### 1. Gerekli Paketlerin Kurulumu

#### Windows
```bash
# Python'u resmi sitesinden indirin ve kurun
# https://python.org

# Gerekli kütüphaneleri kurun
pip install PyQt6 PyQt6-WebEngine psutil
```

#### Ubuntu/Debian
```bash
# Sistem paketlerini güncelle
sudo apt update

# Gerekli paketleri kur
sudo apt install python3 python3-pip python3-pyqt6 python3-pyqt6.qtwebengine python3-psutil

# Pip ile ek kütüphaneler
pip3 install psutil
```

#### Pardus
```bash
# Pardus paket yöneticisi
sudo apt update
sudo apt install python3 python3-pip python3-pyqt6 python3-pyqt6.qtwebengine python3-psutil
```

### 2. Proje Dosyalarını Hazırlama

1. Proje dosyalarını bir klasöre kopyalayın:
```
vertus_os/
├── main.py
├── wallpaper.png
├── wallpaper2.png
├── logo.png
├── dev.png
├── kapa.png
├── ai.png
├── 360.png
├── hesapmakinesi.png
└── eba.png
```

2. Gerekli ikon dosyalarını temin edin veya varsayılan ikonları kullanın.

### 3. Uygulamayı Başlatma

```bash
# Windows
python main.py

# Linux
python3 main.py
```

## 🎮 Kullanım

### Temel Kullanım

1. **Uygulamayı Başlatın**: Program başladığında tam ekran kilitleme modunda açılır.

2. **Güvenlik Kodunu Alın**:
   - Telefon uygulamasından veya zaman tabanlı kod üreticiden gerçek kodu alın
   - Ekranda görünen "sahte" kodu DEĞİL, gerçek kodu girin

3. **Kilidi Açın**:
   - 6 haneli gerçek kodu girin
   - Kilidin açık kalma süresini seçin (1 Ders veya Sınırsız)
   - "KİLİDİ AÇ" butonuna tıklayın

### Kontrol Paneli

#### Sol Panel
- **Güvenlik Kodu**: Zamanla değişen görüntü kodu
- **Sayac**: Kodun ne zaman değişeceğini gösterir
- **Giriş Paneli**: Şifre girişi ve tuş takımı

#### Orta Panel
- **Sistem Bilgileri**: Vertus OS logosu ve versiyon bilgisi
- **Geliştirici Bilgisi**: Proje geliştiricisi

#### Sağ Panel
- **Ders Programı**: Mevcut ders ve kalan süre
- **Uygulamalar**: Hızlı erişim uygulama butonları
- **Sistem İzleme**: CPU ve RAM kullanımı

### Alt Sağ Köşe Kontrolleri

- **Saat ve Tarih**: Gerçek zamanlı saat ve takvim
- **Geliştirici Butonu** (🔧): Geliştirici terminalini açar
- **Kapat Butonu** (⏻): Bilgisayarı kapatır

## ꩜ Güvenlik Sistemi

### Kod Üretim Mekanizması

```python
# Zaman tabanlı kod üretimi
current_time = int(time.time() / 60)  # Dakika bazında
raw_code = f"{secret_key}{current_time}"
hash_code = hashlib.md5(raw_code.encode()).hexdigest()

# Görüntü kodu (ekranda gösterilen)
fake_code = numeric_hash[:6]

# Gerçek kod (girilmesi gereken)
real_code = ""
for char in fake_code:
    digit = int(char)
    real_digit = (10 - digit) % 10
    real_code += str(real_digit)
```

### Doğrulama Süreci

1. **Görüntü Kodu**: Ekranda her dakika değişen 6 haneli kod
2. **Gerçek Kod**: Görüntü kodundan matematiksel olarak türetilen kod
3. **Doğrulama**: Girilen kodun geçerlilik kontrolü

### Otomatik Kilitleme

- **Teneffüslerde**: Otomatik kilitlenme
- **Öğle Arasında**: Otomatik kilitlenme  
- **Ders Başlangıcı**: Otomatik kontrol

## ꩜ Geliştirici Özellikleri

### Geliştirici Terminali

Terminali açmak için sağ alt köşedeki **>_** butonuna tıklayın.

#### Terminal Komutları

##### Temel Komutlar
```bash
root          # Geliştirici girişi
help veya ?   # Yardım menüsü
clear veya cls # Ekranı temizle
exit          # Terminalden çık
```

##### Geliştirici Komutları (Giriş yapıldıktan sonra)
```bash
sysinfo       # Sistem bilgileri
version       # Versiyon bilgisi
status        # Sistem durumu
debug         # Hata ayıklama bilgileri
browser       # Tarayıcı uygulamasını aç
shutdown      # Programı kapat
```

#### Geliştirici Giriş Bilgileri
- **Kullanıcı Adı**: `developer`
- **Şifre**: `fAd473dC5BbCc+`

### Uygulama Geliştirme

#### Yeni Uygulama Ekleme

1. **Uygulama ikonunu ekleyin**: `app_icon.png`
2. **Ana uygulama listesini güncelleyin**:

```python
apps = [
    ("ai.png", "Copilot", "https://yigtii.github.io/copilot/", "vertical", 0, 0),
    ("360.png", "Microsoft Office 365", "https://yigtii.github.io/360/", "horizontal", 0, 1),
    ("hesapmakinesi.png", "Vertus Hesap Makinesi", "https://yigtii.github.io/hesap-makinesi/", "vertical", 1, 0),
    ("eba.png", "Eba", "https://yigtii.github.io/eba/", "horizontal", 1, 1),
    # Yeni uygulama ekle
    ("yeni_icon.png", "Yeni Uygulama", "https://ornek.com", "horizontal", 2, 0)
]
```

#### Özel Uygulama Penceresi

```python
def open_custom_app(self):
    app_window = AppWindow("Özel Uygulama", "https://ornek.com", "horizontal", self)
    app_window.show()
```

## ꩜ Uygulama Yapısı

### Ana Sınıflar

#### `SmartBoardLock`
Ana uygulama sınıfı, tüm sistemi yönetir.

#### `TimeBasedCrypto`
Zaman tabanlı şifreleme sistemi.

#### `DeveloperTerminal`
Geliştirici terminali ve sistem yönetimi.

#### `AppWindow`
Web uygulamaları için pencere yönetimi.

#### `NotificationWidget`
Bildirim sistemi.

### Dosya Yapısı

```
vertus_os/
├── main.py                 # Ana uygulama dosyası
├── wallpaper.png           # Varsayılan duvar kağıdı
├── wallpaper2.png          # Geliştirici duvar kağıdı
├── logo.png               # Vertus OS logosu
├── dev.png                # Geliştirici buton ikonu
├── kapa.png               # Kapat buton ikonu
├── ai.png                 # Copilot ikonu
├── 360.png                # Office 365 ikonu
├── hesapmakinesi.png      # Hesap makinesi ikonu
└── eba.png                # EBA ikonu
```

### Önemli Metodlar

#### Kilitleme/Açma
```python
def lock_device(self)       # Cihazı kilitle
def check_code(self)        # Kodu doğrula
def unlock_device(self)     # Cihazın kilidini aç
```

#### Zaman Yönetimi
```python
def get_current_period(self)    # Mevcut dersi al
def update_schedule_info(self)  # Program bilgisini güncelle
def update_display_code(self)   # Güvenlik kodunu güncelle
```

## ꩜ Sıkça Sorulan Sorular

### S: Uygulama başlamıyor, ne yapmalıyım?
**C**: Python ve gerekli kütüphanelerin kurulu olduğundan emin olun. Konsolda `python --version` komutu ile kontrol edin.

### S: Güvenlik kodu çalışmıyor, neden?
**C**: 
- Sistem saatinin doğru olduğundan emin olun
- Gerçek kodu girdiğinizden emin olun (görüntü kodu değil)
- Kodu 60 saniye içinde girin

### S: Uygulama pencereleri açılmıyor?
**C**: 
- İnternet bağlantınızı kontrol edin
- WebEngine eklentisinin kurulu olduğundan emin olun
- Güvenlik duvarı ayarlarını kontrol edin

### S: Otomatik kilitleme çalışmıyor?
**C**: 
- Sistem saatinin doğru olduğundan emin olun
- Ders programının güncel olduğunu kontrol edin
- Uygulamanın arka planda çalıştığından emin olun

### S: Geliştirici terminaline nasıl giriş yapabilirim?
**C**: 
- Terminali açın
- `root` yazın
- Kullanıcı adı: `developer`
- Şifre: `fAd473dC5BbCc+`

## ꩜ Katkıda Bulunma

Vertus OS projesine katkıda bulunmak isterseniz:

1. Bu depoyu fork edin
2. Yeni özellik ekleyin veya hata düzeltin
3. Pull request gönderin

### Katkıda Bulunma Kuralları
- Kod standartlarına uyun
- Yeni özellikler için testler ekleyin
- Dokümantasyonu güncelleyin

## ꩜ Lisans

Bu proje **telif hakkıyla korunmaktadır**. Tüm hakları saklıdır.

**© 2024 Yiğit Eritici. Tüm hakları saklıdır.**

Bu yazılım, sahibinin açık izni olmadan kopyalanamaz, dağıtılamaz, değiştirilemez veya ticari amaçlarla kullanılamaz.

## ꩜ İletişim

**Vertus OS** projesi hakkında bilgi almak, okulunuzda kullanmak veya işbirliği yapmak için:

**E-posta**: vetrabilgisayar@gmail.com

**Okul Entegrasyonu**: Eğer okulunuzda Vertus OS'u kullanmak istiyorsanız veya özelleştirilmiş bir versiyon talep etmek istiyorsanız yukarıdaki e-posta adresi ile iletişime geçebilirsiniz.

---

**Not**: Bu uygulama eğitim kurumlarında akıllı tahta güvenliği için geliştirilmiştir. Lisans ve kullanım hakları için geliştirici ile iletişime geçin.

**Vertus OS - Eğitimin Güvenli Geleceği** 
