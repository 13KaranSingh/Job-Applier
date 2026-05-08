"use client";

import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";

function slugify(value: string) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

export function SourceCreateForm() {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const [name, setName] = useState("");
  const [sourceType, setSourceType] = useState("company");
  const [boardToken, setBoardToken] = useState("");
  const [companySlug, setCompanySlug] = useState("");

  return (
    <section className="mb-4 rounded-lg border border-black/5 bg-white/85 p-4 shadow-sm">
      <h3 className="font-serif text-xl">Add Live Source</h3>
      <div className="mt-3 grid gap-3 md:grid-cols-[1fr_160px_1fr_1fr_120px]">
        <input value={name} onChange={(event) => setName(event.target.value)} placeholder="Company name" className="rounded-md border border-stone-300 bg-white px-3 py-2 text-sm" />
        <select value={sourceType} onChange={(event) => setSourceType(event.target.value)} className="rounded-md border border-stone-300 bg-white px-3 py-2 text-sm">
          <option value="company">Company</option>
          <option value="ats">ATS</option>
          <option value="feed">Feed</option>
        </select>
        <input value={boardToken} onChange={(event) => setBoardToken(event.target.value)} placeholder="Greenhouse token" className="rounded-md border border-stone-300 bg-white px-3 py-2 text-sm" />
        <input value={companySlug} onChange={(event) => setCompanySlug(event.target.value)} placeholder="Lever slug" className="rounded-md border border-stone-300 bg-white px-3 py-2 text-sm" />
        <button
          type="button"
          disabled={isPending || !name}
          onClick={() => {
            startTransition(async () => {
              await fetch("/api/sources", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                  name,
                  slug: slugify(name),
                  source_type: sourceType,
                  polling_interval_seconds: 300,
                  priority_weight: 8,
                  config_json: {
                    company_name: name,
                    board_token: boardToken,
                    company_slug: companySlug,
                  },
                }),
              });
              setName("");
              setBoardToken("");
              setCompanySlug("");
              router.refresh();
            });
          }}
          className="rounded-md border border-[var(--accent)] bg-[var(--accent)] px-3 py-2 text-sm font-semibold text-white hover:bg-white hover:text-[var(--accent)] disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isPending ? "Adding" : "Add"}
        </button>
      </div>
    </section>
  );
}
