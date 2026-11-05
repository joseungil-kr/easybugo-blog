#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Page Quality Assurance (QA) Evaluator for EasyBugo Blog (blog.easybugo.com)
Evaluates SEO, AEO, meta integrity, content volume, and CTA against a 100-point scale.
Threshold: Minimum 95 points required to pass.
"""

import sys
import re
import urllib.request
from pathlib import Path

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

PASS_THRESHOLD = 95

def evaluate_html(html_content: str, slug: str, target_keyword: str = "") -> dict:
    score = 100
    deductions = []
    details = {}

    # 1. Basic HTTP & Meta Integrity (25 pts)
    # Check UTF-8 charset
    has_charset = bool(re.search(r'<meta[^>]*charset=["\']?utf-8', html_content, re.IGNORECASE))
    if not has_charset:
        score -= 5
        deductions.append("[-5점] UTF-8 문자셋 선언 누락")
    
    # Check viewport
    has_viewport = bool(re.search(r'<meta[^>]*name=["\']?viewport["\']?', html_content, re.IGNORECASE))
    if not has_viewport:
        score -= 5
        deductions.append("[-5점] Viewport 메타 태그 누락")

    # Check canonical
    canonical_match = re.search(r'<link[^>]*rel=["\']?canonical["\']?[^>]*href=["\']?([^"\'\s>]+)', html_content, re.IGNORECASE)
    if not canonical_match:
        canonical_match = re.search(r'<link[^>]*href=["\']?([^"\'\s>]+)[^>]*rel=["\']?canonical["\']?', html_content, re.IGNORECASE)
    
    if canonical_match:
        canonical_url = canonical_match.group(1).strip()
        expected_part = f"/posts/{slug}/"
        if expected_part not in canonical_url:
            score -= 10
            deductions.append(f"[-10점] Canonical URL 불일치 (기대값: {expected_part}, 실제: {canonical_url})")
        details["canonical"] = canonical_url
    else:
        score -= 10
        deductions.append("[-10점] Canonical 태그 누락")
        details["canonical"] = "MISSING"

    # 2. SEO Title & Description Optimization (25 pts)
    # Title check
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
    if title_match:
        title_text = title_match.group(1).strip()
        details["title"] = title_text
        if len(title_text) < 15:
            score -= 5
            deductions.append(f"[-5점] Title 길이 부족 ({len(title_text)}자, 권장: 15~55자)")
        elif len(title_text) > 65:
            score -= 3
            deductions.append(f"[-3점] Title 길이 초과 ({len(title_text)}자, 권장: 15~55자)")
        if "이지부고" not in title_text:
            score -= 2
            deductions.append("[-2점] Title에 브랜드('이지부고') 미포함")
    else:
        score -= 10
        deductions.append("[-10점] Title 태그 누락")
        details["title"] = "MISSING"

    # Meta Description check
    desc_match = re.search(r'<meta[^>]*name=["\']?description["\']?[^>]*content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    if not desc_match:
        desc_match = re.search(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']?description["\']?', html_content, re.IGNORECASE)
    
    if desc_match:
        desc_text = desc_match.group(1).strip()
        details["description"] = desc_text
        if len(desc_text) < 60:
            score -= 5
            deductions.append(f"[-5점] Meta Description 길이 부족 ({len(desc_text)}자, 권장: 60~160자)")
        elif len(desc_text) > 170:
            score -= 2
            deductions.append(f"[-2점] Meta Description 길이 초과 ({len(desc_text)}자, 권장: 60~160자)")
    else:
        score -= 10
        deductions.append("[-10점] Meta Description 누락")
        details["description"] = "MISSING"

    # Open Graph check
    has_og_title = bool(re.search(r'<meta[^>]*property=["\']?og:title["\']?', html_content, re.IGNORECASE))
    has_og_desc = bool(re.search(r'<meta[^>]*property=["\']?og:description["\']?', html_content, re.IGNORECASE))
    if not (has_og_title and has_og_desc):
        score -= 5
        deductions.append("[-5점] Open Graph 메타 태그(og:title 또는 og:description) 누락")

    # 3. Content Volume & AEO Structure (30 pts)
    # Text length (strip html tags)
    clean_text = re.sub(r'<[^>]+>', ' ', html_content)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    text_length = len(clean_text)
    details["text_length"] = text_length

    if text_length < 800:
        score -= 10
        deductions.append(f"[-10점] 실질 텍스트 분량 심각 부족 ({text_length}자 / 권장 1,200자 이상)")
    elif text_length < 1200:
        score -= 5
        deductions.append(f"[-5점] 실질 텍스트 분량 다소 부족 ({text_length}자 / 권장 1,200자 이상)")

    # Heading hierarchy check
    h1_count = len(re.findall(r'<h1[^>]*>', html_content, re.IGNORECASE))
    h2_count = len(re.findall(r'<h2[^>]*>', html_content, re.IGNORECASE))
    details["h1_count"] = h1_count
    details["h2_count"] = h2_count

    if h1_count == 0:
        score -= 5
        deductions.append("[-5점] H1 제목 태그 누락")
    if h2_count < 2:
        score -= 5
        deductions.append(f"[-5점] H2 소제목 부족 ({h2_count}개, 최소 2개 이상 필요)")

    # AEO FAQ structure check (FAQ in Schema, class or Q&A patterns)
    has_faq = bool(
        "faq" in html_content.lower() or
        "schema.org/Question" in html_content or
        re.search(r'Q\.|질문|자주 묻는', html_content)
    )
    if not has_faq:
        score -= 10
        deductions.append("[-10점] AEO FAQ 구조화 요소 또는 질의응답 블록 누락")

    # 4. Conversion & Integrity (20 pts)
    # Check EasyBugo CTA link
    has_cta = bool("easybugo.com" in html_content)
    if not has_cta:
        score -= 10
        deductions.append("[-10점] 이지부고 메인 CTA 링크(easybugo.com) 누락")

    # Check for placeholder residuals (e.g. TODO, FIXME, undefined, null)
    has_placeholders = bool(re.search(r'\b(TODO|FIXME|TBD|PLACEHOLDER|UNDEFINED)\b', html_content, re.IGNORECASE))
    if has_placeholders:
        score -= 5
        deductions.append("[-5점] 미처리 개발 임시 문자열(TODO 등) 잔존")

    # Check template format blocks (e.g. pre, code, or blockquote)
    has_templates = bool(re.search(r'<(pre|code|blockquote)[^>]*>', html_content, re.IGNORECASE))
    if not has_templates:
        score -= 5
        deductions.append("[-5점] 복사 가능한 서식 템플릿(pre/code/blockquote 블록) 누락")

    details["score"] = max(0, score)
    details["pass"] = score >= PASS_THRESHOLD
    details["deductions"] = deductions
    return details

def check_file(file_path: Path, slug: str, keyword: str = "") -> dict:
    if not file_path.exists():
        return {
            "score": 0,
            "pass": False,
            "deductions": [f"[-100점] HTML 파일 미존재: {file_path}"]
        }
    html = file_path.read_text(encoding="utf-8")
    return evaluate_html(html, slug, keyword)

def check_url(url: str, slug: str, keyword: str = "") -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status != 200:
                return {
                    "score": 0,
                    "pass": False,
                    "deductions": [f"[-100점] HTTP 응답 오류: {resp.status}"]
                }
            html = resp.read().decode("utf-8")
            return evaluate_html(html, slug, keyword)
    except Exception as e:
        return {
            "score": 0,
            "pass": False,
            "deductions": [f"[-100점] HTTP 요청 실패: {e}"]
        }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python check_page_quality.py [file|url] [path_or_url] [slug] [keyword]")
        sys.exit(1)

    mode = sys.argv[1]
    target = sys.argv[2]
    slug = sys.argv[3] if len(sys.argv) > 3 else ""
    keyword = sys.argv[4] if len(sys.argv) > 4 else ""

    if mode == "file":
        result = check_file(Path(target), slug, keyword)
    elif mode == "url":
        result = check_url(target, slug, keyword)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)

    score = result["score"]
    passed = result["pass"]

    print("\n" + "=" * 50)
    print(f"📋 [이지부고 품질 진단 리포트] 대상: {slug}")
    print(f"🏆 총점: {score}/100 점")
    print(f"🚦 결과: {'✅ PASS (합격)' if passed else '❌ FAIL (불합격 - 95점 미만 재작업 필요)'}")
    print("=" * 50)

    if result.get("deductions"):
        print("\n🔍 감점 내역:")
        for d in result["deductions"]:
            print(f"  • {d}")
    else:
        print("\n🎉 감점 요인 없음! 완벽한 품질 기준 충족.")

    print("=" * 50 + "\n")

    sys.exit(0 if passed else 1)
