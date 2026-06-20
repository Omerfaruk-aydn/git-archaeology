# Katkıda Bulunma Rehberi

## Başlangıç

1. Depoyu fork edin
2. Feature branch oluşturun:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Değişikliklerinizi commit edin:
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. Branch'i push edin:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Pull Request oluşturun

## Kod Standartları

### Python (Backend)

- PEP 8 formatı
- Black ile biçimlendirme
- Type hint kullanımı zorunlu
- Docstring zorunlu (public fonksiyonlar için)

```bash
# Biçimlendirme
black .

# Lint
flake8 .

# Type check
mypy .
```

### TypeScript (Frontend)

- ESLint + Prettier
- Functional component kullanımı
- Type safety

```bash
# Lint
npm run lint

# Type check
npm run type-check
```

## Commit Mesajları

Conventional Commits formatı:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Tipler

- `feat`: Yeni özellik
- `fix`: Hata düzeltme
- `docs`: Dokümantasyon
- `style`: Kod stili (fonksiyonel değişiklik yok)
- `refactor`: Kod yeniden yapılandırma
- `test`: Test ekleme/düzeltme
- `chore`: Build süreci veya yardımcı araç değişiklikleri

### Örnekler

```
feat(analysis): add LLM provider selection
fix(cache): resolve Redis connection timeout
docs(api): update authentication guide
test(git): add unit tests for GitService
```

## Branch İsimlendirmesi

- `feature/` - Yeni özellikler
- `bugfix/` - Hata düzeltmeleri
- `hotfix/` - Acil düzeltmeler
- `release/` - Release hazırlıkları

## Pull Request Kuralları

1. PR başlığı açıklayıcı olmalı
2. Değişiklikler test edilmeli
3. Coverage %80'in altında olmamalı
4. Review sonrası merge edilmeli
5. Squash merge tercih edilmeli

## Review Süreci

1. En az 1 review gerekli
2. CI checks geçmeli
3. Conflict olmamalı
4. Documentation güncellenmeli (gerekirse)
