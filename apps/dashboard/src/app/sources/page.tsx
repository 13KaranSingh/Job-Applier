import { LayoutShell } from "../../components/layout-shell";
import { ActionButton } from "../../components/action-button";
import { SourceConfigForm } from "../../components/source-config-form";
import { SourceCreateForm } from "../../components/source-create-form";
import { StatusPill } from "../../components/status-pill";
import { getSources } from "../../lib/api";

export const dynamic = "force-dynamic";

export default async function SourcesPage() {
  const sources = await getSources();

  return (
    <LayoutShell title="Sources" actions={<StatusPill label={`${sources.length} configured`} />}>
      <SourceCreateForm />
      <div className="overflow-hidden rounded-lg border border-black/5 bg-white/85 shadow-sm">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-stone-200 bg-stone-50 text-xs uppercase text-stone-500">
            <tr>
              <th className="px-4 py-3">Source</th>
              <th className="px-4 py-3">Type</th>
              <th className="px-4 py-3">Polling</th>
              <th className="px-4 py-3">Priority</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Config</th>
              <th className="px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-stone-200">
            {sources.map((source) => (
              <tr key={source.id}>
                <td className="px-4 py-3">
                  <p className="font-semibold">{source.name}</p>
                  <p className="text-xs text-stone-500">{source.slug}</p>
                </td>
                <td className="px-4 py-3 text-stone-700">{source.source_type}</td>
                <td className="px-4 py-3 text-stone-700">{Math.round(source.polling_interval_seconds / 60)} min</td>
                <td className="px-4 py-3 text-stone-700">{source.priority_weight}</td>
                <td className="px-4 py-3">
                  <StatusPill label={source.enabled ? "enabled" : "disabled"} tone={source.enabled ? "good" : "neutral"} />
                </td>
                <td className="px-4 py-3">
                  <SourceConfigForm source={source} />
                </td>
                <td className="px-4 py-3">
                  <ActionButton
                    label={source.enabled ? "Disable" : "Enable"}
                    endpoint={`/api/sources/${source.id}/toggle`}
                    body={{ enabled: !source.enabled }}
                    tone={source.enabled ? "danger" : "accent"}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </LayoutShell>
  );
}
