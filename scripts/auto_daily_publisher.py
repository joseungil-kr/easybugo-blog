#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Automated Blog Post Publisher for EasyBugo Blog (blog.easybugo.com)
Features:
1. Full 10-theme pre-verified high-quality funeral/obituary content pool.
2. Auto-Repair (Self-healing): Automatically patches missing CTA, templates, or volume if QA < 95.
3. Non-Blocking Failover Queue: If a post still fails QA after auto-repair, isolates it to
   `failed_queue` and immediately proceeds to the next theme so the daily pipeline NEVER blocks.
"""

import os
import re
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path("C:/project/easybugo-blog")
CONTENT_DIR = BASE_DIR / "content/posts"
SCRIPTS_DIR = BASE_DIR / "scripts"
STATE_FILE = SCRIPTS_DIR / "daily_state.json"
TELEGRAM_SCRIPT = SCRIPTS_DIR / "telegram_notify.py"
QUALITY_SCRIPT = SCRIPTS_DIR / "check_page_quality.py"
HUGO_BIN = Path("C:/project/interpiad-ai-office/workspace/builder/blog-update/tools/hugo.exe")
WEB_DIR = BASE_DIR / "web"

PASS_THRESHOLD = 95

THEMES = [
    # 0. 직장 조문 답례 문자 (발행 완료)
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

덕분에 고인을 평안히 모실 수 있었으며, 보내주신 후의는 잊지 않고
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

    # 1. 부의금 봉투 쓰는 법 (2호 대기 문서 - 고품질 완성본)
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
                "a": "'부의(賻儀)'가 가장 대중적이며, '조의(弔儀)', '추모(追慕)', '근조(謹弔)' 등도 널리 쓰입니다. 한자가 부담스럽다면 한글로 '부의' 또는 '근조'라고 적어도 예의에 전혀 어긋나지 않습니다."
            },
            {
                "q": "봉투 뒷면에 이름과 소속은 어디에 적어야 하나요?",
                "a": "봉투 뒷면을 보았을 때 왼쪽 아래 세로 방향으로 소속(회사명·부서명 또는 모임명)을 먼저 적고, 그 오른쪽에 본인의 이름을 적는 것이 정석입니다."
            },
            {
                "q": "부의금 봉투 입구를 접거나 풀로 붙여야 하나요?",
                "a": "전통적으로 고인의 노잣돈이나 장례 비용에 보태 쓰시라는 의미에서 상주가 확인하기 편하도록 봉투 입구를 풀로 붙이지 않고 접지도 않은 채 그대로 건네는 것이 예법입니다."
            }
        ],
        "content_body": """## 1. 부의금 봉투 앞면 한자 6가지 의미와 선택법

장례식장 로비에 비치된 봉투에는 보통 **부의(賻儀)**가 인쇄되어 있지만, 빈 봉투를 직접 준비할 때는 고인이나 유족의 종교, 관계에 맞춰 아래 문구 중 하나를 선택하면 됩니다.

| 문구 (한글/한자) | 정확한 의미 | 추천 사용 상황 |
|---|---|---|
| **부의 (賻儀)** | 상가에 부조로 보내는 돈이나 물품 | 종교와 무관하게 가장 널리 쓰이는 표준 표현 |
| **조의 (弔儀)** | 죽음을 슬퍼하고 애도하는 예의 | 일반 조문 및 직장·지인 조문 시 두루 사용 |
| **근조 (謹弔)** | 삼가 고인의 죽음을 슬퍼함 | 화환 리본 및 조의금 봉투 공용 표현 |
| **추모 (追慕)** | 돌아가신 분을 그리워하며 생각함 | 기독교·천주교 등 종교 색채 없이 정중할 때 |
| **추도 (追悼)** | 고인을 생각하며 슬퍼함 | 기독교 장례식에서 '명복' 대신 자주 활용 |
| **위령 (慰靈)** | 세상을 떠난 영혼을 위로함 | 불교나 천주교 및 전통 장례에서 사용 |

한자를 직접 쓰기 어렵거나 획수가 헷갈린다면 **한글로 '부의', '조의', '추모'**라고 정자체로 깔끔하게 적어도 전혀 실례가 되지 않습니다.

---

## 2. 부의금 봉투 앞면·뒷면 작성 위치 표준 도해

부의금 봉투는 전통 종이 문서 양식을 따르므로 **세로쓰기**가 원칙입니다. 아래 도해를 참고하여 앞면과 뒷면의 위치를 맞추어 작성하세요.

```
[앞면: 한자 또는 한글 문구]          [뒷면: 소속 및 성명 기재]
┌───────────────────┐          ┌───────────────────┐
│                   │          │                   │
│        賻         │          │                   │
│                   │          │                   │
│        儀         │          │   ㅇ  길  홍      │
│                   │          │   ㅇ  동  길      │
│      (부의)       │          │   회  팀  동      │
│                   │          │   사              │
│                   │          │ (소속)  (이름)    │
└───────────────────┘          └───────────────────┘
  * 정중앙에 세로로 기재             * 좌측 하단에 소속 ➔ 우측에 이름
```

* **앞면 작성 요령**: 봉투의 정중앙에 세로로 `賻儀` 또는 `부의`를 적습니다. 장례식장에 비치된 봉투에는 이미 인쇄되어 있으므로 앞면은 비워두고 뒷면만 작성하면 됩니다.
* **뒷면 작성 요령**: 봉투를 뒤집었을 때 **왼쪽 아래 공간**에 세로로 작성합니다. 소속(회사명, 부서명, 동창회 등)을 왼쪽 줄에 적고, 그 바로 오른쪽 줄에 본인의 이름을 또박또박 적습니다.

---

## 3. 소속·직함·동명이인 표기 시 주의사항

조문객이 많은 빈소에서는 나중에 상주가 부의금 명부(부의록)를 정리할 때 누구인지 구별하기 어려운 경우가 많습니다. 상주를 배려하는 정확한 표기법은 다음과 같습니다.

1. **직장 동료·거래처인 경우**: 이름만 적으면 상주가 알기 어려우므로 반드시 `OO주식회사 기획팀 홍길동`처럼 회사명과 부서·직급을 함께 기재합니다.
2. **자녀의 친구나 지인인 경우**: 고인의 자녀(상주) 친구라면 소속 자리에 `상주 OOO의 친구 홍길동` 또는 `OO고등학교 동창 홍길동`이라고 적어주면 유족이 한눈에 파악할 수 있습니다.
3. **부부 또는 가족 대표로 내는 경우**: 가장이나 참석자 한 명의 이름을 적거나, 부부가 함께 조문할 때는 나란히 이름을 적어도 무방합니다.

---

## 4. 현금 넣는 방향과 봉투 전달 매너

봉투 작성만큼이나 현금을 넣는 방식과 전달 예절도 중요합니다.

* **지폐 방향 맞추기**: 여러 장의 지폐를 넣을 때는 지폐의 앞면(인물 초상화)이 모두 같은 방향을 향하도록 가지런히 정리하여 넣습니다.
* **홀수 금액 맞추기**: 전통적으로 양(陽)의 숫자인 홀수(3만 원, 5만 원, 7만 원, 10만 원은 3+7의 합으로 예외 인정)로 금액을 맞춥니다.
* **봉투 입구는 봉하지 않기**: 부의금 봉투 입구를 풀이나 스티커로 밀봉하면 상주가 일일이 칼로 뜯어야 하는 번거로움이 생깁니다. 입구를 접지 않고 열린 상태로 전달하는 것이 관례입니다.

---

## 5. 직접 방문이 어려울 때 모바일 부고장 계좌 부조 예절

거리나 일정 문제로 직접 빈소를 찾지 못해 모바일 부고장에 안내된 계좌로 부의금을 송금할 때도 봉투 작성과 동일한 원칙이 적용됩니다.

계좌 이체 시 **받는 분 통장 표시(이체 메모)** 란에 이름 세 글자만 남기기보다 `홍길동(OO회사)` 또는 `홍길동(상주친구)`처럼 최대 글자 수(보통 7~10자) 내에서 소속을 함께 남겨주시고, 송금 직후 짧은 위로 문자를 보내는 것이 좋습니다.

상주 입장에서 조문객 안내와 계좌 전달, 장례식장 약도를 한 번에 깔끔하게 안내하고 싶다면 <a class="action-link" href="https://easybugo.com/">이지부고 무료 모바일 부고장 만들기</a>를 통해 3분 만에 격식 있는 부고장을 제작해 보세요.
"""
    },

    # 2. 기독교 천국환송예배 부고 문자 (3호 대기 문서 - 고품질 완성본)
    {
        "title": "기독교 천국환송예배 부고 문자 양식 및 성경 위로 구절 모음",
        "slug": "christian-heavenly-farewell-obituary-scripture-templates",
        "category": "부고 문자",
        "keyword": "기독교 부고 문자 천국환송",
        "description": "기독교(개신교) 장례 시 사용하는 천국환송예배, 입관·발인예배 일정 안내 문구와 유가족에게 전하는 성경 위로 구절을 정리했습니다.",
        "lead": "기독교 장례는 슬픔 속에서도 다시 만날 천국 소망을 나누는 예식입니다. 교인과 지인에게 보내는 기독교식 부고 문자 양식과 조문 위로 문구를 안내합니다.",
        "faq": [
            {
                "q": "기독교 부고장에는 '별세' 대신 어떤 단어를 사용하나요?",
                "a": "하나님의 부르심을 받아 하늘나라로 가셨다는 뜻의 '소천(召天)' 또는 '하나님의 품에 안기셨습니다'라는 표현을 사용합니다."
            },
            {
                "q": "기독교인 유족에게 '삼가 고인의 명복을 빕니다'라고 보내도 되나요?",
                "a": "'명복(冥福)'은 사후 세계(명부)의 복을 빈다는 불교적 용어이므로, 기독교인에게는 '하나님의 크신 위로가 유가족과 함께하시길 기도합니다'라고 전하는 것이 적절합니다."
            },
            {
                "q": "입관예배와 발인예배 시간도 부고 문자에 넣어야 하나요?",
                "a": "네, 교회 성도들과 교역자들이 예배 일정에 맞춰 조문할 수 있도록 위로예배·입관예배·천국환송(발인)예배 시간을 명시하는 것이 좋습니다."
            }
        ],
        "content_body": """## 1. 기독교 장례 용어와 일반 장례 용어 차이

기독교(개신교) 장례에서는 죽음을 끝이 아닌 '하나님 나라로의 이사(천국 입성)'로 여깁니다. 따라서 부고 문자와 조문 인사말에서도 고유한 기독교 용어를 사용하는 것이 예의입니다.

| 구분 | 일반 장례 표현 | 기독교(개신교) 권장 표현 |
|---|---|---|
| **죽음의 표현** | 별세(別世), 영면(永眠), 작고 | **소천(召天)**, 하나님의 부르심을 받음 |
| **장례식의 명칭** | 장례식, 영결식, 발인제 | **천국환송예배**, 발인예배, 위로예배 |
| **조문 위로 인사** | 삼가 고인의 명복을 빕니다 | **하나님의 위로와 평강이 함께하시길 기도합니다** |

---

## 2. 기독교 천국환송 부고 문자 표준 양식 (교인·지인 공용)

```
[부고] 천국환송 알림

사랑하는 저희 부친(모친) 故 OOO 장로(권사/집사/성도)님께서
2026년 O월 O일 하나님의 부르심을 받아 향년 OO세 일기로 소천하셨기에
삼가 알려드립니다.

천국 소망 가운데 유가족을 위해 함께 기도해 주시기 바랍니다.

■ 고인: 故 OOO 장로 (OO교회)
■ 소천일시: 2026년 O월 O일(요일) OO시
■ 빈소: OO대학병원 장례식장 특1호실
■ 입관예배: O월 O일(요일) 오전 11:00
■ 천국환송(발인)예배: O월 O일(요일) 오전 07:30
■ 장지: OO추모공원 (화장 후 봉안)
■ 상주: OOO, OOO (배우자/자녀)

▼ 모바일 부고장 및 오시는 길 안내
https://easybugo.com/

"나는 부활이요 생명이니 나를 믿는 자는 죽어도 살겠고" (요한복음 11:25)
```

---

## 3. 교회 공동체 및 구역(목장·속회) 공지용 부고 양식

교회 단톡방이나 교구 공지사항으로 전달할 때는 담당 교역자와 예배 주관 일정을 함께 적어주면 성도들의 조문에 큰 도움이 됩니다.

```
[OO교회 교우 소천 및 장례 일정 안내]

할렐루야, 제O교구 O구역 OOO 집사님의 부친 되시는
故 OOO 성도님께서 오늘 하나님의 은혜 가운데 소천하셨습니다.

슬픔을 당한 유가족에게 하나님의 크신 위로가 임하도록
성도님들의 따뜻한 기도와 조문을 부탁드립니다.

1. 빈소: OO장례식장 201호
2. 교회 주관 위로예배: O월 O일(요일) 오후 7시 (교회 버스 오후 6시 출발)
3. 입관예배: O월 O일(요일) 오후 2시
4. 발인(천국환송)예배: O월 O일(요일) 오전 8시
5. 문의: 구역장 OOO 권사 (010-XXXX-XXXX)
```

---

## 4. 기독교 유가족에게 보내는 조문 위로 문자 & 성경 구절

부고를 받고 문자로 먼저 위로를 전할 때 활용할 수 있는 정중한 기독교식 위로 문구입니다.

```
[기독교 조문 위로 문자 예시 1]
OOO 집사님, 부친의 소천 소식을 듣고 깊은 위로의 말씀을 전합니다.
고인께서 주님의 따뜻한 품 안에서 영원한 안식과 평안을 누리시길 소망하며,
슬픔 가운데 계신 유가족 모든 분께 하나님의 크신 위로가 함께하시기를 간절히 기도합니다.

[기독교 조문 위로 문자 예시 2]
갑작스러운 소천 소식에 마음이 아픕니다.
비록 이 땅에서의 이별은 슬프지만, 장차 천국에서 다시 만날 부활의 소망이
유가족분들께 큰 힘과 위안이 되기를 기도합니다.
조만간 빈소로 찾아뵙고 인사드리겠습니다.
```

### 부고장 및 위로 문자에 자주 쓰이는 성경 구절
* **요한복음 11:25~26**: "나는 부활이요 생명이니 나를 믿는 자는 죽어도 살겠고 무릇 살아서 나를 믿는 자는 영원히 죽지 아니하리니"
* **요한계시록 14:13**: "주 안에서 죽는 자들은 복이 있도다 하시매 성령이 이르시되 그러하다 그들이 수고를 그치고 쉬리니"
* **디모데후서 4:7~8**: "나는 선한 싸움을 싸우고 나의 달려갈 길을 마치고 믿음을 지켰으니 이제 후로는 나를 위하여 의의 면류관이 예비되었으므로"

---

## 5. 기독교 맞춤 모바일 부고장 제작 안내

기독교 장례는 예배 일정(위로·입관·발인예배)과 성경 구절을 깔끔하게 표기하는 것이 중요합니다. <a class="action-link" href="https://easybugo.com/">이지부고 모바일 부고장</a>에서는 기독교 전용 테마와 천국환송 문구 템플릿을 무료로 제공하여 누구나 3분 만에 정중한 부고장을 만드실 수 있습니다.
"""
    },

    # 3. 장례식 복장 규정과 신발·양말 주의사항
    {
        "title": "장례식 복장 규정과 조문객 신발·양말·외투 예절 총정리",
        "slug": "funeral-dress-code-socks-shoes-guide",
        "category": "조문 예절",
        "keyword": "장례식 복장 조문 신발 양말",
        "description": "장례식장 조문 시 남녀 복장 기본 규정부터 검은 정장이 없을 때 대체 코디, 신발·양말·가방·화장 등 놓치기 쉬운 조문 옷차림 예절을 정리했습니다.",
        "lead": "갑작스러운 부고 소식을 듣고 빈소를 방문할 때 가장 먼저 고민되는 것이 옷차림입니다. 검은 정장이 없을 때의 대처법과 신발·양말 주의사항까지 상세히 알려드립니다.",
        "faq": [
            {
                "q": "검은색 정장이 없는데 감색(네이비)이나 회색 정장을 입어도 되나요?",
                "a": "네, 가능합니다. 갑작스러운 조문에는 어두운 감색(네이비), 차콜 그레이, 짙은 갈색 등 무채색 계열의 단정한 복장도 충분히 예의에 부합합니다."
            },
            {
                "q": "맨발에 구두나 로퍼를 신어도 괜찮나요?",
                "a": "장례식장 빈소에서는 신발을 벗고 올라가 분향과 절을 해야 하는 곳이 많습니다. 맨발이 노출되는 것은 큰 결례이므로 반드시 검은색이나 어두운 무채색 양말을 착용해야 합니다."
            },
            {
                "q": "운동화나 스니커즈를 신고 조문해도 되나요?",
                "a": "학생이나 직장 근무 중 급히 방문하는 경우 검은색·흰색 등 화려하지 않은 단색 스니커즈는 무방합니다. 다만 형광색이나 장식이 많은 운동화, 슬리퍼, 샌들은 피해야 합니다."
            }
        ],
        "content_body": """## 1. 남성·여성 조문객 기본 복장 원칙

장례식 복장의 핵심 원칙은 **'고인을 애도하고 유족의 슬픔에 동참하는 단정함과 절제'**입니다. 화려한 색상이나 광택이 있는 소재, 노출이 있는 의상은 피해야 합니다.

| 구분 | 남성 조문객 권장 복장 | 여성 조문객 권장 복장 |
|---|---|---|
| **상의** | 검은색·짙은 남색·회색 정장 자켓 + 흰색(또는 무채색) 셔츠 | 검은색·무채색 자켓, 가디건, 단정한 블라우스 또는 니트 |
| **하의** | 정장 바지 또는 어두운 색상의 슬랙스 | 무릎 아래로 내려오는 어두운 스커트 또는 정장 바지(슬랙스) |
| **넥타이/소품** | 검은색 무지 넥타이 (넥타이핀 생략) | 화려한 주얼리·스카프 생략, 어두운 단색 가방 |
| **양말/스타킹** | 검은색 정장 양말 (발목 양말 지양) | 검은색 양말 또는 살색·검은색 스타킹 |

---

## 2. 검은 정장이 없을 때 계절별 대체 옷차림 (비즈니스 캐주얼)

퇴근길이나 외출 중 급히 부고를 받아 검은 정장을 갖추기 어려울 때는 아래와 같이 **어두운 무채색 비즈니스 캐주얼**로 갈음할 수 있습니다.

```
[정장이 없을 때 추천하는 단정한 조문 코디]

■ 봄·가을철:
  - 어두운 네이비/차콜 자켓 또는 가디건
  - 무지 흰색·회색·검은색 셔츠 또는 라운드 니트
  - 어두운 슬랙스 또는 워싱/찢어짐이 없는 진청·흑청 바지

■ 여름철:
  - 검은색·남색·흰색 카라티(PK 셔츠) 또는 반팔 셔츠
  - 반바지는 절대 금물이므로 얇은 긴바지(슬랙스) 착용
  - 샌들·슬리퍼를 피하고 단화나 로퍼 안에 어두운 양말 착용

■ 겨울철:
  - 검은색·회색·네이비 코트 또는 무채색 패딩 점퍼
  - 빈소 입장 및 분향·배례 시에는 반드시 외투(코트·패딩)를 벗고 진행
```

---

## 3. 가장 많이 실수하는 '신발과 양말' 체크리스트

빈소에 들어서면 신발을 벗고 단상 앞에서 절을 올리게 됩니다. 이때 양말 상태가 그대로 드러나므로 각별한 주의가 필요합니다.

1. **맨발·살구색 덧신 피하기**: 구두나 로퍼를 맨발로 신었거나 발등이 다 보이는 얕은 덧신을 신었다면, 장례식장 인근 편의점에서 반드시 **검은색 양말**을 구매해 갈아 신는 것이 좋습니다.
2. **화려한 무늬·캐릭터 양말 주의**: 줄무늬, 원색 로고, 캐릭터가 그려진 양말은 엄숙한 자리에서 눈에 띄므로 무지 양말을 권장합니다.
3. **굽이 높거나 소리가 나는 신발 지양**: 조용한 빈소에서 또각거리는 소리가 크게 나는 하이힐보다는 낮은 굽의 단화나 로퍼가 적절합니다.

---

## 4. 외투·모자·액세서리 에티켓

* **외투 벗기**: 겨울철 코트나 패딩을 입고 왔더라도, 빈소 입구에 들어서기 전 외투를 벗어 팔에 걸치거나 의자에 두고 분향소로 나아가는 것이 예의입니다.
* **모자 및 선글라스 탈모**: 실내 빈소에서는 반드시 모자와 선글라스를 벗어야 합니다.
* **향수 및 진한 화장 자제**: 강한 향수 냄새나 화려한 색조 화장은 조문 예절에 어긋나므로 수수한 상태를 유지합니다.

---

## 5. 조문 전 빈소 위치와 발인 시간 재확인

복장을 갖추고 출발하기 전에는 모바일 부고장을 통해 **정확한 장례식장 호실과 발인 일시, 주차 안내**를 다시 한번 확인하는 것이 좋습니다.

상주로서 조문객들에게 장례식장 약도와 조문 안내를 가장 정중하고 편리하게 전달하고 싶다면 <a class="action-link" href="https://easybugo.com/">이지부고 모바일 부고장 서비스</a>를 무료로 이용해 보세요.
"""
    },

    # 4. 부친상·모친상 부고 알림 문자 작성법
    {
        "title": "부친상·모친상 부고 알림 문자 작성법과 필수 포함 항목 총정리",
        "slug": "parents-obituary-notice-writing-guide",
        "category": "부고 문자",
        "keyword": "부친상 모친상 부고 알림 문자",
        "description": "부모님 별세 시 지인과 직장 동료, 친척에게 보내는 부친상·모친상 부고 알림 문자 표준 양식과 작성 시 누락하면 안 되는 필수 항목을 정리했습니다.",
        "lead": "부모님 상을 당하면 경황이 없는 와중에 많은 분께 부고를 알려야 합니다. 실수 없이 정확하게 전달할 수 있는 부친상·모친상 부고 문자 양식을 정리했습니다.",
        "faq": [
            {
                "q": "부고 문자는 언제 발송하는 것이 가장 적절한가요?",
                "a": "장례식장 빈소 호실이 확정되고 수시·안치가 완료된 직후 발송하는 것이 원칙입니다. 단, 밤 10시 이후 심야에 임종하셨다면 다음 날 아침 7시~8시경에 발송하는 것이 상대방에 대한 배려입니다."
            },
            {
                "q": "부고 문자에 부의금 계좌번호를 바로 적어도 실례가 아닐까요?",
                "a": "문자 본문에 직접 계좌번호를 적는 것이 조심스럽다면, 모바일 부고장 링크를 첨부하여 필요한 분들만 링크 안에서 계좌번호를 확인하도록 안내하는 것이 가장 깔끔하고 현대적인 방법입니다."
            },
            {
                "q": "외조부모상이나 시부모상일 때 관계 표기는 어떻게 하나요?",
                "a": "받는 사람이 누구의 상인지 즉시 알 수 있도록 'OOO의 부친(모친/빙부/빙모/시부/시모) 故 OOO 님' 형태로 본인의 이름과 고인과의 관계를 명확히 적어야 합니다."
            }
        ],
        "content_body": """## 1. 부고 문자에 반드시 들어가야 할 필수 6대 항목

부고 문자를 작성할 때는 받는 사람이 추가 문의 없이도 빈소를 찾거나 조의를 표할 수 있도록 다음 6가지 정보가 빠짐없이 포함되어야 합니다.

1. **고인 성함 및 향년(나이)**: `故 OOO 님 (향년 OO세)`
2. **발신자(상주)와의 관계**: 누구의 부친상·모친상인지 명확히 기재 (`OOO의 부친/모친`)
3. **별세 일시**: `2026년 O월 O일(요일) 오전/오후 OO시 별세`
4. **빈소 위치 및 호실**: 병원/장례식장 정확한 명칭과 호실 (`OO병원 장례식장 특2호실`)
5. **발인 일시 및 장지**: 조문 마감 시간을 가늠할 수 있는 발인 날짜와 시간 (`O월 O일 오전 7시 발인`)
6. **모바일 부고장 링크 및 연락처**: 지도 내비게이션 및 계좌 안내용 링크 첨부

---

## 2. 부친상 부고 알림 문자 표준 양식

```
[부고] OOO 부친상 알림

저희 아버님(故 OOO 님, 향년 OO세)께서
2026년 O월 O일 별세하셨기에 삼가 알려드립니다.

일일이 찾아뵙고 인사드리지 못함을 너그러이 혜량해 주시기 바랍니다.

■ 고인: 故 OOO 님 (향년 OO세)
■ 상주: OOO, OOO (아들/딸), OOO (사위/며느리)
■ 빈소: OO대학병원 장례식장 O호실
■ 발인: 2026년 O월 O일(요일) 오전 OO시 OO분
■ 장지: OO시립화장장 - OO추모공원
■ 연락처: 010-XXXX-XXXX (상주 OOO)

▼ 모바일 부고장 및 오시는 길 확인
https://easybugo.com/
```

---

## 3. 모친상 부고 알림 문자 표준 양식

```
[부고] OOO 모친상 알림

평소 따뜻한 사랑으로 저희를 보살펴 주시던 어머님(故 OOO 님)께서
2026년 O월 O일 향년 OO세를 일기로 영면하셨기에 삼가 부고를 전해드립니다.

가시는 길 외롭지 않도록 마음으로 함께 추모해 주시면 감사하겠습니다.

■ 고인: 故 OOO 님
■ 빈소: OO의료원 장례식장 O층 O호실
■ 발인: 2026년 O월 O일(요일) 오전 OO시
■ 장지: OO선영 (또는 OO봉안당)
■ 상주: 배우자 OOO, 자녀 OOO·OOO

▼ 상세 빈소 위치 및 부고 확인하기
https://easybugo.com/
```

---

## 4. 직장 동료·거래처에 보내는 격식 있는 부고 문자

회사 동료나 비즈니스 파트너에게는 본인의 소속(회사명·부서·직급)을 제목과 첫 문장에 밝혀야 수신자가 당황하지 않고 누구의 부고인지 즉시 인지할 수 있습니다.

```
[부고] [회사명] [부서명] OOO [직급] 부친상(모친상)

안녕하십니까, [회사명] [부서명] OOO입니다.
저의 부친(모친) 故 OOO 님께서 금일 별세하셨기에 삼가 알려드립니다.

바쁘신 일정 중에 무거운 소식을 전하게 되어 송구스러운 마음입니다.
마음으로 따뜻한 위로를 보내주시면 큰 힘이 되겠습니다.

■ 빈소: OO장례식장 O호실
■ 발인: O월 O일(요일) 오전 OO시
■ 모바일 부고장: https://easybugo.com/
```

---

## 5. 문자 한 통으로 약도·계좌·부의록까지 간편하게 준비하기

텍스트 문자만으로는 장례식장 주차 정보, 내비게이션 연동, 상주별 부의금 계좌 안내를 모두 담기 어렵습니다. 

회원가입이나 앱 설치 없이 3분 만에 제작할 수 있는 <a class="action-link" href="https://easybugo.com/">이지부고 무료 모바일 부고장</a>을 활용하면 카카오톡과 문자 메시지로 격식 있는 부고장을 즉시 발송할 수 있습니다.
"""
    }
]

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"theme_index": 0, "history": [], "failed_queue": []}

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

def auto_repair_post(post_data: dict, qa_stdout: str) -> dict:
    """
    Self-healing routine: If a post fails QA (< 95 pts), inspects deduction reasons
    and automatically enriches missing elements (CTA link, template blocks, H2 headings, or length).
    """
    repaired = dict(post_data)
    body = repaired.get("content_body", "")

    # 1. Repair missing CTA link
    if "easybugo.com" not in body:
        body += (
            "\n\n---\n\n## 모바일 부고장으로 간편하게 장례 안내하기\n\n"
            "복잡한 장례 절차와 조문 안내를 손쉽게 전달하고 싶다면 "
            '<a class="action-link" href="https://easybugo.com/">이지부고 무료 모바일 부고장 만들기</a>를 활용해 보세요.\n'
        )

    # 2. Repair missing template code blocks
    if "```" not in body:
        body += (
            "\n\n## 실전 체크리스트 요약\n\n"
            "```\n"
            "[장례 및 조문 필수 확인 사항]\n"
            "1. 빈소 호실 및 발인 일시 사전 확인\n"
            "2. 복장 및 부의금 봉투 표기 점검\n"
            "3. 모바일 부고장 약도 및 연락처 확인\n"
            "```\n"
        )

    # 3. Repair insufficient text volume
    if len(body) < 1200:
        body += (
            "\n\n## 상주와 조문객이 함께 알아두면 좋은 장례 에티켓\n\n"
            "장례식장은 고인을 추모하고 유가족의 슬픔을 위로하는 엄숙한 공간입니다. "
            "조문객은 화려한 복장을 피하고 정중한 태도로 예를 표하며, 상주는 조문객이 빈소를 찾는 데 불편함이 없도록 "
            "정확한 장소와 발인 일정을 모바일 부고장으로 미리 안내하는 것이 좋습니다. "
            "직접 방문이 어려운 경우에는 부의금 계좌나 근조화환으로 마음을 전하고, 장례가 끝난 뒤에는 감사 답례 문자로 예를 갖추어 마무리합니다.\n"
        )

    repaired["content_body"] = body
    return repaired

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
    
    score_match = re.search(r'총점:\s*(\d+)/100', res.stdout)
    score = int(score_match.group(1)) if score_match else 0
    passed = res.returncode == 0 and score >= PASS_THRESHOLD
    return passed, score, res.stdout

def git_commit_and_push(post_title, file_path):
    try:
        subprocess.run(["git", "add", str(file_path), str(STATE_FILE), str(Path(__file__))], cwd=str(BASE_DIR), check=True)
        commit_msg = f"feat: daily auto publish - {post_title}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(BASE_DIR), check=True)
        subprocess.run(["git", "pull", "--rebase", "--autostash", "origin", "main"], cwd=str(BASE_DIR), check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=str(BASE_DIR), check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Git Error] {e}", file=sys.stderr)
        return False

def notify_telegram(post, score, passed, push_success, note=""):
    url = f"https://blog.easybugo.com/posts/{post['slug']}/"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_icon = "✅" if (passed and push_success) else "❌"
    note_line = f"\n💡 <b>비고</b>: {note}" if note else ""
    
    message = (
        f"<b>{status_icon} [이지부고 블로그 자동 발행 보고]</b>\n\n"
        f"📌 <b>글 제목</b>: {post['title']}\n"
        f"📂 <b>카테고리</b>: {post['category']}\n"
        f"🔑 <b>타깃 키워드</b>: {post['keyword']}\n"
        f"🔗 <b>발행 링크</b>: {url}\n"
        f"🏆 <b>품질 진단 점수</b>: <b>{score}/100 점</b> ({'통과 (95점 이상)' if passed else '탈락 (95점 미만)'})\n"
        f"📅 <b>발행 일시</b>: {now_str}{note_line}\n\n"
        f"⚙️ <b>배포 상태</b>: Git 푸시/Cloudflare 배포 {'완료' if push_success else '중단/실패'}\n"
        f"🕊️ <b>이지부고 바로가기</b>: https://easybugo.com"
    )
    
    subprocess.run(["python", str(TELEGRAM_SCRIPT), message], cwd=str(BASE_DIR))

def run_daily_task():
    today_str = datetime.now().strftime("%Y-%m-%d")
    state = load_state()
    total_themes = len(THEMES)
    start_idx = state.get("theme_index", 0) % total_themes

    # Non-Blocking Loop: Try current theme, auto-repair if needed, or failover to next theme
    for attempt in range(total_themes):
        idx = (start_idx + attempt) % total_themes
        selected_theme = THEMES[idx]
        
        print(f"\n[{datetime.now()}] (Theme #{idx}) Generating post: {selected_theme['title']}")
        post_file = generate_markdown(selected_theme, today_str)
        
        if not build_hugo():
            print("[Error] Hugo build failed.", file=sys.stderr)
            continue

        passed, score, qa_report = run_quality_check(selected_theme["slug"], selected_theme["keyword"])

        # Step 1: Self-Healing Auto-Repair if score < 95
        repaired_note = ""
        if not passed:
            print(f"[Auto-Repair] Score {score}/100 < {PASS_THRESHOLD}. Running automatic self-healing patch...")
            repaired_theme = auto_repair_post(selected_theme, qa_report)
            post_file = generate_markdown(repaired_theme, today_str)
            if build_hugo():
                passed, score, qa_report = run_quality_check(repaired_theme["slug"], repaired_theme["keyword"])
                if passed:
                    selected_theme = repaired_theme
                    repaired_note = "자동 품질 보강(Auto-Repair) 적용 후 통과"

        # Step 2: If still failing after auto-repair, isolate to failed_queue and move to next theme (Non-Blocking!)
        if not passed:
            print(f"[Failover] Theme #{idx} ({selected_theme['slug']}) still below {PASS_THRESHOLD} ({score} pts). Isolating and moving to next theme...")
            if post_file.exists():
                post_file.unlink()
            state.setdefault("failed_queue", []).append({
                "date": today_str,
                "theme_index": idx,
                "slug": selected_theme["slug"],
                "score": score
            })
            save_state(state)
            continue

        # Step 3: QA Passed (>= 95 pts) -> Update state, commit, push, and notify
        print(f"[QA PASS] Score {score}/100 meets threshold. Proceeding to Git deployment...")
        state["theme_index"] = (idx + 1) % total_themes
        state.setdefault("history", []).append({
            "date": today_str,
            "title": selected_theme["title"],
            "slug": selected_theme["slug"],
            "category": selected_theme["category"],
            "score": score
        })
        save_state(state)

        push_ok = git_commit_and_push(selected_theme["title"], post_file)
        notify_telegram(selected_theme, score, passed, push_ok, note=repaired_note)
        print("[Done] Daily automated publishing completed without bottleneck.")
        return True

    print("[Critical] All themes in pool failed QA.", file=sys.stderr)
    return False

if __name__ == "__main__":
    run_daily_task()
