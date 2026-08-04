#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_pdf.py — แปลง content plan + สคริปต์ WISAMIN เป็น PDF ส่งทีม
ใช้ fpdf2 + HarfBuzz text shaping (จำเป็นสำหรับภาษาไทย — สระ/วรรณยุกต์ต้องเรียงตำแหน่งถูกต้อง
เหนือ/ใต้พยัญชนะ ซึ่งไลบรารี PDF ทั่วไปที่ไม่มี text shaping จะเรนเดอร์ผิดตำแหน่ง)
รัน: python3 content/generate_pdf.py
"""
import os
from fpdf import FPDF

ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(ROOT, "..", "assets", "fonts")
OUT = os.path.join(ROOT, "WISAMIN_content-plan-scripts_2026-07-15.pdf")

# ---------- สี ----------
ACCENT = (31, 122, 92)
ACCENT_DARK = (18, 70, 53)
WARN = (184, 134, 11)
DANGER = (176, 48, 48)
MUTED = (90, 90, 90)
LINE = (216, 216, 216)
BG_SOFT = (243, 247, 245)
BG_WARN = (255, 248, 230)
BG_DANGER = (253, 234, 234)
BG_GREEN = (234, 245, 239)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PAGE_W = 210 - 20 - 20  # A4 width minus 20mm margins each side


class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-13)
        self.set_font("Thonburi", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 8, f"WISAMIN Content Plan + Scripts · หน้า {self.page_no()}", align="C")


pdf = PDF(format="A4")
pdf.set_margins(20, 18, 20)
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_font("Thonburi", "", os.path.join(FONT_DIR, "Thonburi-Regular.ttf"))
pdf.add_font("Thonburi", "B", os.path.join(FONT_DIR, "Thonburi-Bold.ttf"))
pdf.set_text_shaping(True)
pdf.set_title("WISAMIN Content Plan + Scripts 2026-07-15")
pdf.set_author("WISAMIN Content Team")
pdf.add_page()


# ---------- helper ----------
def h1(text):
    pdf.set_font("Thonburi", "B", 15)
    pdf.set_text_color(*ACCENT_DARK)
    pdf.ln(3)
    pdf.multi_cell(PAGE_W, 7, text, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.ln(1)


def h2(text):
    pdf.set_font("Thonburi", "B", 12)
    pdf.set_text_color(*ACCENT)
    pdf.multi_cell(PAGE_W, 6, text, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.ln(0.5)


def body(text, size=9.7, color=BLACK, leading=5.2):
    pdf.set_font("Thonburi", "", size)
    pdf.set_text_color(*color)
    pdf.multi_cell(PAGE_W, leading, text, new_x="LMARGIN", new_y="NEXT", markdown=True, align="L")


def muted(text, size=8.6):
    body(text, size=size, color=MUTED, leading=4.6)


def hr(space_before=2, space_after=4):
    pdf.ln(space_before)
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(0.5)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(space_after)


def callout(text, bg, border, text_color=BLACK, size=9.3, pad=4):
    pdf.set_fill_color(*bg)
    pdf.set_draw_color(*border)
    pdf.set_line_width(0.4)
    pdf.set_font("Thonburi", "", size)
    pdf.set_text_color(*text_color)
    y0 = pdf.get_y()
    pdf.set_xy(pdf.l_margin, y0)
    pdf.multi_cell(PAGE_W, 5.0, text, border=1, fill=True, markdown=True, align="L",
                    padding=pad, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def script_meta_bar(topic, pillar, funnel, hook, duration):
    pdf.set_fill_color(*ACCENT_DARK)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Thonburi", "B", 10.5)
    pdf.multi_cell(PAGE_W, 6.5, topic, fill=True, padding=3, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.set_fill_color(*BG_SOFT)
    pdf.set_text_color(*BLACK)
    pdf.set_font("Thonburi", "", 8.6)
    meta = f"เสา: {pillar}   |   Funnel: {funnel}   |   Hook: {hook}   |   ความยาว: {duration}"
    pdf.multi_cell(PAGE_W, 5.5, meta, fill=True, padding=3, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.ln(2)


def text_on_screen(text):
    pdf.set_fill_color(*BG_WARN)
    pdf.set_draw_color(*WARN)
    pdf.set_text_color(*WARN)
    pdf.set_font("Thonburi", "", 9.3)
    pdf.multi_cell(PAGE_W, 5.2, f'TEXT ON SCREEN: "{text}"', border=1, fill=True,
                    padding=3, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.ln(2)


def beat(time_range, label, speak, visual, extra=None):
    pdf.set_font("Thonburi", "B", 9.2)
    pdf.set_text_color(*ACCENT_DARK)
    pdf.multi_cell(PAGE_W, 5.3, f"[{time_range}] — {label}", new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.set_font("Thonburi", "", 9.2)
    pdf.set_text_color(*BLACK)
    pdf.set_x(pdf.l_margin + 3)
    pdf.multi_cell(PAGE_W - 3, 5.0, f'บทพูด: "{speak}"', new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.set_font("Thonburi", "", 8.4)
    pdf.set_text_color(*MUTED)
    pdf.set_x(pdf.l_margin + 3)
    pdf.multi_cell(PAGE_W - 3, 4.6, f"Visual: {visual}", new_x="LMARGIN", new_y="NEXT", align="L")
    if extra:
        pdf.set_x(pdf.l_margin + 3)
        pdf.multi_cell(PAGE_W - 3, 4.6, extra, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.ln(1)
    pdf.set_draw_color(*LINE)
    pdf.set_line_width(0.2)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(2.5)


def production_note(text):
    pdf.set_fill_color(240, 240, 240)
    pdf.set_text_color(*MUTED)
    pdf.set_font("Thonburi", "", 8.4)
    pdf.multi_cell(PAGE_W, 4.8, f"Production Notes: {text}", fill=True, padding=3,
                    new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.ln(2)


def audit_box(risk_lines, warn_lines, verdict, advice, danger=False):
    bg = BG_DANGER if danger else BG_GREEN
    border = DANGER if danger else ACCENT
    y0 = pdf.get_y()
    lines = [f"ผลตรวจ FDA-Thai — ระดับความเสี่ยงรวม: {verdict}"]
    body_lines = []
    for l in risk_lines:
        body_lines.append(("[เสี่ยงผิดกฎหมาย] " + l, BLACK))
    for l in warn_lines:
        body_lines.append(("[ควรระวัง] " + l, WARN))
    body_lines.append((f"คำแนะนำ: {advice}", BLACK))

    pdf.set_xy(pdf.l_margin, y0)
    pdf.set_fill_color(*bg)
    pdf.set_font("Thonburi", "B", 9.3)
    pdf.set_text_color(*(DANGER if danger else ACCENT))
    pdf.multi_cell(PAGE_W, 5.2, lines[0], fill=True, padding=(3, 4, 1, 4),
                    new_x="LMARGIN", new_y="NEXT", align="L")
    for text, color in body_lines:
        pdf.set_font("Thonburi", "", 8.8)
        pdf.set_text_color(*color)
        pdf.set_fill_color(*bg)
        pdf.multi_cell(PAGE_W, 4.8, text, fill=True, padding=(0, 4, 1, 4),
                        new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.set_fill_color(*bg)
    pdf.multi_cell(PAGE_W, 2, "", fill=True, padding=(0, 4, 2, 4), new_x="LMARGIN", new_y="NEXT", align="L")
    y1 = pdf.get_y()
    pdf.rect(pdf.l_margin, y0, PAGE_W, y1 - y0, style="D")
    pdf.ln(3)


def data_table(header, rows, col_widths, header_size=8.3, cell_size=8.0):
    line_h = 4.3
    pdf.set_font("Thonburi", "B", header_size)
    pdf.set_fill_color(*ACCENT_DARK)
    pdf.set_text_color(*WHITE)
    x0 = pdf.l_margin
    y0 = pdf.get_y()
    for w, htext in zip(col_widths, header):
        pdf.multi_cell(w, 6, htext, border=1, fill=True, align="L",
                        new_x="RIGHT", new_y="TOP", padding=1.5)
    pdf.set_xy(x0, y0 + 6)

    pdf.set_font("Thonburi", "", cell_size)
    pdf.set_text_color(*BLACK)
    fill_toggle = False
    for row in rows:
        x = pdf.l_margin
        y_start = pdf.get_y()
        cell_heights = []
        for w, val in zip(col_widths, row):
            n_lines = pdf.multi_cell(w, line_h, val, dry_run=True, output="LINES", align="L")
            h = max(line_h * len(n_lines) + 3, line_h + 3)
            cell_heights.append(h)
        max_h = max(cell_heights)
        fill = (247, 250, 249) if fill_toggle else WHITE
        pdf.set_fill_color(*fill)
        for w, val in zip(col_widths, row):
            pdf.set_xy(x, y_start)
            pdf.multi_cell(w, line_h, val, border=1, fill=True, align="L",
                            padding=1.5, new_x="RIGHT", new_y="TOP", max_line_height=line_h)
            x += w
        pdf.set_xy(pdf.l_margin, y_start + max_h)
        fill_toggle = not fill_toggle
    pdf.ln(3)


# ================= หน้าปก =================
pdf.ln(20)
muted("WISAMIN", size=11)
pdf.set_font("Thonburi", "B", 22)
pdf.set_text_color(*ACCENT_DARK)
pdf.multi_cell(PAGE_W, 10, "แผนคอนเทนต์ + สคริปต์พร้อมถ่าย", new_x="LMARGIN", new_y="NEXT", align="L")
pdf.ln(1)
muted("TikTok / Reels / Shorts — สร้างด้วย Framework 4 เสาเข็ม (hb-4-content)", size=11)
muted("ตรวจคำต้องห้าม อย. ผ่าน Skill fda-thai แล้วทุกสคริปต์", size=11)
pdf.ln(1)
muted("เอกสารวันที่ 15 กรกฎาคม 2026 · จัดทำสำหรับทีมงาน WISAMIN")
hr(6, 6)

body("เอกสารนี้เชื่อมกับงานติดตามคู่แข่งอาหารเสริมไทยที่ทำต่อเนื่องมาก่อนหน้านี้ "
     "(WISAMIN Competitor Radar) — ช่วงนี้ตลาดอยู่ในดราม่า **\"โปรตีนตกฉลาก\"** "
     "ผู้บริโภคไม่เชื่อฉลากที่ไม่มีผลแล็บหนุน และ**ยังไม่มีแบรนด์โปรตีนพืช/คอลลาเจน/พรีไบโอติกรายไหน"
     "ทำแคมเปญโชว์ผลแล็บเชิงรุกเลย** — คอนเทนต์ชุดนี้ออกแบบให้ WISAMIN เข้ายึดพื้นที่ว่างนั้นก่อนคู่แข่ง "
     "โดยไม่เสี่ยงผิดกฎหมาย อย.")
pdf.ln(3)
callout(
    "**ข้อควรระวังสำคัญที่สุดในเอกสารนี้:** หน้าโปรดักต์ไม่ได้ระบุตัวเลขโปรตีน/สารอาหารต่อหน่วยบริโภคไว้ชัดเจน "
    "สคริปต์ทุกตัวจึง**จงใจไม่ใส่ตัวเลขกรัมโปรตีนที่แต่งขึ้นเอง** เพราะตลาดกำลังจับผิดเรื่องตัวเลขไม่ตรงฉลากพอดี "
    "ถ้าจะใส่ตัวเลขในคลิปจริง ต้องดึงจากฉลากโภชนาการบนแพ็กเกจจริงเท่านั้น",
    BG_WARN, WARN)
pdf.add_page()

# ================= สินค้าที่ใช้ในชุดนี้ =================
h1("สินค้าที่ใช้ในชุดนี้")
muted("ดึงจากหน้าร้านจริง: max-globalshop.com/category/PDC")
pdf.ln(2)
data_table(
    ["สินค้า", "ราคา", "จุดขายจากหน้าโปรดักต์"],
    [
        ["PROTEIN PLANT Formula 1-4", "69 บาท (จาก 120)",
         "โปรตีนพืชจาก 5 แหล่ง, ออร์แกนิก, ไม่มี GMO, ไม่มีกลูเตน, มีโพรไบโอติก 6 สายพันธุ์ (F.4)"],
        ["EGG WHITE PROTEIN (3 รส)", "69-79 บาท", "โปรตีนจากไข่ขาว"],
        ["CHICKEN PROTEIN", "69 บาท (จาก 129)", "โปรตีนไก่ไฮโดรไลซ์ 4 รส ไม่มีกลูเตน ไม่มี GMO"],
        ["GLUTA COLLA BLINK (5 รส)", "69 บาท (จาก 99)", "กลูตาไธโอน + คอลลาเจนผสม"],
        ["PEA FIBER", "59 บาท (จาก 129)", "ใยอาหารจากถั่วลันเตา"],
    ],
    col_widths=[45, 30, 95])

h2("อ้างอิงโภชนาการทั่วไป (USDA FoodData Central — ความรู้ทั่วไป ไม่ใช่ตัวเลขเฉพาะของ WISAMIN)")
data_table(
    ["แหล่งโปรตีน", "โปรตีนต่อ 100g", "หมายเหตุ"],
    [
        ["ไข่ขาวแบบผง (dried)", "~80-84g", "โปรตีนสมบูรณ์ ไขมันต่ำมาก"],
        ["โปรตีนพืชไอโซเลท (อ้างอิงใกล้เคียง)", "~85-88g", "ต้องกินคู่กับซีเรียล/ข้าวเพื่อให้ครบกรดอะมิโนจำเป็น"],
        ["เวย์โปรตีนไอโซเลท (ผงผสมเครื่องดื่ม)", "~58g", "ตัวเลขต่างกันมากตามสูตรผสม — เหตุผลที่ต้องอ่านฉลากทุกครั้ง"],
    ],
    col_widths=[55, 35, 80])
pdf.ln(1)
body("**แก่นของ hook ที่ใช้ได้จริง:** \"โปรตีนพืชไม่ได้ด้อยกว่าเวย์โดยธรรมชาติ — ถ้ากินให้ครบสูตร "
     "(พืชหลายชนิดผสมกัน) ก็ได้กรดอะมิโนครบเหมือนกัน\" เป็นข้อเท็จจริงทางโภชนาการที่ใช้ได้จริง "
     "ไม่ต้องอ้างตัวเลขเฉพาะเจาะจง")
pdf.add_page()

# ================= แผนคอนเทนต์สัปดาห์นี้ =================
h1("แผนคอนเทนต์สัปดาห์นี้")
body("**ตัวตน IP:** ทีมงาน WISAMIN พูดตรงกล้อง (ถ้ามีเภสัชกร/นักกำหนดอาหารในทีมจริง ใช้คนนั้นแทน — "
     "คอนเทนต์แบบหมอ/เภสัชพูดเองชนะคอนเทนต์ affiliate รีวิวชัดเจนที่สุดในตลาดตอนนี้)")
body("**Funnel:** TOFU (ติดตาม/เซฟ/แชร์) -> MOFU (คอมเมนต์คีย์เวิร์ดรับผลแล็บ/โค้ดส่วนลดใน LINE) "
     "-> BOFU (ซื้อผ่าน TikTok Shop / 7-Eleven Online)")
pdf.ln(2)

data_table(
    ["#", "วัน", "ชื่อคลิป", "สินค้า", "เสา/Funnel", "CTA"],
    [
        ["1", "จันทร์", "อ่านฉลากโปรตีนพืชแบบไม่โดนหลอก", "Plant Protein", "ข้อมูล / TOFU", "เซฟไว้เช็คก่อนซื้อ"],
        ["2", "อังคาร", "ทำไมเรายังไม่พูดตัวเลขโปรตีนจนกว่าจะมีผลแล็บ", "Plant Protein",
         "ข้อมูล+ธุรกิจ / MOFU", "คอมเมนต์ \"แล็บ\" รับแจ้งเตือน"],
        ["3", "พุธ", "เรื่องเล่า: ลูกค้าทักมาถามกลัวโปรตีนตกฉลาก", "Plant Protein",
         "อารมณ์ / TOFU", "คอมเมนต์คำถามที่อยากถาม"],
        ["4", "พฤหัส", "ไข่ขาว vs เวย์ vs โปรตีนพืช ต่างกันตรงไหน", "Egg White Protein",
         "ข้อมูล / TOFU", "เซฟไว้เทียบก่อนซื้อ"],
        ["5", "ศุกร์", "ทำไมเราถึงกล้าออกโปรตีนไก่ ทั้งที่ตลาดมีแต่เวย์กับพืช", "Chicken Protein",
         "สังคม / TOFU", "คอมเมนต์อยากลองรสไหน"],
        ["6", "เสาร์", "เปิดส่วนผสม Gluta Colla Blink ทำไมราคาเข้าถึงง่าย", "Gluta Colla Blink",
         "ธุรกิจ / BOFU", "คอมเมนต์ \"ราคา\" ดูโปร"],
    ],
    col_widths=[7, 15, 60, 28, 25, 35])

muted("**สรุปสัดส่วนเสา:** ข้อมูล 3 / อารมณ์ 1 / สังคม 1 / ธุรกิจ 1 (เอียงไปทางข้อมูลมากกว่าสัดส่วนมาตรฐาน "
      "40/25/20/15 ตั้งใจ เพราะตลาดกำลังหิวข้อมูล/หลักฐานจากดราม่าโปรตีนตกฉลาก)")
muted("**คิวถ่ายแนะนำ:** เขียนสคริปต์วันอาทิตย์ -> ถ่ายคลิป 1-3 รวดเดียววันจันทร์เช้า -> "
      "ถ่ายคลิป 4-6 รวดเดียววันพุธ -> ตัดต่อวันพฤหัส-ศุกร์ -> โพสต์ตามคิว 18:00-20:00")
pdf.add_page()


def render_script(title, meta, text_screen, beats, notes, audit):
    h1(title)
    script_meta_bar(*meta)
    text_on_screen(text_screen)
    for b in beats:
        beat(*b)
    production_note(notes)
    audit_box(**audit)


# ================= สคริปต์ A =================
render_script(
    "สคริปต์ A — อ่านฉลากโปรตีนพืชแบบไม่โดนหลอก",
    ("อ่านฉลากโปรตีนพืชแบบไม่โดนหลอก", "ข้อมูล", "TOFU", "Warning/List", "45 วิ"),
    "3 จุดที่ต้องเช็คก่อนซื้อโปรตีนพืช",
    [
        ("0:00-0:03", "HOOK",
         "ก่อนซื้อโปรตีนพืชขวดต่อไป เช็ค 3 จุดนี้ก่อน ไม่งั้นเสี่ยงจ่ายแพงแต่ได้โปรตีนไม่ครบ",
         "ถือถุงโปรตีนพืชขึ้นมาจอเต็ม พลิกไปด้านหลังฉลากทันที (เคลื่อนไหวทันทีตั้งแต่เฟรมแรก)"),
        ("0:03-0:15", "จุดที่ 1: แหล่งโปรตีนกี่ชนิด",
         "จุดแรก ดูว่าโปรตีนพืชมาจากกี่แหล่ง พืชแหล่งเดียวมักได้กรดอะมิโนไม่ครบ ต้องผสมหลายแหล่งถึงจะครบเหมือนโปรตีนสัตว์",
         "ชี้ที่รายการส่วนผสมบนฉลากจริง วงกลมคำว่า \"5 แหล่ง\" ด้วยปากกา",
         "Open loop: \"จุดที่ 2 สำคัญกว่านี้อีก\""),
        ("0:15-0:28", "จุดที่ 2: ตัวเลขบนฉลากมาจากไหน",
         "จุดที่ 2 — ถามตัวเองว่าตัวเลขที่เห็นบนฉลากมีผลแล็บบุคคลที่ 3 รองรับไหม เพราะช่วงนี้เราเห็นข่าวหลายแบรนด์"
         "ตัวเลขไม่ตรงปกกันเยอะมาก",
         "สลับภาพเป็นสกรีนช็อตข่าวทั่วไป (เบลอโลโก้ ไม่พาดพิงแบรนด์ไหนเจาะจง) กลับมาที่หน้าคน",
         "Pattern change: เปลี่ยนมุมกล้อง/ระยะช็อต"),
        ("0:28-0:40", "จุดที่ 3: ดูวันที่ผลิต/ผลตรวจล่าสุด",
         "จุดที่ 3 เช็ควันที่ของผลตรวจ ไม่ใช่แค่มีผลตรวจ แต่ต้องเป็นล็อตล่าสุดด้วย เพราะสูตรอาจเปลี่ยนได้ตามรอบผลิต",
         "ชี้วันที่ผลิตบนแพ็กเกจ"),
        ("0:40-0:45", "CTA",
         "เซฟคลิปนี้ไว้ก่อนซื้อโปรตีนพืชตัวต่อไป จะได้กลับมาเช็คได้ทัน", "—"),
    ],
    "ถ่ายจอจริง ไม่ใช้กราฟิกลอย · ห้ามพาดพิงชื่อ/โลโก้แบรนด์คู่แข่งแม้เบลอ ให้ใช้คำอธิบายทั่วไปแทน · "
    "เสียงพลังงาน +30% ช่วง hook เท่านั้น ช่วงอธิบายกลับมาโทนปกติ",
    dict(risk_lines=[], warn_lines=[], verdict="เขียว",
         advice="ผ่าน ไม่มีคำในหมวดคำต้องห้าม เป็นเนื้อหาให้ความรู้วิธีอ่านฉลาก ไม่อวดอ้างสรรพคุณของ WISAMIN "
                 "เอง ไม่พาดพิงคู่แข่ง"),
)
pdf.add_page()

# ================= สคริปต์ B =================
render_script(
    "สคริปต์ B — เรื่องเล่า: ลูกค้าทักมาถามว่ากลัวโปรตีนตกฉลาก",
    ("ลูกค้าทักมาถามแบบนี้ทุกวัน", "อารมณ์ (+ข้อมูลรอง)", "TOFU", "Story/POV", "40 วิ"),
    "ลูกค้าทักมาถามแบบนี้ทุกวัน",
    [
        ("0:00-0:03", "HOOK",
         "อาทิตย์นี้มีคนทักแอดมินมาถามคำถามเดียวกันไม่ต่ำกว่า 20 ครั้ง",
         "ถ่ายหน้าจอแชท (เบลอชื่อ/รูปลูกค้าจริงเพื่อความเป็นส่วนตัว) สลับมาหน้าคนพูด"),
        ("0:03-0:15", "เล่าคำถาม",
         "เขาถามว่า 'พี่คะ โปรตีนพืชของ WISAMIN ตกฉลากเหมือนที่เป็นข่าวไหม' — ตกใจเหมือนกันตอนแรก "
         "แต่เข้าใจเลยว่าทำไมถึงถาม",
         "สีหน้าจริงจัง ไม่ยิ้มเกินจริง (ให้ความรู้สึกเข้าใจลูกค้าจริงๆ)",
         "Open loop: \"แล้วเราตอบเขาแบบนี้...\""),
        ("0:15-0:30", "ตอบแบบจริงใจ",
         "เราตอบตรงๆ ว่า ตอนนี้เรากำลังเตรียมผลแล็บให้ดูอยู่ ยังไม่พร้อมโชว์ก็จะไม่พูดมั่วๆ ไปก่อน "
         "เดี๋ยวพร้อมเมื่อไหร่จะบอกทุกคนที่นี่คนแรก",
         "กลับมาหน้าคนพูดเต็มจอ น้ำเสียงจริงใจ ไม่ hard sell",
         "Pattern change: ซูมเข้าใกล้กล้องเล็กน้อยตอนพูดประโยคนี้"),
        ("0:30-0:40", "CTA",
         "ถ้ามีคำถามแบบนี้ คอมเมนต์มาได้เลย เดี๋ยวทีมงานมาตอบเองทุกคำถาม", "—"),
    ],
    "ต้องมาจากคำถามลูกค้าจริง [เติมเรื่องจริงจากแอดมินเพจ] ถ้ายังไม่เคยมีคำถามแบบนี้จริง "
    "ให้ปรับเป็น \"คำถามที่เราเดาว่าหลายคนอยากถามแต่ไม่กล้าถาม\" แทน ไม่ใช้เรื่องแต่ง",
    dict(risk_lines=[],
         warn_lines=["ไม่พบคำต้องห้าม แต่มีความเสี่ยงนอกเหนือ อย. — ต้องอิงเหตุการณ์จริง (กฎ hb-4-content: "
                     "ห้ามกุ testimonial) ถ้ายังไม่เคยเกิดเหตุการณ์แบบนี้จริง ต้องปรับคำพูดเป็น "
                     "\"คำถามที่เราคิดว่าหลายคนอยากถาม\" แทน"],
         verdict="เขียว (ด้าน อย.) — ต้องเช็คความจริงของเนื้อเรื่องเองก่อนถ่าย",
         advice="ผ่านด้าน อย. เพราะไม่มีการอวดอ้างสรรพคุณ/ผลลัพธ์ใดๆ ทั้งสิ้น เป็นคอนเทนต์อารมณ์ล้วน"),
)
pdf.add_page()

# ================= สคริปต์ C =================
render_script(
    "สคริปต์ C — ไข่ขาว vs เวย์ vs โปรตีนพืช ต่างกันตรงไหน",
    ("โปรตีน 3 แบบ ต่างกันตรงไหน", "ข้อมูล", "TOFU", "Number/List", "50 วิ"),
    "โปรตีน 3 แบบ ต่างกันตรงไหน",
    [
        ("0:00-0:03", "HOOK",
         "ไข่ขาว เวย์ โปรตีนพืช 3 อย่างนี้ไม่เหมือนกัน เลือกผิดอาจไม่ตอบโจทย์ที่ตั้งใจไว้",
         "วางสินค้า 3 แบบเรียงกันบนโต๊ะ (ใช้ Egg White Protein ของ WISAMIN + กราฟิกแทนแบรนด์อื่น)"),
        ("0:03-0:18", "ไข่ขาว",
         "ไข่ขาวมีกรดอะมิโนจำเป็นครบทุกตัวในตัวเดียว ไขมันต่ำมาก เหมาะกับคนที่หลีกเลี่ยงนมหรือถั่วเหลือง "
         "แต่ถ้าหลีกเลี่ยงไข่อยู่แล้ว ตัวนี้ก็ไม่ตอบโจทย์เหมือนกัน",
         "เปิดถุง Egg White Protein โชว์เนื้อผง",
         "Open loop: \"ต่อมาคือเวย์...\""),
        ("0:18-0:32", "เวย์ (ข้อมูลทั่วไป ไม่พาดพิงแบรนด์)",
         "เวย์ดูดซึมไว เหมาะหลังออกกำลังกาย แต่มาจากนม คนแพ้แลคโตสต้องระวัง และตัวเลขโปรตีนต่อกรัมแตกต่างกันมาก"
         "ในแต่ละยี่ห้อ เพราะสูตรผสมไม่เหมือนกัน",
         "กราฟิกไอคอนนม (ไม่ใช้ผลิตภัณฑ์คู่แข่งจริง)",
         "Pattern change: ตัดไปมุมกล้องข้าง"),
        ("0:32-0:45", "โปรตีนพืช",
         "โปรตีนพืชเหมาะกับคนกินมังสวิรัติหรืออยากลดผลิตภัณฑ์จากสัตว์ ข้อสำคัญคือต้องเลือกสูตรที่ผสมพืชหลายแหล่ง "
         "ถึงจะได้กรดอะมิโนครบเหมือนโปรตีนสัตว์",
         "โชว์ Protein Plant ของ WISAMIN ชี้ที่ \"5 แหล่ง\" บนฉลาก"),
        ("0:45-0:50", "CTA", "เซฟไว้เทียบก่อนเลือกว่าตัวไหนตอบโจทย์เราที่สุด", "—"),
    ],
    "ข้อมูลโภชนาการทั่วไป ไม่ใช่ตัวเลขเฉพาะของ WISAMIN — ถ้าจะใส่ตัวเลขกรัมโปรตีนจริงของสินค้า WISAMIN เอง "
    "ต้องดึงจากฉลากบนแพ็กเกจจริงเท่านั้น",
    dict(risk_lines=[],
         warn_lines=["\"เหมาะกับคนที่แพ้นม แพ้ถั่วเหลือง\" (ฉบับร่างเดิม) — ก้ำกึ่งเล็กน้อยเพราะเข้าใกล้การพูดถึง"
                     "ภาวะแพ้ทางการแพทย์ — แก้เป็น \"หลีกเลี่ยงนม/ถั่วเหลือง\" แล้วในสคริปต์ฉบับนี้"],
         verdict="เขียว",
         advice="เนื้อหาเชิงเปรียบเทียบให้ความรู้ทั่วไป ไม่เคลมว่าตัวไหน \"ดีกว่า\" อีกแบบ ไม่พาดพิงแบรนด์คู่แข่ง"
                 "เจาะจง"),
)
pdf.add_page()

# ================= สคริปต์ D =================
h1("สคริปต์ D — ทำไม Gluta Colla Blink ราคาถึงเข้าถึงง่ายขนาดนี้")
callout(
    "**หมวดความเสี่ยงสูงที่สุดในเอกสารนี้:** กลูตาไธโอน/คอลลาเจนชนิดกิน (ไม่ใช่เครื่องสำอาง) "
    "ห้ามใช้คำว่า \"ผิวขาว\" \"ขาวใส\" \"ขาวขึ้น\" \"ผิวกระจ่างใส\" \"ลดฝ้า\" \"ลดจุดด่างดำ\" "
    "เด็ดขาดแม้แต่คำเดียว เพราะเป็นการอ้าง \"เปลี่ยนโครงสร้างร่างกาย\" ที่อาหารเสริมพูดไม่ได้ "
    "(มาตรา 40 พ.ร.บ.อาหาร) เสี่ยงจำคุกไม่เกิน 3 ปี หรือปรับไม่เกิน 30,000 บาท หรือทั้งจำทั้งปรับ "
    "สคริปต์นี้จึงใช้มุม \"ความโปร่งใสเรื่องราคา/ส่วนผสม\" ล้วนๆ แทน ไม่แตะผลลัพธ์ผิวเลย",
    BG_DANGER, DANGER)

script_meta_bar("ทำไมราคาเราเบากว่านี้ได้", "ธุรกิจ (+ข้อมูลรอง)", "BOFU", "Result First/Contrarian", "40 วิ")
text_on_screen("ทำไมราคาเราเบากว่านี้ได้")
for b in [
    ("0:00-0:03", "HOOK",
     "หลายคนถามว่าทำไม Gluta Colla Blink ราคาแค่นี้ ของแท้จริงไหม วันนี้ขอเล่าให้ฟังตรงๆ",
     "ถือซองสินค้าขึ้นมาจอเต็ม พลิกดูฉลากส่วนผสมทันที"),
    ("0:03-0:18", "Story: ทำไมตั้งราคานี้",
     "เราตั้งใจทำแพ็กเกจแบบซองเดี่ยว 28 กรัม แทนที่จะเป็นกระปุกใหญ่ราคาสูง เพื่อให้คนที่อยากลองก่อนตัดสินใจซื้อยาวๆ "
     "ทำได้ง่ายขึ้น เราตัดต้นทุนโฆษณาใหญ่ๆ ออก แล้วเอาเงินตรงนั้นมาทำราคาให้เข้าถึงง่ายแทน",
     "โชว์ซองเดี่ยว 5 รสวางเรียงกัน",
     "Open loop: \"แล้วในซองมีอะไรบ้าง...\""),
    ("0:18-0:32", "Benefit: ส่วนผสมที่พูดได้",
     "ในซองมีส่วนผสมของกลูตาไธโอนและคอลลาเจนซึ่งเป็นสารที่ร่างกายต้องการ ชงง่าย พกพาสะดวก มี 5 รสให้เลือกตามที่ชอบ "
     "เป็นทางเลือกสำหรับคนที่ดูแลตัวเองในชีวิตประจำวัน",
     "ชงตัวอย่าง 1 ซองให้ดูสด (โชว์เนื้อจริง ไม่ใช้กราฟิกลอย)",
     "Pattern change: ตัดมุมกล้องเป็นมุมบนขณะชง"),
    ("0:32-0:40", "CTA",
     "ผลลัพธ์ขึ้นกับแต่ละบุคคลและการดูแลตัวเองโดยรวมด้วยนะคะ ถ้าอยากรู้ราคาโปรวันนี้ คอมเมนต์ 'ราคา' มาได้เลย", "—"),
]:
    beat(*b)
production_note(
    "ห้ามต่อท้ายประโยคส่วนผสมด้วยผลลัพธ์ทางผิวใดๆ ทั้งสิ้น (ห้ามพูดว่า \"ทำให้ผิว...\") แม้แต่ทางอ้อม · "
    "ต้องพูด disclaimer \"ผลลัพธ์ขึ้นกับแต่ละบุคคล\" ทุกครั้งที่โพสต์ซ้ำ/ตัดคลิปสั้นลง")
audit_box(
    risk_lines=[],
    warn_lines=[
        "\"ของแท้จริงไหม\" ใน hook — ก้ำกึ่งเล็กน้อยถ้าตีความว่าโจมตี/พาดพิงว่าตลาดมีของปลอมเกลื่อน "
        "แต่บริบทนี้เป็นการตอบคำถามลูกค้าเรื่องราคา ไม่ใช่กล่าวหาแบรนด์คู่แข่ง ยังอยู่ในกรอบที่พูดได้",
        "ต้องเป็นเหตุผลราคาที่เป็นจริง (ตัดต้นทุนโฆษณา/แพ็กเกจซองเดี่ยว) — ยืนยันกับทีมงานก่อนถ่ายจริงว่าตรงกับ"
        "ความจริงของธุรกิจหรือไม่ [เติมเหตุผลจริงจากทีมถ้าไม่ตรง]",
    ],
    verdict="เขียว",
    advice="เลี่ยงคำเคลมผิว/ความขาวทั้งหมด ใช้มุม \"ความโปร่งใสเรื่องราคา/ส่วนผสม\" แทนทั้งคลิป และใส่ "
           "disclaimer ตามสูตรที่กำหนด — ปลอดภัยกว่าการพยายามเลี่ยงบาลีคำว่าขาวใสด้วยคำอื่น",
)
muted("ข้อจำกัดความรับผิด: การตรวจนี้เป็นการคัดกรองเบื้องต้นตามหลักเกณฑ์ อย. ที่เผยแพร่ทั่วไป "
      "ไม่ใช่คำวินิจฉัยทางกฎหมาย หากจะใช้คอนเทนต์นี้ยิงเป็นโฆษณาแบบเสียเงิน ต้องยื่นขออนุญาตโฆษณากับ อย. "
      "ก่อนตามมาตรา 41 และแสดงเลขที่ใบอนุญาตโฆษณาด้วย")
pdf.add_page()

# ================= ไอเดียสำรอง =================
h1("ไอเดียสำรอง (รอบหน้า)")
body("**Pea Fiber:** ต่อยอดจากธีมสุขภาพลำไส้ที่ WISAMIN เคยทำมาก่อน (ไซเลียมฮัสค์, Wemin Bio) — "
     "ทำเป็นซีรีส์เดียวกันได้")
body("**Chicken Protein:** มีจุดขาย \"ไฮโดรไลซ์\" (ย่อยง่ายกว่าโปรตีนปกติ) ที่ยังไม่ได้ใช้ในสคริปต์นี้ — "
     "เก็บไว้ทำคลิปข้อมูลเจาะลึกรอบหน้า")
pdf.ln(10)
hr(2, 3)
muted("จัดทำโดย Claude · โครงการ WISAMIN Competitor Radar & Content · "
      "content/2026-07-15_content-plan-scripts.md")

pdf.output(OUT)
print(f"สร้าง PDF แล้ว: {OUT}")
