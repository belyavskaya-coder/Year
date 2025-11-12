from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT

# === Подготовка ===
pdf_file = "resume_Natalya_Belyavskaya_final.pdf"
doc = SimpleDocTemplate(
    pdf_file,
    pagesize=A4,
    leftMargin=25 * mm,    # ← 25 мм = ~71 pt (отличный отступ!)
    rightMargin=20 * mm,
    topMargin=20 * mm,
    bottomMargin=20 * mm,
    title="Резюме Белявской Н.А."
)

# === Шрифты ===
try:
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVu-Bold', 'DejaVuSans-Bold.ttf'))
    normal_font = 'DejaVu'
    bold_font = 'DejaVu-Bold'
except:
    normal_font = 'Helvetica'
    bold_font = 'Helvetica-Bold'

# === Стили ===
styles = getSampleStyleSheet()
styleN = ParagraphStyle(
    'Normal',
    parent=styles['Normal'],
    fontName=normal_font,
    fontSize=11,
    leading=14,  # межстрочный интервал
    spaceAfter=6,
    leftIndent=0,
)
styleB = ParagraphStyle(
    'Bold',
    parent=styles['Heading2'],
    fontName=bold_font,
    fontSize=13,
    spaceAfter=8,
    spaceBefore=12,
    textColor='black',
)
styleTitle = ParagraphStyle(
    'Title',
    fontName=bold_font,
    fontSize=18,
    spaceAfter=6,
)
styleContact = ParagraphStyle(
    'Contact',
    fontName=normal_font,
    fontSize=11,
    textColor='#444444',
    spaceAfter=12,
)

# === Контент ===
story = []

# Заголовок
story.append(Paragraph("Белявская Наталья Андреевна", styleTitle))
story.append(Paragraph("г. Сочи | smolyanatali@ya.ru | +7 938-420-08-88", styleContact))
story.append(HRFlowable(width="100%", thickness=0.5, color="#cccccc", spaceBefore=6, spaceAfter=12))

# Функция для пунктов
def add_section(title, bullets):
    story.append(Paragraph(title, styleB))
    for bullet in bullets:
        story.append(Paragraph(f"• {bullet}", styleN))

# Секции
add_section("Цель", [
    "Получение позиции стажёра в IT-сфере для развития навыков в программировании, веб-разработке и анализе данных. Готова активно учиться и вносить вклад в команду."
])

add_section("Образование", [
    "Тюменский государственный университет, 1 курс (2025–2029)",
    "<font name='DejaVu' size='10'>Направление подготовки: Разработка продуктов информационных систем</font>"
])

add_section("Навыки", [
    "Веб: HTML (изучаю), CSS (изучаю)",
    "Языки: Python (изучаю, работа с Jupyter, pandas, matplotlib)",
    "Базы данных: SQL (SELECT, JOIN, агрегаты — на уровне обучения)",
    "Теория: Понимаю принципы работы нейронных сетей",
    "Инструменты: VS Code, Jupyter Notebook, Git (начальный уровень)",
    "Английский: начинаю системно изучать — A1, цель B1 за год",
    "Soft skills: высокая обучаемость, ответственность, терпение, эмпатия"
])

add_section("Проекты (учебные / личные)", [
    "'Конвертер валют' — Python-скрипт с курсами ЦБ (requests, json)",
    "'Страница-портфолио' — HTML+CSS (адаптивная верстка, медиазапросы)",
    "Анализ данных в Jupyter: 'Расходы за месяц' (pandas, matplotlib)"
])

add_section("Личное", [
    "Живу в Сочи с 2015 г.",
    "Люблю животных, готовлю, пишу книгу 📖, интересуюсь финансовой грамотностью.",
    "Ценю честность, развитие и позитивные эмоции — и стараюсь дарить их другим."
])

# === Генерация PDF ===
doc.build(story)
print(f"✅ Финальная версия сохранена: {pdf_file}")