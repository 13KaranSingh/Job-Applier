"use client";

import { useRouter } from "next/navigation";
import { useTransition } from "react";

export function ActionButton({
  label,
  endpoint,
  body,
  tone = "neutral",
}: {
  label: string;
  endpoint: string;
  body?: Record<string, unknown>;
  tone?: "neutral" | "accent" | "danger";
}) {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const toneClass =
    tone === "accent"
      ? "border-[var(--accent)] bg-[var(--accent)] text-white hover:bg-white hover:text-[var(--accent)]"
      : tone === "danger"
        ? "border-red-300 bg-red-50 text-red-700 hover:bg-red-100"
        : "border-stone-300 bg-white text-stone-700 hover:bg-stone-100";

  return (
    <button
      type="button"
      disabled={isPending}
      onClick={() => {
        startTransition(async () => {
          await fetch(endpoint, {
            method: "POST",
            headers: body ? { "Content-Type": "application/json" } : undefined,
            body: body ? JSON.stringify(body) : undefined,
          });
          router.refresh();
        });
      }}
      className={`rounded-md border px-3 py-1.5 text-xs font-semibold transition disabled:cursor-wait disabled:opacity-60 ${toneClass}`}
    >
      {isPending ? "Working" : label}
    </button>
  );
}
