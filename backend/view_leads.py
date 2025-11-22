"""عرض العملاء المحتملين من قاعدة البيانات"""
import sqlite3
from datetime import datetime

conn = sqlite3.connect('datapurity.db')
cursor = conn.cursor()

# Get table info
cursor.execute('PRAGMA table_info(leads)')
columns = [col[1] for col in cursor.fetchall()]

# Get all leads
cursor.execute('SELECT * FROM leads ORDER BY created_at DESC')
rows = cursor.fetchall()

print('=' * 70)
print('📊 العملاء المحتملين في قاعدة البيانات')
print('=' * 70)
print(f'\n✓ إجمالي العملاء: {len(rows)}\n')

if rows:
    for i, row in enumerate(rows, 1):
        print(f'عميل محتمل #{i}:')
        print(f'  🆔 ID: {row[0]}')
        print(f'  👤 الاسم: {row[1]}')
        print(f'  📧 الإيميل: {row[2]}')
        print(f'  📱 الجوال: {row[3] or "غير محدد"}')
        print(f'  🏢 الشركة: {row[4] or "غير محدد"}')
        print(f'  🏭 القطاع: {row[5] or "غير محدد"}')
        print(f'  📍 المصدر: {row[6]}')
        print(f'  🌐 IP: {row[7] or "غير متوفر"}')
        print(f'  📅 تاريخ الإنشاء: {row[9]}')
        print('-' * 70)
else:
    print('⚠️  لا توجد بيانات حتى الآن')
    print('💡 جرب إرسال النموذج من الصفحة: http://127.0.0.1:8000/')

print(f'\n📂 موقع قاعدة البيانات: d:\\datapurity\\backend\\datapurity.db')
print('✅ يمكنك فتحها بأي برنامج SQLite Viewer\n')

conn.close()
