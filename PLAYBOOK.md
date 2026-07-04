# 🧭 PLAYBOOK — Agent เฝ้าคู่แข่ง WISAMIN (รันทุกวัน)

เอกสารนี้คือ "สมอง" ของ Agent รายวัน ใช้เป็นคำสั่งให้ Claude (หรือ scheduled cloud agent) ทำงานซ้ำได้ทุกวันโดยได้ **คอนเทนต์ใหม่จริง ไม่ซ้ำของเดิม**

---

## 🎯 เป้าหมายแต่ละวัน
หา **คอนเทนต์คู่แข่งอาหารเสริมไทยที่ใหม่ + คนดู/มีส่วนร่วมเยอะ** ในรอบ ~24-72 ชม. จาก **TikTok / Facebook / YouTube / X** แล้วสรุปเป็นรายงาน + ไอเดียต่อยอดให้ WISAMIN

## 🏷️ WISAMIN แข่งในหมวดไหน (โฟกัสที่นี่)
1. โปรตีนพืช (plant protein)
2. คอลลาเจน / ผิวใส
3. พรีไบโอติก / ลำไส้ / ขับถ่าย (Wemin Bio)
4. คุมน้ำหนัก / ชาเขียว (MINTEA)
5. วิตามินทั่วไป

## 🔎 ชุดคำค้นมาตรฐาน (หมุนใช้ + เติมชื่อแบรนด์คู่แข่งที่เจอ)
รันผ่านเครื่องมือ WebSearch (ปรับปีให้เป็นปีปัจจุบันเสมอ):
- `คอลลาเจน ไวรัล TikTok ไทย รีวิว <เดือน ปี>`
- `พรีไบโอติก ลำไส้ ขับถ่าย อาหารเสริม TikTok ไทย ล่าสุด`
- `โปรตีนพืช โปรตีนชง รีวิว ไทย ขายดี`
- `อาหารเสริมลดน้ำหนัก คุมหิว ไวรัล TikTok Facebook`
- `<ชื่อคู่แข่ง> รีวิว TikTok` (เช่น FRESH DOZE, AKANE, Glory Collagen, ชาเม่, Woma Balance)
- `อาหารเสริม โฆษณา โดนจับ อย. <ปี>` (จับเทรนด์กฎ/ความเสี่ยง)
- `supplement Thailand viral TikTok <month year>` (มุมภาษาอังกฤษ)
- **X/Twitter:** `<ชื่อแบรนด์> รีวิว site:x.com` หรือค้น `อาหารเสริม รีวิว x.com`

### รายชื่อคู่แข่งที่รู้จักแล้ว (ใช้ค้นต่อ + เฝ้าเพจ)
FRESH DOZE · AKANE · Glory Collagen · ชาเม่ (Chame) · Woma Balance · Colon Man · Nutrilite · Amsel · Vistra · Blackmores · Donutt · Nara · Colligi · MOVE Protein · Benefit

### KOL/หมอที่ต้องเฝ้า (แม่แบบคอนเทนต์)
`@drjade_health` (หมอเจด) · `@doctoram.gastro` (หมอแอม) · `@pimrypie__tiktok` (พิมรี่พาย)

## ✅ เกณฑ์คัดคอนเทนต์เข้ารายงาน
- โพสต์/วิดีโอ **ใหม่** (ไม่อยู่ในรายงานวันก่อน — เช็คไฟล์ `data/reports/` ย้อนหลัง)
- มีสัญญาณ engagement สูง (ยอดวิว/ไลก์/คอมเมนต์เยอะ, ติดแท็ก/discover, ถูกอ้างซ้ำ)
- เกี่ยวกับหมวดที่ WISAMIN แข่ง
- **ต้องแนบลิงก์จริงที่กดเข้าได้เสมอ**

## 🚫 กันข้อมูลซ้ำ (สำคัญมาก ผู้ใช้ย้ำ)
ก่อนบันทึก ให้เปิดไฟล์ `data/reports/*.json` ทั้งหมด แล้วตัด URL/หัวข้อที่เคยรายงานไปแล้วออก — รายงานใหม่ต้องมีของใหม่เท่านั้น

## 📊 การเก็บตัวเลข engagement ให้แม่นยำ (อัปเกรดในอนาคต)
รอบพื้นฐานใช้การจัดระดับเชิงคุณภาพ: `viral` / `high` / `medium`
ถ้าต้องการตัวเลขเป๊ะ ให้เชื่อม API (ใส่ key ใน `collector/.env`):
- **YouTube:** YouTube Data API v3 (`videos?part=statistics`) — ฟรี มีโควตา
- **TikTok:** TikTok Display API / หรือ scraper อย่าง Apify TikTok Scraper
- **Facebook:** Graph API (ต้องมีสิทธิ์เพจ) — ดึงเฉพาะเพจคู่แข่งที่เป็น public
- **X:** X API v2 (`tweets?tweet.fields=public_metrics`)

## 📝 ขั้นตอนทำรายงานประจำวัน
1. `python3 collector/new_report.py` → ได้ไฟล์ `data/reports/<วันนี้>.json` (โครงเปล่า)
2. รันคำค้นด้านบน → คัดคอนเทนต์ใหม่ 6-12 ชิ้น → กรอกลง JSON (ดูสคีมาใน README)
3. เขียน `insights` (Customer Insight) 3-4 ข้อ + `content_ideas` 3-4 ข้อ (ต่อยอด TikTok WISAMIN, ปลอดคำ อย. — ใช้ Skill `fda-thai` ตรวจ)
4. `python3 build.py` → รีเจน `index.html`
5. เปิด `index.html` ดูผล + อัปเดต `AUDIT.md`

## 🧪 Self-Audit ทุกครั้ง (เพื่อพัฒนาต่อเนื่อง — /loop)
ถามตัวเองแล้วบันทึกใน AUDIT.md:
- ครบทั้ง 4 ช่องทางไหม? (ช่องที่ยังอ่อน = X, YouTube → ต้องหาเพิ่ม)
- คอนเทนต์ใหม่จริง ไม่ซ้ำวันก่อน?
- ไอเดียต่อยอด "ทำได้จริงพรุ่งนี้" ไหม? มี hook + CTA + ปลอด อย.?
- ตัวเลข engagement น่าเชื่อถือขึ้นได้อีกไหม?
