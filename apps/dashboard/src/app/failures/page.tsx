import { LayoutShell } from "../../components/layout-shell";
import { EmptyState } from "../../components/empty-state";
import { StatusPill } from "../../components/status-pill";
import { getApplications } from "../../lib/api";

export const dynamic = "force-dynamic";

export default async function FailuresPage() {
  const failures = (await getApplications()).filter((application) => application.status.startsWith("FAILED"));

  return (
    <LayoutShell title="Failures" actions={<StatusPill label={`${failures.length} failures`} tone={failures.length > 0 ? "warn" : "good"} />}>
      {failures.length === 0 ? (
        <EmptyState label="No failed applications recorded." />
      ) : (
        <div className="overflow-hidden rounded-lg border border-black/5 bg-white/85 shadow-sm">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-stone-200 bg-stone-50 text-xs uppercase text-stone-500">
              <tr>
                <th className="px-4 py-3">Application</th>
                <th className="px-4 py-3">Role</th>
                <th className="px-4 py-3">Mode</th>
                <th className="px-4 py-3">Resume</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Failure</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-stone-200">
              {failures.map((failure) => (
                <tr key={failure.id}>
                  <td className="px-4 py-3 font-mono text-xs">{failure.id}</td>
                  <td className="px-4 py-3">
                    <p className="font-semibold">{failure.company_name}</p>
                    <a href={failure.apply_url} className="text-xs text-[var(--accent)]">
                      {failure.title_normalized}
                    </a>
                  </td>
                  <td className="px-4 py-3">{failure.application_mode}</td>
                  <td className="px-4 py-3">{failure.resume_variant}</td>
                  <td className="px-4 py-3">
                    <StatusPill label={failure.status} tone="warn" />
                  </td>
                  <td className="px-4 py-3 text-xs text-stone-600">
                    {failure.failure_stage ?? failure.failure_code ?? "Unknown"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </LayoutShell>
  );
}
