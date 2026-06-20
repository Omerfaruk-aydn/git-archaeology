# Analiz API

## Analiz Başlat

```
POST /api/v1/analyses
```

### Request Body

```json
{
  "repository_id": "uuid",
  "branch": "main",
  "llm_provider": "openai",
  "llm_model": "gpt-4o",
  "batch_size": 10,
  "max_commits": 1000,
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-12-31T23:59:59",
  "focus_areas": ["security", "performance"],
  "include_diffs": true
}
```

### Response

```json
{
  "id": "uuid",
  "repository_id": "uuid",
  "status": "pending",
  "progress": 0.0,
  "total_commits": 0,
  "processed_commits": 0,
  "created_at": "2024-01-01T00:00:00"
}
```

## Analiz Durumu

```
GET /api/v1/analyses/{id}
```

### Response

```json
{
  "id": "uuid",
  "repository_id": "uuid",
  "status": "running",
  "progress": 45.5,
  "total_commits": 100,
  "processed_commits": 45,
  "started_at": "2024-01-01T00:00:00"
}
```

## Analiz Sonuçları

Analiz tamamlandığında sonuçlar `result` alanında bulunur:

```json
{
  "analysis_id": "uuid",
  "repository_name": "repo-name",
  "summary": "Depo analiz özeti...",
  "time_period": {
    "start": "2024-01-01",
    "end": "2024-12-31"
  },
  "statistics": {
    "total_commits": 100,
    "total_additions": 5000,
    "total_deletions": 2000,
    "unique_authors": 10
  },
  "key_changes": [...],
  "author_contributions": [...],
  "file_hotspots": [...],
  "insights": [...],
  "recommendations": [...]
}
```
