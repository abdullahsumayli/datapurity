from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple, Literal


# ------------ Regex أساسية ------------- #

EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
URL_REGEX = re.compile(
    r"\b(?:https?://|www\.)[A-Za-z0-9._%/-]+\.[A-Za-z]{2,}\b",
    re.IGNORECASE,
)

# أرقام سعودية + نمط عام
PHONE_REGEX = re.compile(
    r"""
    (?:
        (?P<intl>\+\d{1,3})?          # كود دولي اختياري
        [\s\-\.]*
        (?:
            (?:0?5\d{8})              # جوال سعودي مثل 05xxxxxxxx
            |
            (?:5\d{8})                # جوال بدون الصفر
            |
            (?:\d{2,4}[\s\-\.]?\d{3}[\s\-\.]?\d{3,4})  # نمط عام
        )
    )
    """,
    re.VERBOSE,
)


# ------------ كلمات دلالية ------------- #

AR_COMPANY_KEYWORDS = [
    "شركة", "مؤسسة", "مجموعة", "القابضة", "القابضه",
    "العقاري", "العقارية", "العقاريه", "القابضة",
    "للاستثمار", "للتطوير", "للمقاولات", "للتمويل",
    "بنك", "البنك", "البلاد", "الراجحي", "الإنماء",
]

EN_COMPANY_KEYWORDS = [
    "Company", "Co.", "Co", "Est.", "Est", "Holding", "Group",
    "Real Estate", "Development", "Trading", "Contracting",
    "Bank", "Albilad", "Albilad Bank", "Bank Albilad",
]

AR_TITLE_KEYWORDS = [
    "مدير", "مسؤول", "مشرف", "رئيس", "أخصائي", "تنفيذي",
    "مندوب", "ممثل", "مسوّق", "مسوق", "التسويق", "العلاقات العامة",
    "العلاقات العامه", "دعم المبيعات", "المبيعات", "الموارد البشرية",
]

EN_TITLE_KEYWORDS = [
    "Manager", "Specialist", "Executive", "Officer", "Director",
    "Representative", "Marketing", "Sales", "Public Relations",
    "PR", "Human Resources", "HR", "Support Manager",
]


# ------------ أدوات مساعدة عامة ------------- #


def _split_lines(text: str) -> List[str]:
    lines = [ln.strip() for ln in text.splitlines()]
    return [ln for ln in lines if ln]


def detect_language(text: str) -> Literal["ar", "en", "mixed"]:
    has_ar = bool(re.search(r"[\u0600-\u06FF]", text))
    has_en = bool(re.search(r"[A-Za-z]", text))
    if has_ar and has_en:
        return "mixed"
    if has_ar:
        return "ar"
    if has_en:
        return "en"
    return "mixed"


def parse_email(text: str) -> Optional[str]:
    match = EMAIL_REGEX.search(text)
    return match.group(0) if match else None


def parse_website(text: str) -> Optional[str]:
    match = URL_REGEX.search(text)
    return match.group(0) if match else None


def _normalize_phone(raw: str) -> str:
    digits = re.sub(r"[^\d+]", "", raw or "")

    if not digits:
        return ""

    # +966 5xxxxxxxx
    if digits.startswith("+966"):
        # إزالة أي صفر زائد بعد 966
        if digits.startswith("+9660"):
            digits = "+966" + digits[5:]
        return digits

    # 05xxxxxxxx → +9665xxxxxxxx
    if digits.startswith("05") and len(digits) == 10:
        return "+966" + digits[1:]

    # 5xxxxxxxxx → +9665xxxxxxxx
    if digits.startswith("5") and len(digits) == 9:
        return "+966" + digits

    return digits


def parse_phone(text: str) -> Dict[str, Optional[str]]:
    match = PHONE_REGEX.search(text)
    if not match:
        return {"raw": None, "normalized": None}
    raw = match.group(0)
    normalized = _normalize_phone(raw)
    return {"raw": raw, "normalized": normalized or None}


def _contains_any(s: str, words: List[str]) -> bool:
    return any(w in s for w in words)


def _looks_like_company(line: str) -> bool:
    if _contains_any(line, AR_COMPANY_KEYWORDS) or _contains_any(line, EN_COMPANY_KEYWORDS):
        return True
    # لا نريد اعتبار "Bank Albilad" اسماً لشخص
    if "Bank" in line or "بنك" in line:
        return True
    return False


def _looks_like_title(line: str) -> bool:
    return _contains_any(line, AR_TITLE_KEYWORDS) or _contains_any(line, EN_TITLE_KEYWORDS)


def _looks_like_contact(line: str) -> bool:
    return bool(
        EMAIL_REGEX.search(line) or
        PHONE_REGEX.search(line) or
        URL_REGEX.search(line)
    )


def _pick_name_candidate(lines: List[str]) -> Optional[str]:
    """
    يحاول اختيار اسم الشخص:
    - لا يحتوي Bank/شركة/وظيفة/إيميل/جوال
    - عدد كلمات من 2 إلى 6
    """
    for ln in lines:
        if _looks_like_contact(ln):
            continue
        if _looks_like_company(ln):
            continue
        if _looks_like_title(ln):
            continue
        word_count = len(ln.split())
        if 2 <= word_count <= 6:
            # استبعاد سطور تبدأ بـ "بنك / Bank"
            if ln.strip().startswith("بنك") or ln.strip().startswith("Bank"):
                continue
            return ln
    return None


def _classify_lines(lines: List[str]) -> Tuple[
    Optional[str], Optional[str], Optional[str], List[str]
]:
    """
    يرجع (name, company, title, remaining_lines)
    """
    name: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None

    remaining: List[str] = []

    # خطوة 1: التقاط الشركة والوظيفة بشكل مباشر
    for ln in lines:
        if _looks_like_company(ln) and company is None:
            company = ln
            continue
        if _looks_like_title(ln) and title is None:
            title = ln
            continue
        remaining.append(ln)

    # خطوة 2: اختيار الاسم من الباقي
    name_candidate = _pick_name_candidate(remaining)
    if name_candidate:
        name = name_candidate
        remaining = [ln for ln in remaining if ln != name_candidate]

    # remaining الآن: أسطر أخرى (قد تحوي عنواناً أو وصفاً)
    return name, company, title, remaining


def parse_business_card(text: str) -> Dict[str, Any]:
    """
    نقطة الدخول الرئيسية: تستقبل نص OCR خام وتُرجع الحقول جاهزة.
    """
    if not text:
        return {
            "name": None,
            "company": None,
            "title": None,
            "email": None,
            "phone": {"raw": None, "normalized": None},
            "website": None,
            "address": None,
        }

    lines = _split_lines(text)
    if not lines:
        return {
            "name": None,
            "company": None,
            "title": None,
            "email": None,
            "phone": {"raw": None, "normalized": None},
            "website": None,
            "address": None,
        }

    joined = " ".join(lines)

    email = parse_email(joined)
    website = parse_website(joined)
    phone = parse_phone(joined)

    name, company, title, remaining_lines = _classify_lines(lines)

    # تنظيف العنوان: إزالة أي سطر كله تكرار لاسم/شركة/وظيفة/إيميل/جوال/موقع
    clean_address_lines: List[str] = []
    seen: set[str] = set()

    for ln in remaining_lines:
        if not ln:
            continue
        if _looks_like_contact(ln):
            continue
        if name and ln == name:
            continue
        if company and ln == company:
            continue
        if title and ln == title:
            continue
        if ln in seen:
            continue
        seen.add(ln)
        clean_address_lines.append(ln)

    address = "\n".join(clean_address_lines) if clean_address_lines else None

    return {
        "name": name,
        "company": company,
        "title": title,
        "email": email,
        "phone": phone,
        "website": website,
        "address": address,
    }
