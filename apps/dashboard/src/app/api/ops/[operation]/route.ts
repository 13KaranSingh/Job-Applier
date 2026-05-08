import { NextResponse } from "next/server";
import { API_BASE_URL } from "../../../../lib/api";

export async function POST(_request: Request, { params }: { params: Promise<{ operation: string }> }) {
  const { operation } = await params;
  const response = await fetch(`${API_BASE_URL}/ops/${operation}`, { method: "POST" });
  const payload = await response.json();
  return NextResponse.json(payload, { status: response.status });
}
