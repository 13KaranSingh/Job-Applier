import { LayoutShell } from "../../components/layout-shell";
import { StatCard } from "../../components/stat-card";
import { getAnalyticsSummary } from "../../lib/api";

export const dynamic = "force-dynamic";

export default async function AnalyticsPage() {
  const summary = await getAnalyticsSummary();

  return (
    <LayoutShell title="Analytics">
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <StatCard label="Discovered" value={String(summary.jobs_discovered)} />
        <StatCard label="Above 70" value={String(summary.jobs_above_70)} tone="accent" />
        <StatCard label="Applications" value={String(summary.applications_submitted)} />
        <StatCard label="Sources" value={String(summary.active_sources)} />
        <StatCard label="Degraded" value={String(summary.degraded_sources)} />
      </section>
      <div className="mt-6 rounded-lg border border-black/5 bg-white/80 p-5 text-sm text-stone-600 shadow-sm">
        Conversion and latency charts will populate once live polling has more historical events.
      </div>
    </LayoutShell>
  );
}
