<h1 align="center">
  <br>
  <img src="https://img.icons8.com/color/144/000000/radar.png" alt="Port Scanner Logo" width="100">
  <br>
  Professional Port Scanner
  <br>
</h1>

<h4 align="center">Hızlı, çoklu iş parçacıklı (multithreaded) ve asenkron Python Port Tarayıcı.</h4>

<p align="center">
  <img src="https://img.shields.io/badge/Lisans-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/Python-3.x-yellow" alt="Python Version">
</p>

<p align="center">
  <a href="#proje-hakkında">Proje Hakkında</a> •
  <a href="#özellikler">Özellikler</a> •
  <a href="#kurulum">Kurulum</a> •
  <a href="#kullanım">Kullanım</a> •
  <a href="#lisans">Lisans</a>
</p>

---

## 📋 Proje Hakkında

Bu araç, siber güvenlik uzmanları, sistem yöneticileri ve ağ meraklıları için hedef sistemlerdeki açık portları tespit etmeyi ve çalışan servislerin bilgisini almayı (banner grabbing) kolaylaştırmak amacıyla geliştirilmiştir.

Python ile yazılan **Professional Port Scanner**, çoklu iş parçacığı (threading) yapısı sayesinde standart tarayıcılara kıyasla çok daha hızlı sonuç üretir. İster tek bir IP adresi, port, ister geniş çaplı taramalar yapın; araç hem komut satırı esnekliği hem de detaylı JSON çıktı imkanı sunar.

## 🌟 Özellikler

- **Çoklu Hedef (Multi-target):** Tek bir IP (örn. `192.168.1.1`) veya virgülle ayrılmış birden çok hedefi aynı anda tarayabilirsiniz.
- **Geniş Port Aralığı:** `80`, `1-1000` gibi esnek port aralığı belirleme yeteneği.
- **Protokol Desteği:** Hem `TCP` hem de basit `UDP` port taraması gerçekleştirebilir.
- **Hız Performansı (Threading):** Kullanıcı tanımlı Thread sayısı ile yüksek tarama hızı.
- **Servis Tanıma (Banner Grabbing):** Açık portların servis ismini belirleme ve versiyon bilgisi okuyabilme (HTTP için varsayılan HTTP GET vb.).
- **Esnek Çıktı:** Renklendirilmiş (Colorama) terminal arayüzü ve tarama sonuçlarını tam kapsamlı `JSON` dosyası olarak kaydedebilme.

## ⚙️ Kurulum

Projeyi sisteminize klonlayıp çalıştırmak oldukça basittir:

1. Repoyu bilgisayarınıza klonlayın:
```bash
git clone https://github.com/muhammetozkaya/port-scanner.git
cd port-scanner
```

2. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```
*(**Not:** Araç sadece terminal renklendirmesi için `colorama` modülüne ihtiyaç duyar.)*

## 🚀 Kullanım

Araç, komut satırı argümanları ile çalışır. Terminalde `python src/scanner.py -h` komutuyla yardım menüsünü görüntüleyebilirsiniz. Ek detaylar için [docs/usage.md](docs/usage.md) dosyasına bakabilirsiniz.

| Parametre | Açıklama | Varsayılan |
| :--- | :--- | :--- |
| `-t, --target` | Hedef IP, Domain veya virgülle ayrılmış liste **(Zorunlu)** | - |
| `-p, --ports` | Taranacak port veya port aralığı (Örn: 80 veya 1-1000) | `1-1024` |
| `--protocol` | Tarama protokolü (`TCP` veya `UDP`) | `TCP` |
| `--threads` |  Eşzamanlı kullanılacak thread sayısı | `100` |
| `--timeout` |  Bağlantı veya yanıt için beklenecek saniye süresi | `1.0` |
| `-o, --output`| Sonuçları belirtilen isimle `JSON` olarak kaydeder | - |

### Örnek Komutlar:

**1. Yerel Ağdaki Temel Bir Hedefi Tarama:**
```bash
python src/scanner.py -t 192.168.1.1
```

**2. Belli Bir Aralıktaki Portları Hızlı Tarama (1000 Thread):**
```bash
python src/scanner.py -t 10.0.0.5 -p 1-65535 --threads 1000
```

**3. Domain Üzerinden Tarama ve Sonucu JSON Olarak Kaydetme:**
```bash
python src/scanner.py -t example.com -p 80,443 -o output/scan_results.json
```

**4. UDP Taraması Gerçekleştirme:**
```bash
python src/scanner.py -t 192.168.1.1 -p 53,161 --protocol UDP
```

## 📝 Geliştirici

**Muhammet Özkaya**  
*Adli Bilişim Mühendisliği Öğrencisi & Siber Güvenlik Çalışanı*

- Github: [@muhammetozkaya](https://github.com/muhammetozkaya)

## ⚖️ Lisans

Bu proje [MIT](https://choosealicense.com/licenses/mit/) lisansı altındadır. Eğitim ve güvenlik testleri amacıyla kullanılması önerilir. Kötüye kullanım durumunda sorumluluk kullanıcıya aittir.
