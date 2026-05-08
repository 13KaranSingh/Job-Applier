import { LayoutShell } from "../../components/layout-shell";
import { StatusPill } from "../../components/status-pill";
import { getAnswers, getProfile, getResumes } from "../../lib/api";

export const dynamic = "force-dynamic";

export default async function ProfilePage() {
  const [{ profile }, answers, resumes] = await Promise.all([getProfile(), getAnswers(), getResumes()]);

  return (
    <LayoutShell title="Profile & Answers" actions={<StatusPill label={profile ? "profile loaded" : "missing profile"} tone={profile ? "good" : "warn"} />}>
      {profile ? (
        <div className="grid gap-4">
          <div className="grid gap-4 lg:grid-cols-[1fr_1fr]">
          <section className="rounded-lg border border-black/5 bg-white/85 p-5 shadow-sm">
            <h3 className="font-serif text-2xl">{String(profile.full_name ?? "Candidate")}</h3>
            <dl className="mt-4 grid gap-3 text-sm">
              <div className="flex justify-between border-b border-stone-200 pb-2">
                <dt className="text-stone-500">Email</dt>
                <dd className="font-medium">{String(profile.email ?? "Unknown")}</dd>
              </div>
              <div className="flex justify-between border-b border-stone-200 pb-2">
                <dt className="text-stone-500">Phone</dt>
                <dd className="font-medium">{String(profile.phone ?? "Unknown")}</dd>
              </div>
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
          <section className="rounded-lg border border-black/5 bg-white/85 p-5 shadow-sm">
            <div className="mb-4 flex items-center justify-between">
              <h3 className="font-serif text-2xl">Resume Assets</h3>
              <StatusPill label={`${resumes.length} variants`} />
            </div>
            <div className="overflow-hidden rounded-md border border-stone-200">
              <table className="w-full text-left text-sm">
                <thead className="bg-stone-50 text-xs uppercase text-stone-500">
                  <tr>
                    <th className="px-3 py-2">Variant</th>
                    <th className="px-3 py-2">Path</th>
                    <th className="px-3 py-2">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-stone-200">
                  {resumes.map((resume) => (
                    <tr key={resume.id}>
                      <td className="px-3 py-2 font-semibold">{resume.variant_name}</td>
                      <td className="px-3 py-2 font-mono text-xs text-stone-600">{resume.file_path}</td>
                      <td className="px-3 py-2">
                        <StatusPill label={resume.active ? "active" : "inactive"} tone={resume.active ? "good" : "neutral"} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
          <section className="rounded-lg border border-black/5 bg-white/85 p-5 shadow-sm">
            <div className="mb-4 flex items-center justify-between">
              <h3 className="font-serif text-2xl">Answer Library</h3>
              <StatusPill label={`${answers.length} answers`} />
            </div>
            <div className="grid gap-3 md:grid-cols-2">
              {answers.map((answer) => (
                <article key={answer.id} className="rounded-md border border-stone-200 bg-white p-3">
                  <div className="mb-2 flex items-center justify-between gap-2">
                    <p className="font-semibold">{answer.answer_key}</p>
                    <StatusPill label={answer.requires_human_review ? "review" : "auto"} tone={answer.requires_human_review ? "warn" : "good"} />
                  </div>
                  <p className="text-xs uppercase text-stone-500">{answer.category}</p>
                  <p className="mt-2 text-sm text-stone-700">{answer.answer_text}</p>
                </article>
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
