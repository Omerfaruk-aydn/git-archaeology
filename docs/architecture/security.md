# Güvenlik Mimarisi

## Kimlik Doğrulama

### JWT Token

- Token süresi: 60 dakika
- Algoritma: HS256
- Secret key: Ortam değişkeninden okunur

### OAuth2

GitHub ve GitLab OAuth entegrasyonu desteklenir.

## Yetkilendirme

Her kullanıcı yalnızca kendi depolarına erişebilir.

```python
# Örnek yetkilendirme kontrolü
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    # Token doğrulama
    # Kullanıcı arama
    # Aktiflik kontrolü
```

## Rate Limiting

- İstek limiti: 60/dakika
- Redis tabanlı sayacı
- IP bazlı filtreleme

## Veri Güvenliği

- Şifreler: bcrypt ile hash'lenmiş
- API anahtarları: Ortam değişkenlerinde saklanır
- Hassas veriler: Loglanmaz
- HTTPS: Üretimde zorunlu

## Middleware Korumaları

1. **ErrorHandlerMiddleware**: Hata yakalama ve loglama
2. **RateLimitMiddleware**: İstek hız sınırlama
3. **MonitoringMiddleware**: İstek izleme ve süre ölçümü
