# Commit API

## Commit'leri Listele

```
GET /api/v1/commits?repo_id={uuid}&page=1&page_size=50
```

### Query Parameters

| Parametre | Zorunlu | Açıklama |
|-----------|---------|----------|
| repo_id | Evet | Depo UUID'si |
| page | Hayır | Sayfa numarası (varsayılan: 1) |
| page_size | Hayır | Sayfa boyutu (varsayılan: 50) |
| author | Hayır | Yazar filtresi |
| start_date | Hayır | Başlangıç tarihi |
| end_date | Hayır | Bitiş tarihi |

### Response

```json
{
  "items": [
    {
      "id": "uuid",
      "sha": "abc123def456",
      "message": "Commit mesajı",
      "author_name": "Yazar Adı",
      "author_email": "yazar@email.com",
      "author_date": "2024-01-01T00:00:00",
      "additions": 10,
      "deletions": 5,
      "files_changed": 2,
      "analyzed": true
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 50
}
```

## Commit Detayını Getir

```
GET /api/v1/commits/{id}
```

### Response

```json
{
  "id": "uuid",
  "sha": "abc123def456",
  "message": "Commit mesajı",
  "author_name": "Yazar Adı",
  "author_email": "yazar@email.com",
  "author_date": "2024-01-01T00:00:00",
  "committer_name": "Committer",
  "committer_email": "committer@email.com",
  "committer_date": "2024-01-01T00:00:00",
  "parents": ["parent_sha"],
  "additions": 10,
  "deletions": 5,
  "files_changed": 2,
  "analyzed": true,
  "analysis_result": {...},
  "file_changes": [
    {
      "id": "uuid",
      "file_path": "src/app.py",
      "change_type": "modified",
      "additions": 10,
      "deletions": 5
    }
  ]
}
```
