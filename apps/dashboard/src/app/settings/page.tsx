import { LayoutShell } from "../../components/layout-shell";
import { StatusPill } from "../../components/status-pill";

export const dynamic = "force-dynamic";

async function getSettings() {
  const response = await fetch("http://127.0.0.1:8000/settings", { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Settings API failed");
  }
  return response.json() as Promise<{ settings: Record<string, unknown> }>;
}

export default async function SettingsPage() {
  const { settings } = await getSettings();
  const mode = String(settings.mode ?? "unknown");

  return (
    <LayoutShell title="Settings" actions={<StatusPill label={mode} tone="good" />}>
      <pre className="overflow-auto rounded-lg border border-black/5 bg-stone-950 p-5 text-xs text-stone-100 shadow-sm">
        {JSON.stringify(settings, null, 2)}
      </pre>
    </LayoutShell>
  );
}
