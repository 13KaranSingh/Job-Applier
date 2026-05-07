import { LayoutShell } from "../../components/layout-shell";
import { StatusPill } from "../../components/status-pill";
import { getProfile } from "../../lib/api";

export const dynamic = "force-dynamic";

export default async function ProfilePage() {
  const { profile } = await getProfile();

  return (
    <LayoutShell title="Profile & Answers" actions={<StatusPill label={profile ? "profile loaded" : "missing profile"} tone={profile ? "good" : "warn"} />}>
      {profile ? (
        <div className="grid gap-4 lg:grid-cols-[1fr_1fr]">
          <section className="rounded-lg border border-black/5 bg-white/85 p-5 shadow-sm">
            <h3 className="font-serif text-2xl">{String(profile.full_name ?? "Candidate")}</h3>
            <dl className="mt-4 grid gap-3 text-sm">
              <div className="flex justify-between border-b border-stone-200 pb-2">
                <dt className="text-stone-500">School</dt>
                <dd className="font-medium">{String(profile.school_name ?? "Unknown")}</dd>
              </div>
              <div className="flex justify-between border-b border-stone-200 pb-2">
                <dt className="text-stone-500">Degree</dt>
                <dd className="font-medium text-right">{String(profile.degree ?? "Unknown")}</dd>
              </div>
              <div className="flex justify-between border-b border-stone-200 pb-2">
                <dt className="text-stone-500">Graduation</dt>
                <dd className="font-medium">
                  {String(profile.graduation_month ?? "")} {String(profile.graduation_year ?? "")}
                </dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-stone-500">Work Auth</dt>
                <dd className="font-medium">{String(profile.work_authorization ?? "Unknown")}</dd>
              </div>
            </dl>
          </section>
          <section className="rounded-lg border border-black/5 bg-white/85 p-5 shadow-sm">
            <h3 className="font-serif text-2xl">Skills</h3>
            <div className="mt-4 flex flex-wrap gap-2">
              {Array.isArray(profile.skill_inventory) &&
                profile.skill_inventory.map((skill) => (
                  <StatusPill key={String(skill)} label={String(skill)} />
                ))}
            </div>
          </section>
        </div>
      ) : (
        <div className="rounded-lg border border-dashed border-stone-300 bg-white/70 p-8 text-center text-sm text-stone-500">
          Seed the local profile to populate this page.
        </div>
      )}
    </LayoutShell>
  );
}
