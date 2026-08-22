---
title: "3일장 일정 계산 — 발인일 자동 계산기"
description: "별세일만 입력하면 3일장(또는 2일장·5일장) 기준 발인일을 바로 계산해 드립니다."
date: 2026-08-22
categories: ["장례식장·비용"]
lead: "3일장 기준 발인일이 언제인지 헷갈릴 때, 별세일만 입력하면 바로 계산해 드립니다."
slug: "funeral-schedule-calculator"
faq:
  - q: "3일장 발인일은 어떻게 계산하나요?"
    a: "별세일을 1일째로 세어 3일째 되는 날 오전에 발인하는 것이 일반적입니다. 즉 별세일 다음다음 날입니다."
  - q: "2일장이나 5일장으로 하면 날짜가 어떻게 달라지나요?"
    a: "2일장은 별세일 다음 날, 5일장은 별세일로부터 5일째 되는 날이 발인일이 됩니다."
---

## 계산기: 별세일과 일정을 선택하세요

<div class="section" style="gap:12px">
  <div class="field">
    <label for="fs-date">별세일</label>
    <input type="date" id="fs-date">
  </div>
  <div class="choice-row" id="fs-days">
    <button type="button" class="choice selected" data-days="3">3일장</button>
    <button type="button" class="choice" data-days="2">2일장</button>
    <button type="button" class="choice" data-days="5">5일장</button>
  </div>
  <div id="fs-result" class="muted">날짜를 선택하면 발인일이 표시됩니다.</div>
</div>

<script>
(function(){
  const dateInput = document.getElementById('fs-date');
  const daysRow = document.getElementById('fs-days');
  const result = document.getElementById('fs-result');
  const WD = ['일','월','화','수','목','금','토'];
  let days = 3;
  function calc(){
    if (!dateInput.value) return;
    const [y,m,d] = dateInput.value.split('-').map(Number);
    const base = new Date(Date.UTC(y, m-1, d));
    base.setUTCDate(base.getUTCDate() + (days - 1));
    const wd = WD[base.getUTCDay()];
    result.innerHTML = '<strong>발인일: ' + base.getUTCFullYear() + '년 ' + (base.getUTCMonth()+1) + '월 ' + base.getUTCDate() + '일 (' + wd + '요일) 오전</strong>';
  }
  dateInput.addEventListener('change', calc);
  daysRow.addEventListener('click', function(e){
    const btn = e.target.closest('.choice');
    if (!btn) return;
    days = Number(btn.dataset.days);
    [...daysRow.children].forEach(b => b.classList.toggle('selected', b === btn));
    calc();
  });
})();
</script>

## 계산 원리

별세일을 1일째로 셉니다. 3일장이면 3일째 되는 날, 즉 별세일 다음다음 날 오전에 발인합니다.

- **2일장**: 별세일 다음 날 발인
- **3일장**: 별세일 다음다음 날 발인 (가장 일반적)
- **5일장**: 별세일로부터 5일째 되는 날 발인

정확한 발인 시각은 장례식장·화장장 예약 상황에 따라 조정될 수 있습니다.

전체 절차가 궁금하다면 <a class="action-link" href="https://easybugo.com/guide/procedure.html">3일장 장례 절차 가이드</a>를 확인하세요. 발인일이 정해지면 <a class="action-link" href="https://easybugo.com/new.html">부고장 만들기</a>에서 자동으로 같은 방식으로 계산해 드립니다.
