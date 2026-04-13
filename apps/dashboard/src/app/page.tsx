import { LayoutShell } from "../components/layout-shell";
import { StatCard } from "../components/stat-card";

export default function OverviewPage() {
  return (
    <LayoutShell title="Overview">
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Jobs Discovered Today" value="0" />
        <StatCard label="Applications Today" value="0" />
        <StatCard label="Failures Today" value="0" />
        <StatCard label="Average Score" value="0.0" tone="accent" />
      </section>
      <section className="mt-6 grid gap-4 lg:grid-cols-[1.4fr_1fr]">
        <div className="rounded-3xl border border-black/5 bg-white/70 p-6 shadow-md">
          <h3 className="font-serif text-2xl">Top 10 Jobs Now</h3>
          <p className="mt-2 text-sm text-stone-600">Live queue will render here once the API is wired.</p>
        </div>
        <div className="rounded-3xl border border-black/5 bg-white/70 p-6 shadow-md">
          <h3 className="font-serif text-2xl">Source Health</h3>
          <p className="mt-2 text-sm text-stone-600">Per-source status, queue depth, and sync lag.</p>
        </div>
      </section>
    </LayoutShell>
  );
}

