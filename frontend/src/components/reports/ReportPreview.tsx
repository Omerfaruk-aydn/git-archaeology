import React from 'react';

interface ReportPreviewProps {
  content: string;
  format: string;
}

export function ReportPreview({ content, format }: ReportPreviewProps) {
  if (format === 'html') {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div
          className="prose max-w-none"
          dangerouslySetInnerHTML={{ __html: content }}
        />
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <pre className="whitespace-pre-wrap font-sans text-sm text-gray-800 leading-relaxed">
        {content}
      </pre>
    </div>
  );
}
