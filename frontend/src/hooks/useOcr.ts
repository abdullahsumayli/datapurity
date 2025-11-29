// OCR hook for business card extraction

export type OcrCardFields = {
  name?: string | null;
  company?: string | null;
  title?: string | null;
  email?: string | null;
  phone?: { raw?: string | null; normalized?: string | null } | null;
  website?: string | null;
  address?: string | null;
};

export type OcrCardResult = {
  raw_text: string;
  language: 'ar' | 'en' | 'mixed' | string;
  fields: OcrCardFields;
};

export async function ocrBusinessCard(file: File): Promise<OcrCardResult> {
  const formData = new FormData();
  // backend single-card endpoint expects field name 'file'
  formData.append('file', file);

  const res = await fetch('/api/v1/ocr/business-card', {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    let errorMsg = 'OCR failed';
    try {
      const err = await res.json();
      errorMsg = err.detail || err.message || errorMsg;
    } catch {}
    throw new Error(errorMsg);
  }

  const data = await res.json();

  // Normalize response shapes:
  // - legacy batch shape: { success, records: [...] }
  // - new single-card shape: { status: 'success', data: { ... } }
  // - direct shape: { raw_text, language, fields }
  if (data && data.success && Array.isArray(data.records) && data.records.length > 0) {
    const rec = data.records[0];
    const fields: OcrCardFields = {
      name: rec.name || null,
      company: rec.company || null,
      title: rec.title || null,
      email: rec.emails ? (Array.isArray(rec.emails) ? rec.emails[0] : rec.emails) : null,
      phone: rec.phones ? { raw: rec.phones, normalized: rec.phones } : null,
      website: rec.website || null,
      address: rec.address || null,
    };

    return {
      raw_text: rec.source_text || rec.ocr_text || '',
      language: rec.language || 'mixed',
      fields,
    };
  }

  // New API shape: { status: 'success', data: { name, company, job_title, phone, email, website, raw_text } }
  if (data && (data.status === 'success' || data.status === 'ok') && data.data) {
    const d = data.data as any;
    const fields: OcrCardFields = {
      name: d.name || d.full_name || null,
      company: d.company || null,
      title: d.job_title || d.title || null,
      email: d.email || null,
      phone: d.phone ? { raw: d.phone, normalized: d.phone } : null,
      website: d.website || null,
      address: d.address || null,
    };

    return {
      raw_text: d.raw_text || d.ocr_text || '',
      language: (d.language as any) || 'mixed',
      fields,
    };
  }

  // If response already matches the desired shape
  if (data && data.fields) {
    return data as OcrCardResult;
  }

  // fallback: try to map common keys
  const mapped: OcrCardResult = {
    raw_text: data.raw_text || data.ocr_text || '',
    language: data.language || 'mixed',
    fields: {
      name: data.name || data.full_name || null,
      company: data.company || null,
      title: data.title || data.job_title || null,
      email: data.email || null,
      phone: data.phone ? { raw: data.phone, normalized: data.phone } : null,
      website: data.website || null,
      address: data.address || null,
    },
  };

  return mapped;
}
