# Analiz Çalıştırma Rehberi

## Analiz Başlatma

### Adım 1: Depoyu Seçin

Depolar listesinden analiz etmek istediğiniz depoyu seçin.

### Adım 2: Analiz Başlat

Depo detay sayfasında "Analiz Başlat" butonuna tıklayın.

### Adım 3: Analiz Ayarlarını Yapın

#### LLM Sağlayıcı Seçimi

| Sağlayıcı | Avantaj | Dezavantaj |
|-----------|---------|------------|
| OpenAI GPT-4o | Yüksek kalite | Yüksek maliyet |
| Anthropic Claude | Yüksek kalite | Orta maliyet |
| Yerel LLM | Düşük maliyet | Düşük kalite |

#### Model Seçimi

- **gpt-4o**: En yüksek kalite
- **gpt-4-turbo**: Yüksek kalite, daha hızlı
- **claude-3-5-sonnet**: Yüksek kalite
- **llama3**: Yerel model

#### İleri Ayarlar

- **Batch Boyutu**: 1-50 arası (varsayılan: 10)
- **Maks Commit**: İşlenecek maksimum commit sayısı
- **Tarih Aralığı**: Belirli dönemdeki commit'ler
- **Odak Alanları**: security, performance, architecture

### Adım 4: Analizi Başlat

"Analizi Başlat" butonuna tıklayın.

## Analiz Süreci

### 1. Hazırlık

- Depo bilgileri doğrulanır
- Commit listesi alınır
- Analiz kaydı oluşturulur

### 2. İşleme

Her batch için:
- Commit'ler veritabanına kaydedilir
- Dosya değişiklikleri kaydedilir
- LLM ile analiz edilir
- Sonuçlar kaydedilir

### 3. Tamamlama

- Genel özet oluşturulur
- Analiz sonuçları birleştirilir
- Durum "completed" olarak güncellenir

## Analiz Sonuçları

### Genel İstatistikler

- Toplam commit sayısı
- Toplam eklenen/silinen satır
- Benzersiz yazar sayısı
- Tarih aralığı

### Dosya Hotspot'ları

En çok değişen dosyalar listelenir.

### Yazar Katkıları

Her yazarın katkıları gösterilir.

### Öneriler

LLM tarafından oluşturulan öneriler.

## Analiz Durumu

| Durum | Açıklama |
|-------|----------|
| pending | Başlatılmadı |
| running | Devam ediyor |
| completed | Tamamlandı |
| failed | Başarısız oldu |

## Sorun Giderme

### Analiz Başarısız Oldu

1. Hata mesajını kontrol edin
2. LLM API anahtarını doğrulayın
3. Bağlantı sorunlarını kontrol edin
4. Yeniden deneyin

### Analiz Çok Uzun Sürüyor

1. Batch boyutunu artırın
2. Maks commit sayısını azaltın
3. Tarih aralığını daraltın
4. Daha hızlı bir model seçin

### Sonuçlar Eksik

1. Analiz durumunu kontrol edin
2. Commit sayısını doğrulayın
3. Yeniden analiz edin
