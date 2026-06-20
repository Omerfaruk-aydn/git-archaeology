# Veritabanı Mimarisi

## Tablolar

### users
Kullanıcı bilgileri Deposu.

| Kolon | Tip | Açıklama |
|-------|-----|----------|
| id | UUID | Primary key |
| email | VARCHAR(255) | Benzersiz email |
| username | VARCHAR(255) | Benzersiz kullanıcı adı |
| hashed_password | VARCHAR(255) | Şifrelenmiş şifre (OAuth için nullable) |
| full_name | VARCHAR(255) | Tam ad |
| avatar_url | VARCHAR(1024) | Avatar URL |
| oauth_provider | VARCHAR(50) | OAuth sağlayıcı |
| oauth_id | VARCHAR(255) | OAuth ID |
| is_active | BOOLEAN | Hesap aktif mi |
| created_at | DATETIME | Oluşturulma tarihi |

### repositories
Git depoları Deposu.

| Kolon | Tip | Açıklama |
|-------|-----|----------|
| id | UUID | Primary key |
| name | VARCHAR(255) | Depo adı |
| url | VARCHAR(1024) | Git URL |
| local_path | VARCHAR(1024) | Yerel depo yolu |
| default_branch | VARCHAR(255) | Varsayılan dal |
| description | TEXT | Açıklama |
| is_analyzed | BOOLEAN | Analiz edildi mi |
| last_analyzed_at | DATETIME | Son analiz tarihi |
| created_at | DATETIME | Oluşturulma tarihi |
| updated_at | DATETIME | Güncellenme tarihi |
| owner_id | UUID | Depo sahibi (users.id) |

### commits
Commit geçmişi Deposu.

| Kolon | Tip | Açıklama |
|-------|-----|----------|
| id | UUID | Primary key |
| repository_id | UUID | Depo (repositories.id) |
| sha | VARCHAR(40) | Commit SHA |
| message | TEXT | Commit mesajı |
| author_name | VARCHAR(255) | Yazar adı |
| author_email | VARCHAR(255) | Yazar email |
| author_date | DATETIME | Yazar tarihi |
| committer_name | VARCHAR(255) | Committer adı |
| committer_email | VARCHAR(255) | Committer email |
| committer_date | DATETIME | Committer tarihi |
| parents | JSONB | Parent commit'ler |
| additions | INTEGER | Eklenen satır sayısı |
| deletions | INTEGER | Silinen satır sayısı |
| files_changed | INTEGER | Değişen dosya sayısı |
| analyzed | BOOLEAN | Analiz edildi mi |
| analysis_result | JSONB | Analiz sonucu |

### file_changes
Dosya değişiklikleri Deposu.

| Kolon | Tip | Açıklama |
|-------|-----|----------|
| id | UUID | Primary key |
| commit_id | UUID | Commit (commits.id) |
| file_path | VARCHAR(1024) | Dosya yolu |
| old_path | VARCHAR(1024) | Eski dosya yolu |
| change_type | VARCHAR(50) | Değişiklik türü |
| additions | INTEGER | Eklenen satır |
| deletions | INTEGER | Silinen satır |
| diff | TEXT | Diff içeriği |
| old_content | TEXT | Eski içeriği |
| new_content | TEXT | Yeni içeriği |
| analysis | JSONB | Analiz sonucu |

### analyses
Analiz Deposu.

| Kolon | Tip | Açıklama |
|-------|-----|----------|
| id | UUID | Primary key |
| repository_id | UUID | Depo (repositories.id) |
| status | VARCHAR(50) | Analiz durumu |
| progress | FLOAT | İlerleme yüzdesi |
| total_commits | INTEGER | Toplam commit |
| processed_commits | INTEGER | İşlenen commit |
| error_message | TEXT | Hata mesajı |
| result | JSONB | Analiz sonucu |
| config | JSONB | Analiz yapılandırması |

## İndeksler

```sql
-- Composite indexes
CREATE INDEX idx_commits_repo_date ON commits(repository_id, author_date DESC);
CREATE INDEX idx_commits_repo_author ON commits(repository_id, author_name);
CREATE INDEX idx_file_changes_repo_path ON file_changes(commit_id, file_path);
CREATE INDEX idx_analyses_repo_status ON analyses(repository_id, status);

-- Partial indexes
CREATE INDEX idx_commits_unanalyzed ON commits(repository_id) WHERE analyzed = false;
CREATE INDEX idx_analyses_running ON analyses(repository_id) WHERE status = 'running';
```
