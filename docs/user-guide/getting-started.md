# Başlangıç Rehberi

## Hoş Geldiniz!

Git Arkeoloji Aracı, Git depolarını analiz eden AI destekli bir araçtır. Bu rehber size uygulamayı nasıl kullanacağınızı gösterecek.

## İlk Adımlar

### 1. Uygulamaya Giriş

Tarayıcınızda http://localhost:3000 adresine gidin.

### 2. Kayıt Olma

"Kayıt Ol" butonuna tıklayıp bilgilerinizi girin:
- E-posta adresi
- Kullanıcı adı
- Şifre (en az 8 karakter)
- Tam ad (opsiyonel)

### 3. Giriş Yapma

E-posta ve şifrenizle giriş yapın.

## Depo Ekleme

### 1. Depo Oluştur

Sol menüden "Depolar" > "Yeni Depo" seçeneğine tıklayın.

### 2. Bilgileri Doldurun

- **Depo Adı**: Deponuzun adı
- **Git URL**: Depo URL'si (örn: https://github.com/user/repo.git)
- **Açıklama**: Depo hakkında kısa bilgi
- **Varsayılan Dal**: Genellikle "main" veya "master"

### 3. Kaydedin

"Depo Oluştur" butonuna tıklayın.

## Analiz Başlatma

### 1. Depoyu Seçin

Depolar listesinden analiz etmek istediğiniz depoyu seçin.

### 2. Analiz Başlat

"Analiz Başlat" butonuna tıklayın.

### 3. Ayarları Yapın

- **LLM Sağlayıcı**: OpenAI, Anthropic veya Yerel LLM
- **Model**: Kullanılacak model
- **Batch Boyutu**: İşlenecek commit sayısı
- **Tarih Aralığı**: Analiz edilecek dönem

### 4. Başlat

"Analizi Başlat" butonuna tıklayın.

## Rapor Oluşturma

### 1. Rapor Türünü Seçin

- **Kapsamlı Rapor**: Tüm analiz sonuçları
- **Özet Rapor**: Kısa özet
- **Güvenlik Raporu**: Güvenlik odaklı
- **Mimari Rapor**: Mimari analiz
- **Legacy Kod Raporu**: Legacy kod analizi

### 2. Ayarları Yapın

- Format: Markdown veya HTML
- Dal: Belirli bir dal
- Tarih Aralığı: Belirli dönem
- Dosya Yolları: Belirli dosyalar

### 3. Oluşturun

"Rapor Oluştur" butonuna tıklayın.

## Ayarlar

### Profil Ayarları

- E-posta güncelleme
- Şifre değiştirme
- Avatar yükleme

### Bildirimler

- E-posta bildirimleri
- Analiz tamamlanma bildirimleri

### Güvenlik

- İki faktörlü kimlik doğrulama
- Oturum yönetimi
- API anahtarı oluşturma

## Sıkça Sorulan Sorular

### Analiz neden uzun sürüyor?

Büyük depolarda çok sayıda commit bulunduğu için analiz uzun sürebilir. İlerleme çubuğunu takip edebilirsiniz.

### Hangi LLM modelini kullanmalıyım?

- **OpenAI GPT-4o**: En yüksek kalite, en yüksek maliyet
- **Anthropic Claude**: Yüksek kalite, orta maliyet
- **Yerel LLM**: Düşük maliyet, daha düşük kalite

### Raporları nasıl dışa aktarabilirim?

Rapor oluşturduktan sonra "İndir" butonuna tıklayarak Markdown veya HTML formatında indirebilirsiniz.
