import { NextResponse } from "next/server";
import { API_BASE_URL } from "../../../../../lib/api";

export async function POST(_request: Request, { params }: { params: Promise<{ applicationId: string }> }) {
  const { applicationId } = await params;
  const response = await fetch(`${API_BASE_URL}/applications/${applicationId}/retry`, { method: "POST" });
  const payload = await response.json();
  return NextResponse.json(payload, { status: response.status });
}

