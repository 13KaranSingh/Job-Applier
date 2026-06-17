const exports = ["TopJobs.csv", "JobFeed.csv", "Applications.csv", "Failures.csv", "DailyStats.csv"];

export function ExportLinks() {
  return (
    <div className="flex flex-wrap gap-2">
      {exports.map((fileName) => (
        <a
          key={fileName}
          href={`/api/exports/${fileName}`}
          className="rounded-md border border-stone-300 bg-white px-3 py-1.5 text-xs font-semibold text-stone-700 hover:bg-stone-100"
        >
          {fileName}
        </a>
      ))}
    </div>
  );
}
