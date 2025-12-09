'use client';

import { useState } from 'react';
import { MediaContext, MediaPlanRow, MediaPlanUploader } from '../components/MediaPlanUploader';

type FeedRow = {
  Unique_ID: string;
  Headline: string;
  Image_URL: string;
  Exit_URL: string;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Simple demo stubs so the page is usable before full wiring from the main app.
const DEMO_AUDIENCE_STRATEGY = [
  { audience: 'Prospects', headline: 'Discover Aurora’s “Night Reset” ritual.' },
  { audience: 'Trialists', headline: 'Turn your first week into a new sleep habit.' },
];

const DEMO_ASSET_LIST = [
  {
    audience: 'Prospects',
    image_url: 'https://example.com/night-reset.jpg',
    exit_url: 'https://example.com/night-reset',
  },
  {
    audience: 'Trialists',
    image_url: 'https://example.com/trialist.jpg',
    exit_url: 'https://example.com/trialist',
  },
];

const DEMO_MEDIA_PLAN_ROWS: MediaPlanRow[] = [
  { 'Placement ID': 'PL-001', 'Target Audience': 'Prospects' },
  { 'Placement ID': 'PL-002', 'Target Audience': 'Trialists' },
];

export default function FeedReviewPage() {
  const [mediaContext, setMediaContext] = useState<MediaContext | null>(null);
  const [feed, setFeed] = useState<FeedRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mediaRows = mediaContext?.rows?.length ? mediaContext.rows : DEMO_MEDIA_PLAN_ROWS;

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API_BASE_URL}/generate-feed`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          audience_strategy: DEMO_AUDIENCE_STRATEGY,
          asset_list: DEMO_ASSET_LIST,
          media_plan_rows: mediaRows,
        }),
      });

      if (!res.ok) {
        const detail = await res.text();
        throw new Error(detail || `Failed with status ${res.status}`);
      }

      const data = await res.json();
      setFeed(data.feed || []);
    } catch (e: any) {
      setError(e?.message ?? 'Unable to generate feed.');
    } finally {
      setLoading(false);
    }
  };

  const handleExportCsv = () => {
    if (!feed.length) return;
    const headers = ['Unique_ID', 'Headline', 'Image_URL', 'Exit_URL'];
    const rows = feed.map((r) => headers.map((h) => (r as any)[h] ?? '').join(','));
    const csv = [headers.join(','), ...rows].join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'dco_feed.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleExportBrief = async () => {
    if (!feed.length) return;

    try {
      const res = await fetch(`${API_BASE_URL}/export/pdf`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          plan: {
            campaign_name: 'DCO Feed – Production Brief',
            bill_of_materials: feed.map((row) => ({
              asset_id: row.Unique_ID,
              concept: row.Headline,
              format: 'Dynamic creative',
            })),
          },
        }),
      });
      if (!res.ok) {
        const detail = await res.text();
        throw new Error(detail || `Failed with status ${res.status}`);
      }
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'dco_production_brief.pdf';
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50">
      <div className="max-w-6xl mx-auto py-10 px-4 space-y-8">
        <header className="flex items-center justify-between gap-4">
          <div>
            <h1 className="text-lg font-semibold text-slate-900">DCO Feed Review</h1>
            <p className="text-sm text-slate-500">
              Inspect the generated dynamic creative feed before handing it off to production.
            </p>
          </div>
        </header>

        {/* Media plan ingestor */}
        <section className="space-y-3">
          <h2 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Media Plan Context
          </h2>
          <p className="text-[11px] text-slate-500 max-w-xl">
            Upload a media plan CSV to override the demo rows. Audience + placement
            information becomes the container for the DCO feed.
          </p>
          <div className="border border-slate-200 rounded-xl bg-white p-4">
            <MediaPlanUploader onMediaContextChange={setMediaContext} />
          </div>
        </section>

        {/* Controls */}
        <section className="flex flex-wrap items-center gap-3">
          <button
            onClick={handleGenerate}
            disabled={loading}
            className="px-4 py-2 text-xs font-semibold rounded-full bg-teal-600 text-white hover:bg-teal-700 disabled:opacity-60"
          >
            {loading ? 'Generating…' : 'Generate DCO Feed'}
          </button>
          <button
            onClick={handleExportCsv}
            disabled={!feed.length}
            className="px-4 py-2 text-xs font-semibold rounded-full border border-slate-300 text-slate-700 bg-white disabled:opacity-50"
          >
            Export to CSV
          </button>
          <button
            onClick={handleExportBrief}
            disabled={!feed.length}
            className="px-4 py-2 text-xs font-semibold rounded-full border border-slate-300 text-slate-700 bg-white disabled:opacity-50"
          >
            Export Production Brief (PDF)
          </button>
          {error && <p className="text-[11px] text-red-500">{error}</p>}
        </section>

        {/* Feed table */}
        <section className="border border-slate-200 rounded-xl bg-white overflow-hidden">
          <div className="border-b border-slate-200 bg-slate-50 px-4 py-2">
            <p className="text-[11px] text-slate-500">
              {feed.length
                ? `Showing ${feed.length} rows in the generated feed.`
                : 'No feed generated yet. Run "Generate DCO Feed" to see results.'}
            </p>
          </div>
          <div className="max-h-[480px] overflow-auto">
            <table className="min-w-full text-[11px]">
              <thead className="bg-slate-50 sticky top-0 z-10">
                <tr>
                  <th className="text-left px-3 py-2 font-semibold text-slate-600 border-b border-slate-200">
                    Unique ID
                  </th>
                  <th className="text-left px-3 py-2 font-semibold text-slate-600 border-b border-slate-200">
                    Headline
                  </th>
                  <th className="text-left px-3 py-2 font-semibold text-slate-600 border-b border-slate-200">
                    Image URL
                  </th>
                  <th className="text-left px-3 py-2 font-semibold text-slate-600 border-b border-slate-200">
                    Exit URL
                  </th>
                </tr>
              </thead>
              <tbody>
                {feed.map((row) => (
                  <tr key={row.Unique_ID} className="odd:bg-white even:bg-slate-50/40">
                    <td className="px-3 py-2 border-b border-slate-100 font-mono text-slate-700">
                      {row.Unique_ID}
                    </td>
                    <td className="px-3 py-2 border-b border-slate-100 text-slate-700">
                      {row.Headline}
                    </td>
                    <td className="px-3 py-2 border-b border-slate-100 text-slate-500">
                      {row.Image_URL}
                    </td>
                    <td className="px-3 py-2 border-b border-slate-100 text-slate-500">
                      {row.Exit_URL}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </main>
  );
}


