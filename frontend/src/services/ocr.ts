export type OcrLanguage = 'ar' | 'en' | 'mixed' | string

export interface OcrPhoneField {
  raw?: string | null
  normalized?: string | null
}

export interface OcrFields {
  name?: string | null
  company?: string | null
  title?: string | null
  email?: string | null
  phone?: OcrPhoneField | null
  website?: string | null
  address?: string | null
}

export interface OcrApiResponse {
  raw_text: string
  language: OcrLanguage
  fields: OcrFields
}

/**
 * Calls the backend OCR endpoint to extract information from a business card image.
 */
export async function ocrBusinessCard(file: File): Promise<OcrApiResponse> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch('/api/v1/ocr/card', {
    method: 'POST',
    body: formData
  })

  if (!response.ok) {
    let detail = 'فشل في قراءة الكرت، حاول مرة أخرى.'
    try {
      const errorBody = (await response.json()) as { detail?: string }
      if (errorBody?.detail) {
        detail = errorBody.detail
      }
    } catch {
      // ignore parse errors and use generic message
    }
    throw new Error(detail)
  }

  const payload = (await response.json()) as OcrApiResponse
  return payload
}
