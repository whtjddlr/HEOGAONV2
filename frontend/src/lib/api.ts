import type { ApiEnvelope, TurnInput } from "@/types/flow";

const API_BASE_URL = (process.env.NEXT_PUBLIC_HEOGAON_API_BASE_URL || "http://127.0.0.1:4100").replace(/\/$/, "");

export async function startCase(text: string): Promise<ApiEnvelope> {
  return send("/api/cases", { type: "natural_language", text });
}

export async function sendTurn(caseId: string, input: TurnInput): Promise<ApiEnvelope> {
  return send(`/api/cases/${caseId}/turns`, input);
}

async function send(path: string, input: TurnInput): Promise<ApiEnvelope> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `API ${response.status}`);
  }

  return response.json() as Promise<ApiEnvelope>;
}
