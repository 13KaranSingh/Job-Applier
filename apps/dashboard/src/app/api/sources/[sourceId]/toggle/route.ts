import { NextResponse } from "next/server";
import { API_BASE_URL } from "../../../../../lib/api";

export async function POST(request: Request, { params }: { params: Promise<{ sourceId: string }> }) {
  const { sourceId } = await params;
  const body = await request.json().catch(() => ({ enabled: true }));
  const action = body.enabled ? "enable" : "disable";
  const response = await fetch(`${API_BASE_URL}/sources/${sourceId}/${action}`, { method: "POST" });
  const payload = await response.json();
  return NextResponse.json(payload, { status: response.status });
}

