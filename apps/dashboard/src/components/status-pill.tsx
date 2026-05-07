export function StatusPill({
  label,
  tone = "neutral",
}: {
  label: string;
  tone?: "neutral" | "good" | "warn";
}) {
  const className =
    tone === "good"
      ? "border-emerald-200 bg-emerald-50 text-emerald-800"
      : tone === "warn"
        ? "border-amber-200 bg-amber-50 text-amber-800"
        : "border-stone-200 bg-stone-50 text-stone-700";

  return (
    <span className={`inline-flex items-center rounded-full border px-2 py-1 text-xs font-medium ${className}`}>
      {label}
    </span>
  );
}

