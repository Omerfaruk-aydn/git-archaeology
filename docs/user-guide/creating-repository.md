# Depo Oluşturma Rehberi

## Depo Ekleme

### Adım 1: Depo Formunu Açın

Sol menüden "Depolar" > "Yeni Depo" seçeneğine tıklayın.

### Adım 2: Depo Bilgilerini Girin

| Alan | Açıklama | Örnek |
|------|----------|-------|
| Depo Adı | Deponuzun adı | my-project |
| Git URL | Depo URL'si | https://github.com/user/repo.git |
| Açıklama | Kısa açıklama | Web uygulaması projesi |
| Varsayılan Dal | Ana dal | main |

### Adım 3: Kaydedin

"Depo Oluştur" butonuna tıklayın.

## Depo Türleri

### Public Depolar

- Herkes tarafından görüntülenebilir
- URL ile erişilebilir
- Kimlik doğrulaması gerekmez

### Private Depolar

- Yalnızca yetkili kullanıcılar tarafından görüntülenebilir
- Kimlik doğrulaması gerekir
- API token gerektirir

## Desteklenen Git Sağlayıcıları

| Sağlayıcı | Destek | Notlar |
|-----------|--------|--------|
| GitHub | Evet | Public ve private |
| GitLab | Evet | Public ve private |
| Bitbucket | Evet | Public ve private |
| Yerel | Evet | Lokal depolar |

## Depo Ayarları

### Dal Seçimi

Analiz edilecek dalı seçin:
- **main**: Varsayılan dal
- **develop**: Geliştirme dalı
- **Belirli bir dal**: Özel dal adı

### Analiz Ayarları

- **Batch Boyutu**: İşlenecek commit sayısı (1-50)
- **Maks Commit**: İşlenecek maksimum commit
- **Tarih Aralığı**: Belirli dönem
- **Dosya Filtreleri**: Belirli dosyalar

## Depo Silme

1. Depo detay sayfasına gidin
2. "Ayarlar" sekmesine tıklayın
3. "Depoyu Sil" butonuna tıklayın
4. Onaylayın

**Not**: Depo silme geri alınamaz. Tüm analiz sonuçları ve raporlar silinir.
