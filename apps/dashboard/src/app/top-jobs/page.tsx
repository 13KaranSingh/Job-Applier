import { LayoutShell } from "../../components/layout-shell";
import { EmptyState } from "../../components/empty-state";
import { ExportLinks } from "../../components/export-links";
import { ScoreBar } from "../../components/score-bar";
import { StatusPill } from "../../components/status-pill";
import { ActionButton } from "../../components/action-button";
import { formatDate, getTopJobs } from "../../lib/api";

export const dynamic = "force-dynamic";

const sortModes = [
  "best_overall",
  "highest_pay",
  "highest_prestige",
  "best_quant",
  "best_swe",
  "fastest_apply",
  "best_remote",
] as const;

const trackFilters = ["all", "swe", "quant", "both"] as const;

export default async function TopJobsPage({
  searchParams,
}: {
  searchParams?: Promise<Record<string, string | string[] | undefined>>;
}) {
  const params = (await searchParams) ?? {};
  const sortMode = typeof params.sort_mode === "string" && sortModes.includes(params.sort_mode as (typeof sortModes)[number])
    ? params.sort_mode
    : "best_overall";
  const track = typeof params.track === "string" && trackFilters.includes(params.track as (typeof trackFilters)[number])
    ? params.track
    : "all";
  const remoteOnly = params.remote_only === "true";
  const autoApplyOnly = params.auto_apply_only === "true";
  const jobs = await getTopJobs({
    sort_mode: sortMode,
    track: track === "all" ? undefined : track,
    remote_only: remoteOnly,
    auto_apply_only: autoApplyOnly,
  });
  const baseParams = new URLSearchParams();

  function buildHref(next: { sort_mode?: string; track?: string; remote_only?: boolean; auto_apply_only?: boolean }) {
    const qp = new URLSearchParams(baseParams);
    qp.set("sort_mode", next.sort_mode ?? sortMode);
    qp.set("track", next.track ?? track);
    if (next.remote_only ?? remoteOnly) {
      qp.set("remote_only", "true");
    } else {
      qp.delete("remote_only");
    }
    if (next.auto_apply_only ?? autoApplyOnly) {
      qp.set("auto_apply_only", "true");
    } else {
      qp.delete("auto_apply_only");
    }
    return `/top-jobs?${qp.toString()}`;
  }

  return (
    <LayoutShell
      title="Top Jobs"
      actions={<div className="flex flex-wrap items-center gap-2"><StatusPill label={`${jobs.length} active matches`} tone={jobs.length > 0 ? "good" : "neutral"} /><ExportLinks /></div>}
    >
      <div className="mb-4 grid gap-3 rounded-lg border border-black/5 bg-white/85 p-4 shadow-sm">
        <div className="flex flex-wrap gap-2">
          {sortModes.map((mode) => (
            <a
              key={mode}
              href={buildHref({ sort_mode: mode })}
              className={`rounded-md border px-3 py-1.5 text-xs font-semibold ${sortMode === mode ? "border-[var(--accent)] bg-[var(--accent)] text-white" : "border-stone-300 bg-white text-stone-700 hover:bg-stone-100"}`}
            >
              {mode}
            </a>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          {trackFilters.map((item) => (
            <a
              key={item}
              href={buildHref({ track: item })}
              className={`rounded-md border px-3 py-1.5 text-xs font-semibold ${track === item ? "border-[var(--accent)] bg-[var(--accent)] text-white" : "border-stone-300 bg-white text-stone-700 hover:bg-stone-100"}`}
            >
              {item}
            </a>
          ))}
          <a
            href={buildHref({ remote_only: !remoteOnly })}
            className={`rounded-md border px-3 py-1.5 text-xs font-semibold ${remoteOnly ? "border-[var(--accent)] bg-[var(--accent)] text-white" : "border-stone-300 bg-white text-stone-700 hover:bg-stone-100"}`}
          >
            remote_only
          </a>
          <a
            href={buildHref({ auto_apply_only: !autoApplyOnly })}
            className={`rounded-md border px-3 py-1.5 text-xs font-semibold ${autoApplyOnly ? "border-[var(--accent)] bg-[var(--accent)] text-white" : "border-stone-300 bg-white text-stone-700 hover:bg-stone-100"}`}
          >
            auto_apply_only
          </a>
        </div>
      </div>
      <div className="overflow-hidden rounded-lg border border-black/5 bg-white/85 shadow-sm">
        {jobs.length === 0 ? (
          <EmptyState label="No ranked jobs above 70. Run polling and ranking, then refresh." />
        ) : (
          <table className="w-full table-fixed text-left text-sm">
            <thead className="border-b border-stone-200 bg-stone-50 text-xs uppercase text-stone-500">
              <tr>
                <th className="w-[28%] px-4 py-3">Role</th>
                <th className="w-[18%] px-4 py-3">Location</th>
                <th className="w-[18%] px-4 py-3">Scores</th>
                <th className="w-[18%] px-4 py-3">Timing</th>
                <th className="w-[18%] px-4 py-3">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-stone-200">
              {jobs.map((job) => (
                <tr key={job.id} className="align-top">
                  <td className="px-4 py-4">
                    <p className="font-semibold text-stone-950">{job.company_name}</p>
                    <p className="mt-1 text-stone-700">{job.title_normalized}</p>
                    <p className="mt-2 text-xs text-stone-500">{job.source_name}</p>
                  </td>
                  <td className="px-4 py-4 text-stone-700">{job.location_normalized ?? "Unknown"}</td>
                  <td className="px-4 py-4">
                    <ScoreBar value={job.total_score} />
                    <p className="mt-2 text-xs text-stone-500">
                      {job.role_family.toUpperCase()} · SWE {job.swe_score.toFixed(1)} · Quant {job.quant_score.toFixed(1)}
                    </p>
                  </td>
                  <td className="px-4 py-4 text-xs text-stone-600">
                    <p>Posted {formatDate(job.posted_at_source)}</p>
                    <p className="mt-1">Seen {formatDate(job.first_seen_at)}</p>
                    <p className="mt-1 uppercase">{job.remote_policy ?? "unknown"}</p>
                  </td>
                  <td className="px-4 py-4">
                    <StatusPill label={job.recommended_action} tone="warn" />
                    <div className="mt-3 flex flex-wrap gap-2">
                      <ActionButton label="Rerank" endpoint={`/api/jobs/${job.id}/rerank`} />
                      <ActionButton label="Queue Apply" endpoint={`/api/jobs/${job.id}/apply`} tone="accent" />
                      <a className="rounded-md border border-stone-300 bg-white px-3 py-1.5 text-xs font-semibold text-stone-700 hover:bg-stone-100" href={job.apply_url}>
                        Open
                      </a>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </LayoutShell>
  );
}
