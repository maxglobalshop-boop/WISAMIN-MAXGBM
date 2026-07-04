#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
new_report.py — สร้างโครงรายงานเปล่าสำหรับวันนี้ (หรือวันที่ระบุ)
ใช้: python3 collector/new_report.py [YYYY-MM-DD]
"""
import json, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "data", "reports")

date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
path = os.path.join(REPORTS, f"{date}.json")

if os.path.exists(path):
    print(f"มีไฟล์อยู่แล้ว: {path} (ไม่เขียนทับ)")
    sys.exit(0)

skeleton = {
    "date": date,
    "generated_at": date,
    "brand": "WISAMIN",
    "brand_categories": ["โปรตีนพืช", "คอลลาเจน", "พรีไบโอติก/ลำไส้", "คุมน้ำหนัก/ชาเขียว", "วิตามิน"],
    "summary": {
        "headline": "<สรุปประเด็นเด่นของวัน 1 ประโยค>",
        "top_theme": "<ธีมคอนเทนต์ที่มาแรงวันนี้>",
        "channel_counts": {"TikTok": 0, "Facebook": 0, "YouTube": 0, "X": 0},
        "note_on_metrics": "จัดระดับ engagement เชิงคุณภาพ (viral/high/medium)"
    },
    "competitors": [
        {
            "brand": "<ชื่อคู่แข่ง>",
            "category": "<หมวด>",
            "channel": "TikTok | Facebook | YouTube | X",
            "creator": "<@ครีเอเตอร์/เพจ>",
            "title": "<หัวข้อคอนเทนต์>",
            "url": "https://...",
            "engagement_tier": "viral | high | medium",
            "format": "<รูปแบบคอนเทนต์>",
            "why_it_works": "<ทำไมปัง>",
            "threat_to_wisamin": "สูง | กลาง | ต่ำ — <เหตุผล>"
        }
    ],
    "insights": [
        {"insight": "<insight>", "evidence": "<หลักฐาน>", "opportunity": "<โอกาส WISAMIN>"}
    ],
    "content_ideas": [
        {"idea": "<ไอเดีย>", "hook": "<ประโยคเปิด>", "format": "<รูปแบบ>",
         "cta": "<CTA>", "fda_safe": True, "counters_competitor": "<ชนคู่แข่งเจ้าไหน>"}
    ],
    "trends": ["<เทรนด์ 1>"]
}

os.makedirs(REPORTS, exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    json.dump(skeleton, f, ensure_ascii=False, indent=2)
print(f"✓ สร้างโครงรายงาน: {path}")
print("  กรอกข้อมูลคอนเทนต์คู่แข่งใหม่ แล้วรัน python3 build.py")
