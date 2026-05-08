"use client";

import { ActionButton } from "./action-button";

const actions = [
  { label: "Full Refresh", operation: "full-refresh", tone: "accent" as const },
  { label: "Poll Sources", operation: "poll", tone: "neutral" as const },
  { label: "Rank Jobs", operation: "rank", tone: "neutral" as const },
  { label: "Export CSV", operation: "export-csv", tone: "neutral" as const },
  { label: "Send Alerts", operation: "send-alerts", tone: "danger" as const },
];

export function PipelineActions() {
  return (
    <div className="flex flex-wrap gap-2">
      {actions.map((action) => (
        <ActionButton
          key={action.operation}
          label={action.label}
          endpoint={`/api/ops/${action.operation}`}
          tone={action.tone}
        />
      ))}
    </div>
  );
}
