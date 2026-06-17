import { LayoutShell } from "../../components/layout-shell";
import { ActionButton } from "../../components/action-button";
import { EmptyState } from "../../components/empty-state";
import { StatusPill } from "../../components/status-pill";
import { formatDate, getApplications } from "../../lib/api";

export const dynamic = "force-dynamic";

export default async function ApplicationsPage() {
  const applications = await getApplications();

  return (
    <LayoutShell title="Applications" actions={<StatusPill label={`${applications.length} records`} />}>
      <div className="overflow-hidden rounded-lg border border-black/5 bg-white/85 shadow-sm">
        {applications.length === 0 ? (
          <EmptyState label="No applications have been created yet." />
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="border-b border-stone-200 bg-stone-50 text-xs uppercase text-stone-500">
              <tr>
                <th className="px-4 py-3">Application</th>
                <th className="px-4 py-3">Role</th>
                <th className="px-4 py-3">Mode</th>
                <th className="px-4 py-3">Resume</th>
                <th className="px-4 py-3">Submitted</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-stone-200">
              {applications.map((application) => (
                <tr key={application.id}>
                  <td className="px-4 py-3 font-mono text-xs">{application.id}</td>
                  <td className="px-4 py-3">
                    <p className="font-semibold">{application.company_name}</p>
                    <a href={application.apply_url} className="text-xs text-[var(--accent)]">
                      {application.title_normalized}
                    </a>
                  </td>
                  <td className="px-4 py-3">{application.application_mode}</td>
                  <td className="px-4 py-3">{application.resume_variant}</td>
                  <td className="px-4 py-3">{formatDate(application.submitted_at)}</td>
                  <td className="px-4 py-3">
                    <StatusPill label={application.status} tone={application.status === "CONFIRMED" ? "good" : "neutral"} />
                  </td>
                  <td className="px-4 py-3">
                    <ActionButton label="Retry" endpoint={`/api/applications/${application.id}/retry`} />
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
