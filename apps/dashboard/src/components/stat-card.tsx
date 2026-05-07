export function StatCard({
  label,
  value,
  tone = "default",
}: {
  label: string;
  value: string;
  tone?: "default" | "accent";
}) {
  return (
    <div className="rounded-lg border border-black/5 bg-white/80 p-5 shadow-sm backdrop-blur">
      <p className="text-xs uppercase tracking-[0.25em] text-stone-500">{label}</p>
      <p className={tone === "accent" ? "mt-3 text-3xl font-semibold text-[var(--accent)]" : "mt-3 text-3xl font-semibold"}>
        {value}
      </p>
    </div>
  );
}
