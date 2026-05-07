import { LayoutShell } from "../../components/layout-shell";
import { EmptyState } from "../../components/empty-state";
import { StatusPill } from "../../components/status-pill";
import { formatDate, getJobs } from "../../lib/api";

export const dynamic = "force-dynamic";

export default async function JobsPage() {
  const jobs = await getJobs();

  return (
    <LayoutShell title="All Jobs" actions={<StatusPill label={`${jobs.length} jobs`} />}>
      <div className="overflow-hidden rounded-lg border border-black/5 bg-white/85 shadow-sm">
        {jobs.length === 0 ? (
          <EmptyState label="No jobs discovered yet." />
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="border-b border-stone-200 bg-stone-50 text-xs uppercase text-stone-500">
              <tr>
                <th className="px-4 py-3">Company</th>
                <th className="px-4 py-3">Title</th>
                <th className="px-4 py-3">Location</th>
                <th className="px-4 py-3">Seen</th>
                <th className="px-4 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-stone-200">
              {jobs.map((job) => (
                <tr key={job.id}>
                  <td className="px-4 py-3 font-semibold">{job.company_name}</td>
                  <td className="px-4 py-3">
                    <a href={job.apply_url} className="text-[var(--accent)]">
                      {job.title_normalized}
                    </a>
                  </td>
                  <td className="px-4 py-3 text-stone-700">{job.location_normalized ?? "Unknown"}</td>
                  <td className="px-4 py-3 text-stone-600">{formatDate(job.first_seen_at)}</td>
                  <td className="px-4 py-3">
                    <StatusPill label={job.status} tone={job.status === "active" ? "good" : "neutral"} />
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
