import { LayoutShell } from "../../components/layout-shell";
import { EmptyState } from "../../components/empty-state";
import { ExportLinks } from "../../components/export-links";
import { ScoreBar } from "../../components/score-bar";
import { StatusPill } from "../../components/status-pill";
import { ActionButton } from "../../components/action-button";
import { formatDate, getTopJobs } from "../../lib/api";

export const dynamic = "force-dynamic";

export default async function TopJobsPage() {
  const jobs = await getTopJobs();

  return (
    <LayoutShell
      title="Top Jobs"
      actions={<div className="flex flex-wrap items-center gap-2"><StatusPill label={`${jobs.length} active matches`} tone={jobs.length > 0 ? "good" : "neutral"} /><ExportLinks /></div>}
    >
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
                      SWE {job.swe_score.toFixed(1)} · Quant {job.quant_score.toFixed(1)}
                    </p>
                  </td>
                  <td className="px-4 py-4 text-xs text-stone-600">
                    <p>Posted {formatDate(job.posted_at_source)}</p>
                    <p className="mt-1">Seen {formatDate(job.first_seen_at)}</p>
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
