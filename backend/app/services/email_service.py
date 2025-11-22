"""Email service for marketing automation."""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Tuple

from app.core.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def build_template(template_name: str, context: dict) -> Tuple[str, str]:
    """
    Build email subject and body from template.
    
    Args:
        template_name: Template identifier
        context: Context data for template
        
    Returns:
        Tuple of (subject, body)
    """
    lead_name = context.get("lead_name", "عزيزي العميل")
    
    templates = {
        "welcome_0": {
            "subject": "مرحباً بك في DataPurity - جرّب التنظيف المجاني الآن! 🎉",
            "body": f"""
مرحباً {lead_name}! 👋

شكراً لتسجيلك في DataPurity - منصة تنظيف البيانات الذكية!

🎁 **هديتك المجانية:**
يمكنك الآن تنظيف **150 سجل مجاناً** بدون أي التزام!

ما الذي تحصل عليه:
✅ تنظيف أسماء جهات الاتصال
✅ توحيد أرقام الهاتف
✅ التحقق من صحة البريد الإلكتروني
✅ إزالة التكرارات
✅ تحديد البيانات غير الصحيحة

🚀 **ابدأ الآن:**
1. قم بتحميل ملف Excel أو CSV الخاص بك
2. احصل على بياناتك النظيفة في دقائق
3. وفّر ساعات من العمل اليدوي!

رابط التجربة المجانية:
http://46.62.239.119:8000/api/v1/trial/upload

لديك أي أسئلة؟ نحن هنا للمساعدة!

مع تحياتنا,
فريق DataPurity 💙
            """
        },
        
        "trial_reminder_1": {
            "subject": "لا تفوت فرصة تنظيف بياناتك مجاناً! ⏰",
            "body": f"""
مرحباً {lead_name}!

لاحظنا أنك لم تجرب خدمة التنظيف المجانية بعد.

⏰ **العرض محدود:**
150 سجل مجاني في انتظارك!

لماذا DataPurity؟
📊 نظّفنا أكثر من 5 ملايين سجل لعملائنا
⚡ توفير 80% من الوقت مقارنة بالتنظيف اليدوي
✨ دقة 95%+ في تنظيف البيانات
🇸🇦 دعم كامل للغة العربية

جرّب الآن - مجاناً تماماً:
http://46.62.239.119:8000/api/v1/trial/upload

استثمر 5 دقائق فقط وشاهد الفرق!

فريق DataPurity
            """
        },
        
        "case_study_3": {
            "subject": "كيف وفّر أحمد 20 ساعة شهرياً في تنظيف البيانات 💡",
            "body": f"""
مرحباً {lead_name}!

دعني أشارك معك قصة نجاح واقعية:

📖 **قصة أحمد - مدير تسويق:**

**المشكلة:**
كان أحمد يضيع 20 ساعة شهرياً في:
- تنظيف قوائم العملاء يدوياً
- إزالة التكرارات
- توحيد صيغ الهواتف والأسماء

**الحل:**
استخدم DataPurity وحصل على:
✅ تنظيف 10,000 سجل في 5 دقائق
✅ توفير 20 ساعة شهرياً
✅ زيادة دقة البيانات من 60% إلى 95%
✅ تحسين معدل الوصول للعملاء بنسبة 40%

💬 **ما قاله أحمد:**
"DataPurity غيّر طريقة عملنا. بدلاً من قضاء أيام في التنظيف، أصبح الأمر يستغرق دقائق."

🎯 **حان دورك:**
جرّب التنظيف المجاني الآن واكتشف الفرق:
http://46.62.239.119:8000/api/v1/trial/upload

مع تحياتنا,
فريق DataPurity
            """
        },
        
        "discount_push_7": {
            "subject": "🎁 عرض خاص: خصم 30% - محدود لـ 48 ساعة فقط!",
            "body": f"""
مرحباً {lead_name}!

لديّ أخبار رائعة لك! 🎉

🔥 **عرض حصري - لمدة 48 ساعة فقط:**
احصل على خصم 30% على باقة GrowthDesk

**ماذا تحصل عليه:**
✨ تنظيف غير محدود
✨ API مخصص لأنظمتك
✨ دعم فني متقدم
✨ تقارير شهرية مفصلة
✨ أولوية في المعالجة

**الأسعار بعد الخصم:**
~~999 ريال/شهر~~ → **699 ريال/شهر فقط!**

💰 **وفّر 3,600 ريال سنوياً!**

⏰ **العرض ينتهي خلال 48 ساعة**
استخدم كود الخصم: DATAPURITY30

🚀 ابدأ الآن:
http://46.62.239.119:8000/

أي أسئلة؟ نحن هنا للمساعدة!

فريق DataPurity
ص.ب: لا تفوت هذه الفرصة - العرض ينتهي قريباً!
            """
        }
    }
    
    template = templates.get(template_name, {
        "subject": "رسالة من DataPurity",
        "body": f"مرحباً {lead_name}،\n\nشكراً لاهتمامك بـ DataPurity!\n\nفريق DataPurity"
    })
    
    return template["subject"], template["body"]


def send_email(to: str, subject: str, body: str) -> bool:
    """
    Send email via SMTP.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body
        
    Returns:
        True if successful, False otherwise
    """
    if not settings.EMAIL_USERNAME or not settings.EMAIL_PASSWORD:
        logger.warning("Email credentials not configured. Skipping email send.")
        logger.info(f"Would send email to {to}: {subject}")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM or settings.EMAIL_USERNAME}>"
        msg["To"] = to
        msg["Subject"] = subject
        
        # Add body
        msg.attach(MIMEText(body, "plain", "utf-8"))
        
        # Connect to SMTP server
        with smtplib.SMTP(settings.EMAIL_SMTP_HOST, settings.EMAIL_SMTP_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email sent successfully to {to}: {subject}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to}: {str(e)}")
        return False
