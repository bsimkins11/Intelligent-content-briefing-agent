import { NextRequest, NextResponse } from 'next/server';

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const OPENAI_MODEL = process.env.OPENAI_MODEL || 'gpt-4.1-mini';

const GEMINI_API_KEY = process.env.GOOGLE_API_KEY;
const GEMINI_MODEL = process.env.GEMINI_MODEL || 'models/gemini-2.5-pro';

type ScoreResponse = {
  quality_score: number;
  gaps: string[];
  rationale: string;
};

export async function POST(req: NextRequest) {
  if (!OPENAI_API_KEY && !GEMINI_API_KEY) {
    return NextResponse.json(
      { detail: 'No model API key set. Provide OPENAI_API_KEY (recommended) or GOOGLE_API_KEY.' },
      { status: 500 },
    );
  }

  try {
    const body = await req.json();
    const current_state = body?.current_state ?? {};

    const systemPrompt = `
You are a world-class Executive Creative Director and ModCon (modular content) strategy lead.
Score the brief for production readiness AND creative excellence.

Rubric (0-10):
- 0-3: missing fundamentals; vague; not actionable.
- 4-6: usable but generic; unclear audience insight; weak SMP; limited modularity.
- 7-8: strong strategy; clear brief; modular thinking; mostly production-ready.
- 9-10: exceptional: sharp SMP, concrete audiences/insight, clear mandatories/guardrails, proof/offer, channel-fit, and modular system thinking.

Return ONLY valid JSON with this exact shape:
{
  "quality_score": 0-10 (number, can be decimal),
  "gaps": ["Gap 1", "Gap 2", "Gap 3"], // max 3, most important missing items
  "rationale": "1-2 sentences explaining the score and what to improve next."
}
`;

    // Prefer OpenAI for demo deployments.
    if (OPENAI_API_KEY) {
      const resp = await fetch('https://api.openai.com/v1/responses', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${OPENAI_API_KEY}`,
        },
        body: JSON.stringify({
          model: OPENAI_MODEL,
          temperature: 0.2,
          input: [
            { role: 'system', content: systemPrompt.trim() },
            { role: 'user', content: `Brief JSON:\n${JSON.stringify(current_state)}` },
          ],
        }),
      });

      if (!resp.ok) {
        const errText = await resp.text();
        return NextResponse.json({ detail: errText }, { status: resp.status });
      }

      const data: any = await resp.json();
      const text =
        (typeof data?.output_text === 'string' && data.output_text) ||
        data?.output?.[0]?.content?.map((c: any) => c?.text).filter(Boolean).join(' ') ||
        '';

      const parsed = JSON.parse(text) as ScoreResponse;
      return NextResponse.json(parsed);
    }

    // Gemini fallback
    const geminiPayload = {
      systemInstruction: { parts: [{ text: systemPrompt.trim() }] },
      contents: [
        {
          role: 'user',
          parts: [{ text: `Brief JSON:\n${JSON.stringify(current_state)}` }],
        },
      ],
    };

    const resp = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${GEMINI_API_KEY}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(geminiPayload),
      },
    );

    if (!resp.ok) {
      const errText = await resp.text();
      return NextResponse.json({ detail: errText }, { status: resp.status });
    }

    const data: any = await resp.json();
    const text =
      data?.candidates?.[0]?.content?.parts?.map((p: any) => p.text).join(' ') || '';

    const parsed = JSON.parse(text) as ScoreResponse;
    return NextResponse.json(parsed);
  } catch (err: any) {
    return NextResponse.json({ detail: err?.message || 'Unknown error' }, { status: 500 });
  }
}


