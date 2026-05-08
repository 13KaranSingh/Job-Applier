import { NextResponse } from "next/server";
import { API_BASE_URL } from "../../../../lib/api";

export async function PUT(request: Request, { params }: { params: Promise<{ sourceId: string }> }) {
  const { sourceId } = await params;
  const body = await request.json();
  const response = await fetch(`${API_BASE_URL}/sources/${sourceId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const payload = await response.json();
  return NextResponse.json(payload, { status: response.status });
}

