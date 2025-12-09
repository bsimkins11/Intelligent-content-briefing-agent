'use client';

import { useState } from 'react';

type FeedRow = {
  row_id: string;
  creative_filename: string;
  reporting_label: string;
  is_default: boolean;
  asset_slot_a_path?: string | null;
  asset_slot_b_path?: string | null;
  asset_slot_c_path?: string | null;
  logo_asset_path?: string | null;
  copy_slot_a_text?: string | null;
  copy_slot_b_text?: string | null;
  copy_slot_c_text?: string | null;
  legal_disclaimer_text?: string | null;
  cta_button_text?: string | null;
  font_color_hex?: string | null;
  cta_bg_color_hex?: string | null;
  background_color_hex?: string | null;
  platform_id: string;
  placement_dimension: string;
  asset_format_type: string;
  audience_id?: string | null;
  geo_targeting?: string | null;
  date_start?: string | null;
  date_end?: string | null;
  trigger_condition?: string | null;
  destination_url?: string | null;
  utm_suffix?: string | null;
};

const FEED_COLUMNS: { key: keyof FeedRow; label: string; readOnly?: boolean }[] = [
  { key: 'row_id', label: 'Row ID', readOnly: true },
  { key: 'creative_filename', label: 'Creative Filename' },
  { key: 'reporting_label', label: 'Reporting Label' },
  { key: 'is_default', label: 'Is Default?' },
  { key: 'asset_slot_a_path', label: 'Asset Slot A (Primary)' },
  { key: 'asset_slot_b_path', label: 'Asset Slot B (Secondary)' },
  { key: 'asset_slot_c_path', label: 'Asset Slot C (Tertiary)' },
  { key: 'logo_asset_path', label: 'Logo Asset Path' },
  { key: 'copy_slot_a_text', label: 'Copy Slot A (Hook)' },
  { key: 'copy_slot_b_text', label: 'Copy Slot B (Support)' },
  { key: 'copy_slot_c_text', label: 'Copy Slot C (CTA)' },
  { key: 'legal_disclaimer_text', label: 'Legal Disclaimer' },
  { key: 'cta_button_text', label: 'CTA Button Text' },
  { key: 'font_color_hex', label: 'Font Color Hex' },
  { key: 'cta_bg_color_hex', label: 'CTA BG Color Hex' },
  { key: 'background_color_hex', label: 'Background Color Hex' },
  { key: 'platform_id', label: 'Platform ID' },
  { key: 'placement_dimension', label: 'Placement Dimension' },
  { key: 'asset_format_type', label: 'Asset Format Type' },
  { key: 'audience_id', label: 'Audience ID' },
  { key: 'geo_targeting', label: 'Geo Targeting' },
  { key: 'date_start', label: 'Date Start' },
  { key: 'date_end', label: 'Date End' },
  { key: 'trigger_condition', label: 'Trigger Condition' },
  { key: 'destination_url', label: 'Destination URL' },
  { key: 'utm_suffix', label: 'UTM Suffix' },
];

export default function FeedReviewPage() {
  const [feed, setFeed] = useState<FeedRow[]>([]);

  const updateFeedCell = (index: number, key: keyof FeedRow, value: string) => {
    setFeed((prev) =>
      prev.map((row, i) => (i === index ? { ...row, [key]: value } : row)),
    );
  };

  const setDefaultRow = (index: number) => {
    setFeed((prev) =>
      prev.map((row, i) => ({
        ...row,
        is_default: i === index,
      })),
    );
  };

  const addFeedRow = () => {
    setFeed((prev) => [
      ...prev,
      {
        row_id: crypto.randomUUID ? crypto.randomUUID() : `ROW-${Date.now()}-${prev.length + 1}`,
        creative_filename: '',
        reporting_label: '',
        is_default: prev.length === 0,
        asset_slot_a_path: '',
        asset_slot_b_path: '',
        asset_slot_c_path: '',
        logo_asset_path: '',
        copy_slot_a_text: '',
        copy_slot_b_text: '',
        copy_slot_c_text: '',
        legal_disclaimer_text: '',
        cta_button_text: 'Learn More',
        font_color_hex: '#FFFFFF',
        cta_bg_color_hex: '#14b8a6',
        background_color_hex: '#020617',
        platform_id: 'META',
        placement_dimension: '',
        asset_format_type: 'STATIC',
        audience_id: '',
        geo_targeting: '',
        date_start: '',
        date_end: '',
        trigger_condition: '',
        destination_url: '',
        utm_suffix: '',
      },
    ]);
  };

  const handleExportCsv = () => {
    if (!feed.length) return;
    const headers = [
      'row_id',
      'creative_filename',
      'reporting_label',
      'is_default',
      'asset_slot_a_path',
      'asset_slot_b_path',
      'asset_slot_c_path',
      'logo_asset_path',
      'copy_slot_a_text',
      'copy_slot_b_text',
      'copy_slot_c_text',
      'legal_disclaimer_text',
      'cta_button_text',
      'font_color_hex',
      'cta_bg_color_hex',
      'background_color_hex',
      'platform_id',
      'placement_dimension',
      'asset_format_type',
      'audience_id',
      'geo_targeting',
      'date_start',
      'date_end',
      'trigger_condition',
      'destination_url',
      'utm_suffix',
    ];
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

  const handleExportBrief = () => {
    if (!feed.length) return;
    const lines: string[] = [];
    lines.push('DCO Feed – Production Brief');
    lines.push('========================================');
    lines.push('');
    feed.forEach((row) => {
      lines.push(`Asset: ${row.creative_filename}`);
      lines.push(`Label: ${row.reporting_label}`);
      lines.push(`Platform: ${row.platform_id} · ${row.placement_dimension}`);
      lines.push(`Type: ${row.asset_format_type}`);
      lines.push(`Destination: ${row.destination_url}`);
      lines.push('');
    });
    const blob = new Blob([lines.join('\n')], { type: 'text/plain;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'dco_production_brief.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <main className="min-h-screen bg-slate-50">
      <div className="max-w-6xl mx-auto py-10 px-4 space-y-8">
        <header className="flex items-center justify-between gap-4">
          <div>
            <h1 className="text-lg font-semibold text-slate-900">Asset Feed Builder</h1>
            <p className="text-sm text-slate-500">
              Inspect the generated dynamic creative feed before handing it off to production.
            </p>
          </div>
        </header>

        {/* Controls */}
        <section className="flex flex-wrap items-center gap-3">
          <button
            onClick={addFeedRow}
            className="px-4 py-2 text-xs font-semibold rounded-full bg-teal-600 text-white hover:bg-teal-700"
          >
            {feed.length === 0 ? 'Add first row' : 'Add row'}
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
            Export Production Brief (TXT)
          </button>
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
                  {FEED_COLUMNS.map((col) => (
                    <th
                      key={col.key as string}
                      className="text-left px-3 py-2 font-semibold text-slate-600 border-b border-slate-200"
                    >
                      {col.label}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {feed.map((row, index) => (
                  <tr key={row.row_id} className="odd:bg-white even:bg-slate-50/40">
                    {FEED_COLUMNS.map((col) => {
                      const key = col.key;
                      const cellValue = row[key];

                      if (col.readOnly) {
                        return (
                          <td
                            key={key as string}
                            className="px-3 py-2 border-b border-slate-100 font-mono text-slate-700"
                          >
                            {String(cellValue ?? '')}
                          </td>
                        );
                      }

                      if (key === 'is_default') {
                        return (
                          <td key={key as string} className="px-3 py-2 border-b border-slate-100">
                            <button
                              type="button"
                              onClick={() => setDefaultRow(index)}
                              className={`px-2 py-1 rounded-full text-[10px] ${
                                row.is_default
                                  ? 'bg-teal-600 text-white'
                                  : 'bg-slate-100 text-slate-500 hover:bg-slate-200'
                              }`}
                            >
                              {row.is_default ? 'Default' : 'Make default'}
                            </button>
                          </td>
                        );
                      }

                      return (
                        <td key={key as string} className="px-3 py-2 border-b border-slate-100">
                          <input
                            className="w-full border border-slate-200 rounded px-2 py-1 text-[11px] text-slate-700 focus:outline-none focus:ring-1 focus:ring-teal-500/40 focus:border-teal-500"
                            value={(cellValue ?? '') as string}
                            onChange={(e) => updateFeedCell(index, key, e.target.value)}
                          />
                        </td>
                      );
                    })}
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


