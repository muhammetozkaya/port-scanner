# Professional Port Scanner - Kullanım Kılavuzu

Hoş geldiniz! Bu araç, siber güvenlik değerlendirmeleri, açık port kontrolleri ve servis tanıma amaçlarıyla geliştirilmiş esnek ve çoklu iş parçacıklı bir komut satırı aracıdır.

## Gelişmiş Kullanım

Aşağıda farklı network senaryolarında aracı nasıl kullanabileceğinize dair örnek ve ipuçları yer almaktadır:

### 1. Basit Tekli IP Taraması
Tek bir IP'nin varsayılan portlarını (1-1024) tarar.
```bash
python src/scanner.py -t 192.168.1.5
```

### 2. Belirlenen Portları Tarama
Bir veya birden çok (belirli bir aralık) portu tarayabilirsiniz.
```bash
# Tek bir port (ör. 80 - HTTP)
python src/scanner.py -t 10.0.0.1 -p 80

# Port aralığı (1-65535 tüm portlar)
python src/scanner.py -t 127.0.0.1 -p 1-65535
```

### 3. Çoklu IP (Multi-Target) Tarama
Birden çok hedefi virgül ile ayırarak bir kerede tarayabilirsiniz.
```bash
python src/scanner.py -t 192.168.1.1,192.168.1.254,google.com -p 80-443
```

### 4. UDP Port Taraması
`TCP` varsayılandır. Eğer UDP bağlantı noktalarını taramak istiyorsanız `--protocol` parametresini kullanın.
```bash
python src/scanner.py -t 192.168.1.1 -p 53,161 --protocol UDP
```

### 5. Hız Ayarı (Threading)
Taramanın hızını artırmak veya ağ üzerinde çok fazla yük (gürültü) yaratmamak için eşzamanlı bağlanan thread'leri ayarlayabilirsiniz.
```bash
# Agresif ve hızlı (Tavsiye edilen max: 1000-2000)
python src/scanner.py -t 192.168.1.1 -p 1-65535 --threads 1000

# Gizli (Stealthy) ve yavaş (Daha az gürültü)
python src/scanner.py -t 192.168.1.1 -p 1-1000 --threads 5 --timeout 3.0
```

### 6. Sonuçları JSON Formatında Çıktı Alma
Taramayı bitirdikten sonra sonuçları kolay log analizi için bir JSON dosyasına dökebilirsiniz:
```bash
python src/scanner.py -t example.com -p 1-1000 -o output/scan_results.json
```

## Notlar
- Hedef sistemlere izin almadan tarama yapmayınız, etik hacking kuralları çerçevesinde kullanınız.
- Bu uygulama eğitim amaçlı ve siber güvenlik profesyonelleri için yazılmıştır. Yasadışı kullanımından yazar sorumlu tutulamaz.
