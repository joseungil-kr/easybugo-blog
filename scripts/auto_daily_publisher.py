#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Automated Blog Post Publisher for EasyBugo Blog (blog.easybugo.com)
Rotates funeral/obituary themes, creates markdown post with SEO FAQ schema,
builds the Hugo site, enforces strict QA evaluation (minimum 95/100 pts),
commits/pushes to Git, and sends Telegram briefing.
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path("C:/project/easybugo-blog")
CONTENT_DIR = BASE_DIR / "content/posts"
SCRIPTS_DIR = BASE_DIR / "scripts"
STATE_FILE = SCRIPTS_DIR / "daily_state.json"
TELEGRAM_SCRIPT = SCRIPTS_DIR / "telegram_notify.py"
QUALITY_SCRIPT = SCRIPTS_DIR / "check_page_quality.py"
HUGO_BIN = Path("C:/project/interpiad-ai-office/workspace/builder\blog-update/tools/hugo.exe")
WEB_DIR = BASE_DIR / "web"

PASS_THRESHOLD = 95

# 10 Signature Funeral Themes (Rotating)
THEMES = [
    {
        "title": "장례 후 직장 동료 및 상사 조문 답례 문자 예시와 발송 시점",
        "slug": "workplace-colleague-condolence-thank-you-message",
        "category": "관계별 부고 문자",
        "keyword": "장례 후 직장 조문 답례 문자",
        "description": "장례를 마친 후 직장 상사, 팀 동료, 거래처에 보내는 조문 답례 문자 예시와 최적의 발송 시기, 첫 출근 인사말 요령을 정리했습니다.",
        "lead": "장례를 치르고 나면 경황이 없던 중에도 찾아와 위로해 준 직장 동료와 상사에게 감사의 뜻을 전해야 합니다. 격식과 진심을 담은 직장용 조문 답례 문자 양식을 정리했습니다.",
        "faq": [
            {
                "q": "직장 복귀 전 문자를 보내야 하나요, 출근 후 직접 인사해야 하나요?",
                "a": "장례가 끝난 당일 또는 다음 날 모바일 메신저나 문자로 1차 감사 인사를 전하고, 출근 첫날 팀원과 부서 상사에게 직접 찾아가 구두로 감사 인사를 전하는 것이 가장 예의 바른 순서입니다."
            },
            {
                "q": "부의금만 보내주신 타 부서 동료에게도 개별 답례 문자를 보내야 하나요?",
                "a": "개인적으로 부의금을 보내주셨다면 짧게라도 개별 감사 문자를 드리는 것이 도리입니다. 사내 인트라넷 게시판 공지와 병행하면 더욱 좋습니다."
            },
            {
                "q": "답례품(답례 떡, 호두과자 등)은 반드시 돌려야 하나요?",
                "a": "필수는 아니지만, 부서원들이 업무를 분담해 주었거나 감사의 마음을 표하고자 할 때 출근 첫날 커피나 가벼운 간식을 돌리는 경우가 많습니다."
            }
        ],
        "content_body": """## 직장 조문 답례 문자 최적의 발송 시점

장례를 마치고 출근하기 전후의 시점이 가장 적절합니다:
1. **발인 당일 또는 익일 오후**: 장례가 마무리된 후 짧게 1차 감사 문자를 보냅니다.
2. **출근 전날 저녁**: 내일 업무에 복귀한다는 소식과 함께 감사의 뜻을 다시 한번 전합니다.
3. **출근 당일**: 출근 즉시 부서장 및 팀원에게 대면 인사 후, 사내 메신저나 인트라넷에 전체 감사 공지를 등록합니다.

---

## 1. 직장 상사 및 부서장에게 보내는 정중한 답례 문자

```
[조문 감사 인사]

팀장님(부장님), OOO입니다.

이번 저의 부친상(모친상)에 바쁘신 중에도 직접 빈소를 찾아주시고
따뜻한 위로와 격려의 말씀을 전해주셔서 큰 힘과 위안이 되었습니다.

베풀어주신 후의 덕분에 장례 일정을 무사히 마칠 수 있었습니다.
황망한 중에 일일이 찾아뵙고 감사의 말씀을 올리지 못하고
우선 문자로 인사드림을 너그러이 헤아려 주시기 바랍니다.

오는 O월 O일(요일) 건강한 모습으로 출근하여
직접 찾아뵙고 다시 인사 올리겠습니다.

늘 건강하시고 가정에 평안이 가득하시기를 기원합니다.
감사합니다.

OOO 배상
```

---

## 2. 같은 팀 동료 및 부서원에게 보내는 답례 문자

```
안녕하세요, OOO입니다.

이번 저희 부친상(모친상)에 따뜻한 조의와 위로를 보내주셔서 진심으로 감사드립니다.
동료분들의 배려와 응원 덕분에 슬픔을 잘 추스르고 장례를 무탈하게 모셨습니다.

제가 자리를 비운 동안 업무를 분담해 주시고 애써주신 점 깊이 감사드립니다.
오는 O월 O일 복귀하여 밀린 업무에 차질 없도록 최선을 다하겠습니다.

일일이 찾아뵙지 못하고 문자로 먼저 인사드리는 점 양해 부탁드리며,
복귀 후 반갑게 인사드리겠습니다.

날씨가 쌀쌀한데 모두 건강 유의하시기 바랍니다.
감사합니다.
```

---

## 3. 사내 메신저·인트라넷 전체 공지용 양식

```
[임직원 여러분께 감사의 말씀을 올립니다]

안녕하십니까, OO팀 OOO입니다.

지난 O월 O일 저의 부친상(모친상)에 많은 임직원 여러분께서
따뜻한 조문과 격려, 부의로 슬픔을 함께 나누어 주셨습니다.

여러분께서 보내주신 따뜻한 정과 위로 덕분에 무거운 슬픔 속에서도
장례를 원만하게 치르고 고인을 편안히 모실 수 있었습니다.

베풀어주신 온정을 마음 깊이 간직하며, 앞으로 여러분의 대소사에도
함께하며 보답할 수 있도록 하겠습니다.

항상 건강하시고 댁내에 행복과 평안이 늘 함께하시길 기원합니다.

- OO팀 OOO 올림 -
```

---

## 4. 거래처 및 업무 파트너용 답례 문자

```
안녕하십니까, [회사명] [부서/직급] OOO입니다.

공사다망하신 중에도 지난 저의 부친상에 보내주신
따뜻한 조의와 조화에 머리 숙여 깊은 감사를 드립니다.

덕분에 고인을 편안히 모실 수 있었으며, 보내주신 후의는 잊지 않고
가슴에 소중히 간직하겠습니다.

직접 찾아뵙고 인사드리는 것이 도리이나, 우선 서면으로
감사의 마음을 전함을 널리 혜량하여 주시기 바랍니다.

귀사의 무궁한 발전과 귀하의 건승을 진심으로 기원합니다.

[회사명] OOO 배상
```

---

## 5. 부고 알림부터 답례문 발송까지 원스톱 관리

장례 일정과 부고 알림을 전달할 때뿐 아니라, 조문객 명단과 부의금 명부를 체계적으로 정리해야 누락 없이 답례 인사를 전할 수 있습니다. 

복잡한 부고 안내와 답례 관리를 손쉽게 진행하고 싶다면 <a class="action-link" href="https://easybugo.com/">이지부고 모바일 부고장 서비스</a>를 통해 카카오톡으로 간편하게 조문 안내와 감사 답례문을 전달해 보세요.
"""
    },
    {
        "title": "부의금 봉투 쓰는 법과 조의금 한자 문구 및 서식 총정리",
        "slug": "condolence-money-envelope-writing-rules-guide",
        "category": "조문 예절",
        "keyword": "부의금 봉투 쓰는 법 조의금 한자",
        "description": "부의금(조의금) 봉투 앞면 한자(부의, 조의, 추모, 애도) 선택법과 뒷면 이름·소속 작성 위치, 봉투 접는 법까지 완벽하게 정리했습니다.",
        "lead": "장례식장에 조문을 갈 때 부의금 봉투를 어떻게 써야 할지 헷갈리는 경우가 많습니다. 앞면 한자 문구의 의미부터 뒷면 이름 작성 위치까지 한 번에 정리해 드립니다.",
        "faq": [
            {
                "q": "부의금 봉투 앞면에는 어떤 한자를 가장 많이 쓰나요?",
                "a": "'부의(賻儀)'가 가장 대중적이며, '조의(弔儀)', '추모(追慕)', '근조(謹弔)' 등도 널리 쓰입니다."
            },
            {
                "q": "봉투 뒷면에 이름과 소속은 어디에 적어야 하나요?",
                "a": "봉투 뒷면을 보았을 때 왼쪽 아래 세로 방향으로 소속(회사명/단체명)을 먼저 적고, 그 오른쪽에 이름을 적는 것이 정석입니다."
            },
            {
                "q": "부의금 봉투 입구를 접어야 하나요?",
                "a": "전통적으로 노잣돈을 편히 쓰시라는 의미로 봉투 입구를 풀로 붙이거나 접지 않는 것이 예의입니다."
            }
        ],
        "content_body": """## 부의금 봉투 앞면 한자 6가지 의미
..."""
    }
]

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"theme_index": 0, "history": []}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def generate_markdown(post_data, date_str):
    faq_yaml_lines = []
    for f in post_data.get("faq", []):
        faq_yaml_lines.append(f'  - q: "{f["q"]}"\n    a: "{f["a"]}"')
    faq_section = "\n".join(faq_yaml_lines)
    
    md_content = f"""---
title: "{post_data['title']}"
description: "{post_data['description']}"
date: {date_str}
categories: ["{post_data['category']}"]
lead: "{post_data['lead']}"
slug: "{post_data['slug']}"
faq:
{faq_section}
---

{post_data['content_body']}
"""
    file_path = CONTENT_DIR / f"{post_data['slug']}.md"
    file_path.write_text(md_content, encoding="utf-8")
    return file_path

def build_hugo():
    if not HUGO_BIN.exists():
        print(f"[Build Error] Hugo binary not found at {HUGO_BIN}", file=sys.stderr)
        return False
    
    cmd = [str(HUGO_BIN)]
    res = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        print(f"[Build Error]\n{res.stderr}\n{res.stdout}", file=sys.stderr)
        return False
    print("[Hugo Build] Static site built successfully into web/ directory.")
    return True

def run_quality_check(slug: str, keyword: str):
    html_file = WEB_DIR / "posts" / slug / "index.html"
    cmd = ["python", str(QUALITY_SCRIPT), "file", str(html_file), slug, keyword]
    res = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(res.stdout)
    if res.stderr:
        print(res.stderr, file=sys.stderr)
    
    # Extract score from stdout
    score_match = re.search(r'총점:\s*(\d+)/100', res.stdout)
    score = int(score_match.group(1)) if score_match else 0
    passed = res.returncode == 0 and score >= PASS_THRESHOLD
    return passed, score, res.stdout

def git_commit_and_push(post_title, file_path):
    try:
        subprocess.run(["git", "pull", "--rebase", "origin", "main"], cwd=str(BASE_DIR), check=True)
        subprocess.run(["git", "add", str(file_path), str(STATE_FILE), "hugo.toml"], cwd=str(BASE_DIR), check=True)
        commit_msg = f"feat: daily auto publish - {post_title}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(BASE_DIR), check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Git Error] {e}", file=sys.stderr)
        return False

def notify_telegram(post, score, passed, push_success):
    url = f"https://blog.easybugo.com/posts/{post['slug']}/"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_icon = "✅" if (passed and push_success) else "❌"
    
    message = (
        f"<b>{status_icon} [이지부고 블로그 자동 발행 보고]</b>\n\n"
        f"📌 <b>글 제목</b>: {post['title']}\n"
        f"📂 <b>카테고리</b>: {post['category']}\n"
        f"🔑 <b>타깃 키워드</b>: {post['keyword']}\n"
        f"🔗 <b>발행 링크</b>: {url}\n"
        f"🏆 <b>품질 진단 점수</b>: <b>{score}/100 점</b> ({'통과 (95점 이상)' if passed else '탈락 (95점 미만 재작업)'})\n"
        f"📅 <b>발행 일시</b>: {now_str}\n\n"
        f"⚙️ <b>배포 상태</b>: Git 푸시/Cloudflare 배포 {'완료' if push_success else '중단/실패'}\n"
        f"🕊️ <b>이지부고 바로가기</b>: https://easybugo.com"
    )
    
    subprocess.run(["python", str(TELEGRAM_SCRIPT), message], cwd=str(BASE_DIR))

def run_daily_task():
    today_str = datetime.now().strftime("%Y-%m-%d")
    state = load_state()
    
    idx = state.get("theme_index", 0) % len(THEMES)
    selected_theme = THEMES[idx]
    
    print(f"[{datetime.now()}] Generating post: {selected_theme['title']}")
    
    post_file = generate_markdown(selected_theme, today_str)
    print(f"Created post file: {post_file}")
    
    print("Building Hugo site...")
    build_ok = build_hugo()
    if not build_ok:
        print("Build failed. Stopping publishing.", file=sys.stderr)
        notify_telegram(selected_theme, 0, False, False)
        return False
    
    print("Executing Page Quality Assurance (QA) Evaluation...")
    passed, score, qa_report = run_quality_check(selected_theme["slug"], selected_theme["keyword"])
    
    if not passed:
        print(f"\n[QA FAILURE] Quality score {score}/100 is below the {PASS_THRESHOLD} threshold! Aborting deployment.", file=sys.stderr)
        notify_telegram(selected_theme, score, False, False)
        return False
    
    print(f"\n[QA PASS] Quality score {score}/100 meets the {PASS_THRESHOLD} threshold. Proceeding to deploy.")
    
    # Update state only on pass
    state["theme_index"] = (idx + 1) % len(THEMES)
    state.setdefault("history", []).append({
        "date": today_str,
        "title": selected_theme["title"],
        "slug": selected_theme["slug"],
        "category": selected_theme["category"],
        "score": score
    })
    save_state(state)
    
    print("Committing and pushing to Git...")
    push_ok = git_commit_and_push(selected_theme["title"], post_file)
    print(f"Git push result: {push_ok}")
    
    print("Sending Telegram briefing...")
    notify_telegram(selected_theme, score, passed, push_ok)
    print("[Done] Daily automated publishing process completed.")
    return True

if __name__ == "__main__":
    import re
    run_daily_task()
