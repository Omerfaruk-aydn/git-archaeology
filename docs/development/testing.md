# Test Rehberi

## Backend Testleri

### Test Çalıştırma

```bash
cd backend

# Tüm testleri çalıştır
pytest

# Belirli test dosyasını çalıştır
pytest tests/test_git_service.py

# Verilen pattern ile testleri çalıştır
pytest -k "test_validate"

# Coverage ile çalıştır
pytest --cov=app --cov-report=html

# Veritabanı testleri (SQLite)
pytest --tb=short
```

### Test Yapısı

```
tests/
├── conftest.py           # Fixtures
├── test_git_service.py   # Git servisi testleri
├── test_analysis_engine.py # Analiz motoru testleri
└── test_api/             # API endpoint testleri
    ├── test_repositories.py
    ├── test_analyses.py
    └── test_auth.py
```

### Fixture'lar

```python
# conftest.py
@pytest.fixture
def db_session():
    # Test veritabanı session'ı
    pass

@pytest.fixture
def client(db_session):
    # Test client
    pass
```

## Frontend Testleri

### Test Çalıştırma

```bash
cd frontend

# Tüm testleri çalıştır
npm test

# Watch modunda
npm test -- --watch

# Coverage ile
npm test -- --coverage

# Tek test dosyası
npm test -- Dashboard.test.tsx
```

### Test Yapısı

```
src/
├── __tests__/
│   ├── Dashboard.test.tsx
│   ├── Repositories.test.tsx
│   └── Analysis.test.tsx
└── components/
    └── __tests__/
        └── RepositoryList.test.tsx
```

### Örnek Test

```tsx
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { Dashboard } from '../pages/Dashboard';

describe('Dashboard', () => {
  it('renders loading state initially', () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });
});
```

## CI/CD Testleri

GitHub Actions'da otomatik çalışır:

1. Backend testleri (Python 3.11, PostgreSQL)
2. Frontend testleri (Node.js 20)
3. Docker build testleri
4. Lint ve type-check
