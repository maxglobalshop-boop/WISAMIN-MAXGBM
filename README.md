# 🛰️ WISAMIN Competitor Radar

Dashboard + Agent เฝ้าติดตามคอนเทนต์คู่แข่งอาหารเสริมไทย (TikTok / Facebook / YouTube / X)
ทำงานรายวัน → รายงานคอนเทนต์ไวรัลของคู่แข่ง + Customer Insight + ไอเดียต่อยอดคอนเทนต์ TikTok WISAMIN

## 🚀 เปิดใช้งาน (ง่ายสุด)
เปิดไฟล์ **`index.html`** ด้วยเบราว์เซอร์ (ดับเบิลคลิกได้เลย) — เป็นไฟล์ self-contained ข้อมูลฝังในตัว ไม่ต้องต่อเน็ต/เซิร์ฟเวอร์

Dashboard มี 4 แท็บ:
- 📡 **คอนเทนต์คู่แข่ง** — การ์ดคอนเทนต์จริง เห็นแบรนด์/ช่องทาง/ยอด engagement/ลิงก์ + ระดับภัยต่อ WISAMIN (กรองตามช่องทางได้)
- 🧠 **Customer Insight** — วิเคราะห์ความต้องการลูกค้า + โอกาสของ WISAMIN
- 💡 **ไอเดียคอนเทนต์** — สคริปต์ต่อยอด TikTok พร้อม hook + CTA + ตราปลอดคำต้องห้าม อย.
- 📈 **เทรนด์** — ทิศทางคอนเทนต์ที่กำลังมา

## 📁 โครงสร้าง
```
index.html              ← Dashboard (เปิดอันนี้)
build.py                ← สร้าง index.html จากรายงานทั้งหมด
PLAYBOOK.md             ← สมองของ Agent: วิธีหาข้อมูลรายวัน + คำค้น + เกณฑ์
AUDIT.md                ← บันทึกการพัฒนา/ตรวจงานต่อเนื่อง (/loop)
data/reports/           ← รายงานรายวัน (1 ไฟล์ = 1 วัน)
  2026-07-04.json
collector/
  new_report.py         ← สร้างโครงรายงานวันใหม่
  serve.py              ← เสิร์ฟ dashboard สำหรับพรีวิว (ออปชัน)
```

## 🔄 รอบงานรายวัน (Agent)
```bash
python3 collector/new_report.py      # 1) สร้างโครงรายงานวันนี้
#    2) หาคอนเทนต์คู่แข่งใหม่ตาม PLAYBOOK.md แล้วกรอกลง data/reports/<วันนี้>.json
python3 build.py                     # 3) รีเจน index.html
open index.html                      # 4) ดูผล
```

> **ข้อมูลใหม่เท่านั้น:** ก่อนบันทึก ระบบ/Agent จะเทียบกับรายงานย้อนหลังใน `data/reports/` เพื่อไม่เอาคอนเทนต์เดิมมาแจ้งซ้ำ

## ⏰ ตั้งให้ทำงานอัตโนมัติทุกวัน
มี 3 ทางเลือก (แนะนำข้อ 1):
1. **Claude scheduled agent** — พิมพ์ `/schedule` แล้วตั้งให้รัน PLAYBOOK ทุกเช้า (Claude จะค้นเว็บ กรอกรายงาน และ build ให้อัตโนมัติ)
2. **/loop** — สั่ง `/loop` ให้ Claude วนปรับปรุงคุณภาพ + audit เอง (โหมดที่กำลังใช้อยู่)
3. **cron เครื่องตัวเอง** — ตั้ง cron รัน `build.py` (ต้องมีคน/สคริปต์กรอกรายงานก่อน)

## 🧾 สคีมา JSON ของแต่ละคอนเทนต์
```json
{
  "brand": "ชื่อคู่แข่ง", "category": "หมวด",
  "channel": "TikTok|Facebook|YouTube|X",
  "creator": "@ครีเอเตอร์", "title": "หัวข้อ", "url": "ลิงก์จริง",
  "engagement_tier": "viral|high|medium",
  "format": "รูปแบบ", "why_it_works": "ทำไมปัง",
  "threat_to_wisamin": "สูง|กลาง|ต่ำ — เหตุผล"
}
```

## 🔗 อ้างอิงแบรนด์
- WISAMIN TikTok: https://www.tiktok.com/@wisamin_official
- WISAMIN Shop (FB): https://www.facebook.com/wisaminshop
