"use client";

import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";

import type { SourceItem } from "../lib/api";

export function SourceConfigForm({ source }: { source: SourceItem }) {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const [boardToken, setBoardToken] = useState(String(source.config_json.board_token ?? ""));
  const [companySlug, setCompanySlug] = useState(String(source.config_json.company_slug ?? ""));
  const [companyName, setCompanyName] = useState(String(source.config_json.company_name ?? ""));
  const [careerUrl, setCareerUrl] = useState(String(source.config_json.career_url ?? ""));
  const [atsType, setAtsType] = useState(String(source.config_json.ats_type ?? ""));

  return (
    <div className="grid gap-2">
      <input
        value={boardToken}
        onChange={(event) => setBoardToken(event.target.value)}
        placeholder="Board token / ATS token"
        className="w-full rounded-md border border-stone-300 bg-white px-2 py-1.5 text-xs"
      />
      <input
        value={companySlug}
        onChange={(event) => setCompanySlug(event.target.value)}
        placeholder="Lever company slug"
        className="w-full rounded-md border border-stone-300 bg-white px-2 py-1.5 text-xs"
      />
      <input
        value={atsType}
        onChange={(event) => setAtsType(event.target.value)}
        placeholder="ATS type"
        className="w-full rounded-md border border-stone-300 bg-white px-2 py-1.5 text-xs"
      />
      <input
        value={companyName}
        onChange={(event) => setCompanyName(event.target.value)}
        placeholder="Company display name"
        className="w-full rounded-md border border-stone-300 bg-white px-2 py-1.5 text-xs"
      />
      <input
        value={careerUrl}
        onChange={(event) => setCareerUrl(event.target.value)}
        placeholder="Careers URL"
        className="w-full rounded-md border border-stone-300 bg-white px-2 py-1.5 text-xs"
      />
      <button
        type="button"
        disabled={isPending}
        onClick={() => {
          startTransition(async () => {
            await fetch(`/api/sources/${source.id}`, {
              method: "PUT",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                board_token: boardToken,
                company_slug: companySlug,
                company_name: companyName,
                career_url: careerUrl,
                ats_type: atsType,
              }),
            });
            router.refresh();
          });
        }}
        className="rounded-md border border-stone-300 bg-white px-3 py-1.5 text-xs font-semibold text-stone-700 hover:bg-stone-100 disabled:cursor-wait disabled:opacity-60"
      >
        {isPending ? "Saving" : "Save config"}
      </button>
    </div>
  );
}
