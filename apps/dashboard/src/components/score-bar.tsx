export function ScoreBar({ value }: { value: number }) {
  const width = Math.max(0, Math.min(100, value));

  return (
    <div className="min-w-28">
      <div className="mb-1 flex items-center justify-between text-xs text-stone-500">
        <span>Score</span>
        <span className="font-semibold text-stone-900">{value.toFixed(1)}</span>
      </div>
      <div className="h-2 rounded-full bg-stone-200">
        <div className="h-2 rounded-full bg-[var(--accent)]" style={{ width: `${width}%` }} />
      </div>
    </div>
  );
}

