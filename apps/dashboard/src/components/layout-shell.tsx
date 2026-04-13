import Link from "next/link";
import { ReactNode } from "react";

const navItems = [
  ["Overview", "/"],
  ["Top Jobs", "/top-jobs"],
  ["All Jobs", "/jobs"],
  ["Applications", "/applications"],
  ["Failures", "/failures"],
  ["Sources", "/sources"],
  ["Analytics", "/analytics"],
  ["Settings", "/settings"],
  ["Profile", "/profile"],
];

export function LayoutShell({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  return (
    <div className="mx-auto flex min-h-screen max-w-7xl gap-6 px-4 py-6 md:px-8">
      <aside className="hidden w-64 shrink-0 rounded-3xl border border-black/5 bg-white/60 p-5 shadow-lg backdrop-blur md:block">
        <div className="mb-6">
          <p className="text-xs uppercase tracking-[0.3em] text-stone-500">Job Bot</p>
          <h1 className="font-serif text-2xl">Operator Console</h1>
        </div>
        <nav className="space-y-2">
          {navItems.map(([label, href]) => (
            <Link key={href} href={href} className="block rounded-2xl px-3 py-2 text-sm text-stone-700 transition hover:bg-stone-900 hover:text-white">
              {label}
            </Link>
          ))}
        </nav>
      </aside>
      <main className="flex-1">
        <header className="mb-6 rounded-3xl border border-black/5 bg-[var(--panel)] p-6 shadow-lg backdrop-blur">
          <p className="text-xs uppercase tracking-[0.25em] text-[var(--accent)]">Automation Platform</p>
          <h2 className="font-serif text-4xl">{title}</h2>
        </header>
        {children}
      </main>
    </div>
  );
}

