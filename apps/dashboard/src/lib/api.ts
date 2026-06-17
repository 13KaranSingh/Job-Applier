export const API_BASE_URL = process.env.API_BASE_URL ?? "http://127.0.0.1:8000";

export type AnalyticsSummary = {
  jobs_discovered: number;
  applications_submitted: number;
  jobs_above_70: number;
  active_sources: number;
  degraded_sources: number;
};

export type TopJob = {
  id: string;
  company_name: string;
  title_normalized: string;
  location_normalized: string | null;
  remote_policy: string | null;
  role_family: string;
  status: string;
  apply_url: string;
  source_name: string;
  posted_at_source: string | null;
  first_seen_at: string | null;
  total_score: number;
  compensation_score: number;
  prestige_score: number;
  quant_score: number;
  swe_score: number;
  automation_readiness_score: number;
  recency_score: number;
  company_priority_score: number;
  location_fit_score: number;
  recommended_action: string;
};

export type JobFeedItem = {
  id: string;
  company_name: string;
  title_normalized: string;
  location_normalized: string | null;
  status: string;
  first_seen_at: string | null;
  posted_at_source: string | null;
  apply_url: string;
};

export type SourceItem = {
  id: string;
  name: string;
  slug: string;
  enabled: boolean;
  source_type: string;
  priority_weight: number;
  polling_interval_seconds: number;
  supports_auto_apply: boolean;
  config_json: Record<string, unknown>;
  health: {
    status: string;
    last_success_at: string | null;
    last_failure_at: string | null;
    recent_error_summary: string | null;
  } | null;
};

export type ApplicationItem = {
  id: string;
  job_id: string;
  status: string;
  application_mode: string;
  resume_variant: string;
  submitted_at: string | null;
  company_name: string;
  title_normalized: string;
  location_normalized: string | null;
  apply_url: string;
  notes: string | null;
  failure_code: string | null;
  failure_stage: string | null;
};

export type ProfilePayload = {
  profile: Record<string, unknown> | null;
};

export type AnswerItem = {
  id: string;
  answer_key: string;
  category: string;
  prompt_patterns: string[];
  answer_text: string;
  requires_human_review: boolean;
  active: boolean;
};

export type ResumeItem = {
  id: string;
  variant_name: string;
  file_path: string;
  active: boolean;
  metadata_json: Record<string, unknown>;
};

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error(`API ${path} failed with ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function getAnalyticsSummary(): Promise<AnalyticsSummary> {
  const payload = await fetchJson<{ summary: AnalyticsSummary }>("/analytics/summary");
  return payload.summary;
}

export async function getTopJobs(params?: {
  sort_mode?: string;
  track?: string;
  remote_only?: boolean;
  auto_apply_only?: boolean;
}): Promise<TopJob[]> {
  const search = new URLSearchParams();
  if (params?.sort_mode) {
    search.set("sort_mode", params.sort_mode);
  }
  if (params?.track) {
    search.set("track", params.track);
  }
  if (params?.remote_only) {
    search.set("remote_only", "true");
  }
  if (params?.auto_apply_only) {
    search.set("auto_apply_only", "true");
  }
  const suffix = search.size > 0 ? `?${search.toString()}` : "";
  const payload = await fetchJson<{ items: TopJob[] }>(`/jobs/top${suffix}`);
  return payload.items;
}

export async function getJobs(): Promise<JobFeedItem[]> {
  const payload = await fetchJson<{ items: JobFeedItem[] }>("/jobs");
  return payload.items;
}

export async function getSources(): Promise<SourceItem[]> {
  const payload = await fetchJson<{ items: SourceItem[] }>("/sources");
  return payload.items;
}

export async function getApplications(): Promise<ApplicationItem[]> {
  const payload = await fetchJson<{ items: ApplicationItem[] }>("/applications");
  return payload.items;
}

export async function getProfile(): Promise<ProfilePayload> {
  return fetchJson<ProfilePayload>("/profile");
}

export async function getAnswers(): Promise<AnswerItem[]> {
  const payload = await fetchJson<{ items: AnswerItem[] }>("/answers");
  return payload.items;
}

export async function getResumes(): Promise<ResumeItem[]> {
  const payload = await fetchJson<{ items: ResumeItem[] }>("/resumes");
  return payload.items;
}

export function formatDate(value: string | null): string {
  if (!value) {
    return "Unknown";
  }
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(value));
}
