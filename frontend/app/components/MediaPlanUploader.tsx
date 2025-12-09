'use client';

import { useState, ChangeEvent } from 'react';

export type MediaPlanRow = Record<string, string>;

export type MediaContext = {
  headers: string[];
  rows: MediaPlanRow[];
};

type MediaPlanUploaderProps = {
  onMediaContextChange: (context: MediaContext) => void;
};

function parseCsv(text: string): MediaContext {
  const lines = text
    .split(/\r?\n/)
    .map((l) => l.trimEnd())
    .filter((l) => l.length > 0);

  if (lines.length === 0) {
    return { headers: [], rows: [] };
  }

  const rawHeaders = lines[0].split(',').map((h) => h.trim());
  const headers = rawHeaders.map((h, idx) => h || `col_${idx}`);

  const rows: MediaPlanRow[] = [];

  for (let i = 1; i < lines.length; i++) {
    const cells = lines[i].split(',');
    const row: MediaPlanRow = {};
    cells.forEach((value, idx) => {
      const key = headers[idx] ?? `col_${idx}`;
      row[key] = value.trim();
    });
    // Skip completely empty rows
    if (Object.values(row).some((v) => v && v.length > 0)) {
      rows.push(row);
    }
  }

  return { headers, rows };
}

export function MediaPlanUploader({ onMediaContextChange }: MediaPlanUploaderProps) {
  const [fileName, setFileName] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setError(null);
    setFileName(file.name);

    try {
      const text = await file.text();
      const context = parseCsv(text);
      onMediaContextChange(context);
    } catch (e: any) {
      setError(e?.message ?? 'Unable to read CSV file.');
    }
  };

  return (
    <div className="border border-slate-200 rounded-xl p-4 bg-slate-50/60">
      <div className="flex items-center justify-between gap-2 mb-2">
        <div>
          <h3 className="text-xs font-semibold text-slate-700 uppercase tracking-wider">
            Media Plan Ingestor
          </h3>
          <p className="text-[11px] text-slate-500">
            Upload a media plan CSV to create the Media Context container for DCO feeds.
          </p>
        </div>
      </div>
      <label className="inline-flex items-center gap-2 text-xs font-medium px-3 py-2 rounded-full border border-dashed border-teal-400 text-teal-700 bg-teal-50 hover:bg-teal-100 cursor-pointer">
        <span>Upload media plan (.csv)</span>
        <input type="file" accept=".csv,text/csv" className="hidden" onChange={handleFileChange} />
      </label>
      {fileName && (
        <p className="mt-2 text-[11px] text-slate-500">
          Loaded: <span className="font-mono text-slate-700">{fileName}</span>
        </p>
      )}
      {error && <p className="mt-2 text-[11px] text-red-500">{error}</p>}
    </div>
  );
}


