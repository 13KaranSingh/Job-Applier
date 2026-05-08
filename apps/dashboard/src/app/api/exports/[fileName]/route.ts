import { readFile } from "node:fs/promises";
import { basename, join } from "node:path";

import { NextResponse } from "next/server";

const allowedFiles = new Set(["Applications.csv", "Failures.csv", "JobFeed.csv", "TopJobs.csv"]);

export async function GET(_request: Request, { params }: { params: Promise<{ fileName: string }> }) {
  const { fileName } = await params;
  const safeName = basename(fileName);
  if (!allowedFiles.has(safeName)) {
    return NextResponse.json({ error: "Unknown export" }, { status: 404 });
  }
  const filePath = join(process.cwd(), "..", "..", "storage", "exports", safeName);
  const content = await readFile(filePath, "utf8").catch(() => "");
  return new Response(content, {
    headers: {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": `attachment; filename="${safeName}"`,
    },
  });
}

