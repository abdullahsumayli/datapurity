import JSZip from 'jszip'
import Papa from 'papaparse'
import * as XLSX from 'xlsx'

type CellValue = string | number | boolean | null | undefined

export interface ProcessedData {
  headers: string[]
  rows: CellValue[][]
  totalRows: number
  duplicates: number
  emptyRows: number
  cleanedData: CleanedContact[]
}

export interface CleanedContact {
  id: number
  name: string
  email: string
  phone: string
  company?: string
  address?: string
  notes?: string
  status: 'valid' | 'warning' | 'error'
  issues: string[]
}

/**
 * معالجة الملفات المضغوطة واستخراج البيانات
 */
export async function processZipFile(file: File): Promise<File[]> {
  const zip = new JSZip()
  const contents = await zip.loadAsync(file)
  const extractedFiles: File[] = []

  for (const [filename, fileData] of Object.entries(contents.files)) {
    if (!fileData.dir && isValidDataFile(filename)) {
      const blob = await fileData.async('blob')
      const extractedFile = new File([blob], filename, { type: getMimeType(filename) })
      extractedFiles.push(extractedFile)
    }
  }

  return extractedFiles
}

/**
 * معالجة ملف Excel
 */
export async function processExcelFile(file: File): Promise<ProcessedData> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    
    reader.onload = (e) => {
      try {
        const data = new Uint8Array(e.target?.result as ArrayBuffer)
        const workbook = XLSX.read(data, { type: 'array' })
        const firstSheet = workbook.Sheets[workbook.SheetNames[0]]
        const jsonData = XLSX.utils.sheet_to_json(firstSheet, { header: 1 }) as CellValue[][]

        if (jsonData.length === 0) {
          reject(new Error('الملف فارغ'))
          return
        }

        const headers = jsonData[0].map(h => String(h).trim())
        const rows = jsonData.slice(1)

        const processed = processAndCleanData(headers, rows)
        resolve(processed)
      } catch (error) {
        reject(error)
      }
    }

    reader.onerror = () => reject(new Error('فشل قراءة الملف'))
    reader.readAsArrayBuffer(file)
  })
}

/**
 * معالجة ملف CSV
 */
export async function processCSVFile(file: File): Promise<ProcessedData> {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      complete: (results: Papa.ParseResult<CellValue[]>) => {
        try {
          const data = results.data as CellValue[][]
          if (data.length === 0) {
            reject(new Error('الملف فارغ'))
            return
          }

          const headers = data[0].map(h => String(h).trim())
          const rows = data.slice(1)

          const processed = processAndCleanData(headers, rows)
          resolve(processed)
        } catch (error) {
          reject(error)
        }
      },
      error: (error: Error) => reject(error),
      skipEmptyLines: true
    })
  })
}

/**
 * معالجة وتنظيف البيانات
 */
function processAndCleanData(headers: string[], rows: CellValue[][]): ProcessedData {
  const columnMap = mapColumns(headers)
  const cleanedData: CleanedContact[] = []
  let duplicates = 0
  let emptyRows = 0
  const seenEmails = new Set<string>()
  const seenPhones = new Set<string>()

  rows.forEach((row, index) => {
    // تجاهل الصفوف الفارغة
    if (isEmptyRow(row)) {
      emptyRows++
      return
    }

    const contact = extractContact(row, columnMap, index + 1)
    
    // فحص التكرار
    const isDuplicate = (contact.email && seenEmails.has(contact.email)) ||
                        (contact.phone && seenPhones.has(contact.phone))
    
    if (isDuplicate) {
      duplicates++
      contact.issues.push('تكرار')
      contact.status = 'warning'
    }

    if (contact.email) seenEmails.add(contact.email)
    if (contact.phone) seenPhones.add(contact.phone)

    cleanedData.push(contact)
  })

  return {
    headers,
    rows,
    totalRows: rows.length,
    duplicates,
    emptyRows,
    cleanedData
  }
}

/**
 * تعيين الأعمدة تلقائياً
 */
function mapColumns(headers: string[]): Record<string, number> {
  const map: Record<string, number> = {}

  headers.forEach((header, index) => {
    const normalized = normalizeHeader(header)

    if (matchesPattern(normalized, ['name', 'اسم', 'الاسم', 'full name'])) {
      map.name = index
    } else if (matchesPattern(normalized, ['email', 'بريد', 'إيميل', 'e-mail', 'بريد إلكتروني'])) {
      map.email = index
    } else if (matchesPattern(normalized, ['phone', 'tel', 'mobile', 'هاتف', 'جوال', 'رقم'])) {
      map.phone = index
    } else if (matchesPattern(normalized, ['company', 'شركة', 'organization', 'منظمة'])) {
      map.company = index
    } else if (matchesPattern(normalized, ['address', 'عنوان', 'location', 'موقع'])) {
      map.address = index
    } else if (matchesPattern(normalized, ['notes', 'ملاحظات', 'note', 'comment'])) {
      map.notes = index
    }
  })

  return map
}

/**
 * استخراج جهة اتصال من صف
 */
function extractContact(row: CellValue[], columnMap: Record<string, number>, id: number): CleanedContact {
  const contact: CleanedContact = {
    id,
    name: '',
    email: '',
    phone: '',
    status: 'valid',
    issues: []
  }

  // استخراج البيانات
  if (columnMap.name !== undefined) {
    contact.name = cleanText(row[columnMap.name])
  }
  if (columnMap.email !== undefined) {
    contact.email = cleanEmail(row[columnMap.email])
  }
  if (columnMap.phone !== undefined) {
    contact.phone = cleanPhone(row[columnMap.phone])
  }
  if (columnMap.company !== undefined) {
    contact.company = cleanText(row[columnMap.company])
  }
  if (columnMap.address !== undefined) {
    contact.address = cleanText(row[columnMap.address])
  }
  if (columnMap.notes !== undefined) {
    contact.notes = cleanText(row[columnMap.notes])
  }

  // التحقق من الصحة
  validateContact(contact)

  return contact
}

/**
 * التحقق من صحة جهة الاتصال
 */
function validateContact(contact: CleanedContact) {
  if (!contact.name) {
    contact.issues.push('الاسم مفقود')
    contact.status = 'error'
  }

  if (!contact.email && !contact.phone) {
    contact.issues.push('البريد أو الهاتف مفقود')
    contact.status = 'error'
  }

  if (contact.email && !isValidEmail(contact.email)) {
    contact.issues.push('بريد غير صحيح')
    contact.status = contact.status === 'error' ? 'error' : 'warning'
  }

  if (contact.phone && !isValidPhone(contact.phone)) {
    contact.issues.push('رقم هاتف غير صحيح')
    contact.status = contact.status === 'error' ? 'error' : 'warning'
  }
}

/**
 * تنظيف النص
 */
function cleanText(value: CellValue): string {
  if (!value) return ''
  return String(value).trim().replace(/\s+/g, ' ')
}

/**
 * تنظيف البريد الإلكتروني
 */
function cleanEmail(value: CellValue): string {
  if (!value) return ''
  return String(value).toLowerCase().trim()
}

/**
 * تنظيف رقم الهاتف
 */
function cleanPhone(value: CellValue): string {
  if (!value) return ''
  // إزالة المسافات والرموز غير الرقمية (ما عدا +)
  let phone = String(value).replace(/[^\d+]/g, '')
  
  // إضافة +966 للأرقام السعودية
  if (phone.startsWith('05')) {
    phone = '+966' + phone.substring(1)
  } else if (phone.startsWith('5') && phone.length === 9) {
    phone = '+966' + phone
  }
  
  return phone
}

/**
 * التحقق من صحة البريد الإلكتروني
 */
function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * التحقق من صحة رقم الهاتف
 */
function isValidPhone(phone: string): boolean {
  // التحقق من الأرقام السعودية
  const saudiRegex = /^\+966\d{9}$/
  const internationalRegex = /^\+\d{10,15}$/
  return saudiRegex.test(phone) || internationalRegex.test(phone)
}

/**
 * تطبيع اسم العمود
 */
function normalizeHeader(header: string): string {
  return header.toLowerCase().trim().replace(/[_\s-]+/g, '')
}

/**
 * مطابقة النمط
 */
function matchesPattern(text: string, patterns: string[]): boolean {
  return patterns.some(pattern => 
    text.includes(pattern.toLowerCase().replace(/\s+/g, ''))
  )
}

/**
 * فحص إذا كان الصف فارغاً
 */
function isEmptyRow(row: CellValue[]): boolean {
  return row.every(cell => !cell || String(cell).trim() === '')
}

/**
 * فحص إذا كان الملف صالحاً
 */
function isValidDataFile(filename: string): boolean {
  const ext = filename.toLowerCase().split('.').pop()
  return ['csv', 'xlsx', 'xls'].includes(ext || '')
}

/**
 * الحصول على نوع MIME
 */
function getMimeType(filename: string): string {
  const ext = filename.toLowerCase().split('.').pop()
  const mimeTypes: Record<string, string> = {
    'csv': 'text/csv',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'xls': 'application/vnd.ms-excel'
  }
  return mimeTypes[ext || ''] || 'application/octet-stream'
}

/**
 * معالجة ملف (اكتشاف النوع تلقائياً)
 */
export async function processFile(file: File): Promise<ProcessedData> {
  const ext = file.name.toLowerCase().split('.').pop()
  
  if (ext === 'zip') {
    const extractedFiles = await processZipFile(file)
    if (extractedFiles.length === 0) {
      throw new Error('لا توجد ملفات بيانات في الملف المضغوط')
    }
    // معالجة أول ملف صالح
    return processFile(extractedFiles[0])
  } else if (ext === 'csv') {
    return processCSVFile(file)
  } else if (ext === 'xlsx' || ext === 'xls') {
    return processExcelFile(file)
  } else {
    throw new Error('نوع الملف غير مدعوم')
  }
}

/**
 * تصدير البيانات المنظفة إلى Excel
 */
export function exportToExcel(data: CleanedContact[], filename: string = 'cleaned_data.xlsx') {
  const excelData = data.map(contact => ({
    'الاسم': contact.name,
    'البريد الإلكتروني': contact.email,
    'رقم الهاتف': contact.phone,
    'الشركة': contact.company || '',
    'العنوان': contact.address || '',
    'ملاحظات': contact.notes || '',
    'الحالة': contact.status === 'valid' ? 'صحيح' : contact.status === 'warning' ? 'تحذير' : 'خطأ',
    'المشاكل': contact.issues.join(', ')
  }))

  const wb = XLSX.utils.book_new()
  const ws = XLSX.utils.json_to_sheet(excelData)

  // تنسيق الأعمدة
  ws['!cols'] = [
    { wch: 25 }, // الاسم
    { wch: 30 }, // البريد
    { wch: 18 }, // الهاتف
    { wch: 25 }, // الشركة
    { wch: 35 }, // العنوان
    { wch: 30 }, // ملاحظات
    { wch: 12 }, // الحالة
    { wch: 40 }  // المشاكل
  ]

  XLSX.utils.book_append_sheet(wb, ws, 'البيانات المنظفة')
  XLSX.writeFile(wb, filename)
}

/**
 * تصدير إلى CSV
 */
export function exportToCSV(data: CleanedContact[], filename: string = 'cleaned_data.csv') {
  const csvData = data.map(contact => ({
    name: contact.name,
    email: contact.email,
    phone: contact.phone,
    company: contact.company || '',
    address: contact.address || '',
    notes: contact.notes || '',
    status: contact.status,
    issues: contact.issues.join('; ')
  }))

  const csv = Papa.unparse(csvData, {
    header: true
  })

  const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  
  link.setAttribute('href', url)
  link.setAttribute('download', filename)
  link.click()
}
