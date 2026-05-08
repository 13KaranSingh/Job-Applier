import { LayoutShell } from "../components/layout-shell";
import { StatCard } from "../components/stat-card";
import { EmptyState } from "../components/empty-state";
import { ExportLinks } from "../components/export-links";
import { PipelineActions } from "../components/pipeline-actions";
import { ScoreBar } from "../components/score-bar";
import { StatusPill } from "../components/status-pill";
import { formatDate, getAnalyticsSummary, getSources, getTopJobs } from "../lib/api";

export const dynamic = "force-dynamic";

export default async function OverviewPage() {
  const [summary, topJobs, sources] = await Promise.all([
    getAnalyticsSummary(),
    getTopJobs(),
    getSources(),
  ]);
  const degraded = sources.filter((source) => !source.enabled).length;

  return (
    <LayoutShell
      title="Overview"
      actions={
        <div className="flex flex-wrap items-center justify-end gap-2">
          <PipelineActions />
          <ExportLinks />
        </div>
      }
    >
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Jobs Discovered" value={String(summary.jobs_discovered)} />
        <StatCard label="Top Jobs" value={String(summary.jobs_above_70)} tone="accent" />
        <StatCard label="Applications" value={String(summary.applications_submitted)} />
        <StatCard label="Active Sources" value={String(summary.active_sources)} />
      </section>
      <section className="mt-6 grid gap-4 lg:grid-cols-[1.4fr_1fr]">
        <div className="rounded-lg border border-black/5 bg-white/80 p-5 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <h3 className="font-serif text-2xl">Top Jobs Now</h3>
            <StatusPill label={`${topJobs.length} matches`} tone={topJobs.length > 0 ? "good" : "neutral"} />
          </div>
          {topJobs.length === 0 ? (
            <EmptyState label="No jobs above the Top Jobs threshold yet." />
          ) : (
            <div className="divide-y divide-stone-200">
              {topJobs.slice(0, 5).map((job) => (
                <a key={job.id} href={job.apply_url} className="grid gap-3 py-4 md:grid-cols-[1fr_160px]">
                  <div>
                    <p className="font-semibold text-stone-950">{job.company_name}</p>
                    <p className="text-sm text-stone-700">{job.title_normalized}</p>
                    <p className="mt-1 text-xs text-stone-500">
                      {job.location_normalized ?? "Unknown"} · Posted {formatDate(job.posted_at_source)}
                    </p>
                  </div>
                  <ScoreBar value={job.total_score} />
                </a>
              ))}
            </div>
          )}
        </div>
        <div className="rounded-lg border border-black/5 bg-white/80 p-5 shadow-sm">
          <h3 className="font-serif text-2xl">Source Health</h3>
          <div className="mt-4 grid gap-3">
            <div className="flex items-center justify-between border-b border-stone-200 pb-3 text-sm">
              <span className="text-stone-600">Enabled</span>
              <span className="font-semibold">{summary.active_sources}</span>
            </div>
            <div className="flex items-center justify-between border-b border-stone-200 pb-3 text-sm">
              <span className="text-stone-600">Disabled</span>
              <span className="font-semibold">{degraded}</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-stone-600">Degraded</span>
              <span className="font-semibold">{summary.degraded_sources}</span>
            </div>
          </div>
        </div>
      </section>
    </LayoutShell>
  );
}
