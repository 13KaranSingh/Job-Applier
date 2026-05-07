import { LayoutShell } from "../../components/layout-shell";
import { StatusPill } from "../../components/status-pill";
import { getSources } from "../../lib/api";

export const dynamic = "force-dynamic";

export default async function SourcesPage() {
  const sources = await getSources();

  return (
    <LayoutShell title="Sources" actions={<StatusPill label={`${sources.length} configured`} />}>
      <div className="overflow-hidden rounded-lg border border-black/5 bg-white/85 shadow-sm">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-stone-200 bg-stone-50 text-xs uppercase text-stone-500">
            <tr>
              <th className="px-4 py-3">Source</th>
              <th className="px-4 py-3">Type</th>
              <th className="px-4 py-3">Polling</th>
              <th className="px-4 py-3">Priority</th>
              <th className="px-4 py-3">Status</th>
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
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </LayoutShell>
  );
}
