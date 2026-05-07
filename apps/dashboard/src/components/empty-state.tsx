export function EmptyState({ label }: { label: string }) {
  return (
    <div className="rounded-lg border border-dashed border-stone-300 bg-white/60 px-4 py-8 text-center text-sm text-stone-500">
      {label}
    </div>
  );
}

