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
  actions,
  children,
}: {
  title: string;
  actions?: ReactNode;
  children: ReactNode;
}) {
  return (
    <div className="mx-auto flex min-h-screen max-w-7xl gap-6 px-4 py-6 md:px-8">
      <aside className="hidden w-64 shrink-0 rounded-lg border border-black/5 bg-white/70 p-5 shadow-sm backdrop-blur md:block">
        <div className="mb-6">
          <p className="text-xs uppercase tracking-[0.3em] text-stone-500">Job Bot</p>
          <h1 className="font-serif text-2xl">Operator Console</h1>
        </div>
        <nav className="space-y-2">
          {navItems.map(([label, href]) => (
            <Link key={href} href={href} className="block rounded-md px-3 py-2 text-sm text-stone-700 transition hover:bg-stone-900 hover:text-white">
              {label}
            </Link>
          ))}
        </nav>
      </aside>
      <main className="flex-1">
        <header className="mb-6 flex flex-col gap-4 border-b border-black/10 pb-5 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-[var(--accent)]">Automation Platform</p>
            <h2 className="font-serif text-4xl">{title}</h2>
          </div>
          {actions}
        </header>
        {children}
      </main>
    </div>
  );
}
