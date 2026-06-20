# Rapor API

## Rapor Oluştur

```
POST /api/v1/reports
```

### Request Body

```json
{
  "repository_id": "uuid",
  "report_type": "full",
  "branch": "main",
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-12-31T23:59:59",
  "file_paths": ["src/app.py", "src/utils.py"],
  "format": "markdown"
}
```

### Rapor Türleri

| Tür | Açıklama |
|-----|----------|
| full | Kapsamlı analiz raporu |
| summary | Kısa özet raporu |
| security | Güvenlik odaklı analiz |
| architecture | Mimari analiz |
| legacy | Legacy kod analizi |

### Response

```json
{
  "id": "uuid",
  "repository_id": "uuid",
  "report_type": "full",
  "content": "# Git Arkeoloji Raporu\n\n...",
  "format": "markdown",
  "generated_at": "2024-01-01T00:00:00",
  "metadata": {
    "commit_count": 100,
    "date_range": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    }
  }
}
```

## Raporu İndir

```
GET /api/v1/reports/{id}/download
```

Response olarak dosya döner.
