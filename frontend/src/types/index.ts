export interface Repository {
  id: string;
  name: string;
  url: string;
  local_path: string | null;
  default_branch: string;
  description: string | null;
  is_analyzed: boolean;
  last_analyzed_at: string | null;
  created_at: string;
  updated_at: string;
  commit_count?: number;
  contributor_count?: number;
}

export interface Commit {
  id: string;
  sha: string;
  message: string;
  author_name: string;
  author_email: string;
  author_date: string;
  additions: number;
  deletions: number;
  files_changed: number;
  analyzed: boolean;
  analysis_result: Record<string, any> | null;
}

export interface CommitDetail extends Commit {
  parents: string[];
  committer_name: string;
  committer_email: string;
  committer_date: string;
  file_changes: FileChange[];
}

export interface FileChange {
  id: string;
  file_path: string;
  old_path: string | null;
  change_type: 'added' | 'modified' | 'deleted' | 'renamed';
  additions: number;
  deletions: number;
  diff?: string;
  analysis?: Record<string, any>;
}

export interface Analysis {
  id: string;
  repository_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  total_commits: number;
  processed_commits: number;
  error_message: string | null;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
}

export interface AnalysisResult {
  analysis_id: string;
  repository_name: string;
  summary: string;
  time_period: {
    start: string;
    end: string;
  };
  statistics: {
    total_commits: number;
    total_additions: number;
    total_deletions: number;
  };
  key_changes: Array<{
    path: string;
    changes: number;
  }>;
  author_contributions: Array<{
    name: string;
    commits: number;
    additions: number;
    deletions: number;
  }>;
  file_hotspots: Array<{
    path: string;
    changes: number;
  }>;
  insights: string[];
  recommendations: string[];
}

export interface Report {
  id: string;
  repository_id: string;
  report_type: string;
  content: string;
  format: string;
  generated_at: string;
  metadata: Record<string, any> | null;
}

export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string | null;
  avatar_url: string | null;
}

export interface AuthTokens {
  access_token: string;
  token_type: string;
  expires_in: number;
  refresh_token: string | null;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export interface AnalysisConfig {
  repository_id: string;
  branch?: string;
  start_date?: string;
  end_date?: string;
  max_commits?: number;
  llm_provider: 'openai' | 'anthropic' | 'local';
  llm_model?: string;
  focus_areas?: string[];
  include_diffs?: boolean;
  batch_size?: number;
}
