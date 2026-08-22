---
title: "49재 계산 — 날짜 자동 계산기"
description: "49재가 언제인지 헷갈릴 때, 발인일이나 별세일만 입력하면 바로 계산해 드립니다."
date: 2026-08-22
categories: ["49재·제사"]
lead: "49재는 돌아가신 날을 1일로 세어 49일째 되는 날입니다. 직접 세기 번거로우니 날짜만 입력하면 계산해 드립니다."
slug: "49jae-calculator"
faq:
  - q: "49재는 어떻게 계산하나요?"
    a: "돌아가신 날을 1일째로 세어 49일째 되는 날입니다. 7일마다 재를 지내는 불교 의식에서 유래했으며, 7번째 7일(7×7=49일)이 마지막 재입니다."
  - q: "49재를 꼭 지내야 하나요?"
    a: "필수는 아닙니다. 불교식 전통에서 비롯된 의식이라 종교나 가족 사정에 따라 생략하거나 간소하게 치르기도 합니다."
  - q: "기제사와 49재는 다른 건가요?"
    a: "네, 다릅니다. 49재는 돌아가신 후 49일째 한 번 지내는 의식이고, 기제사는 매년 돌아가신 날(기일)에 지내는 제사입니다."
---

## 계산기: 날짜만 입력하세요

<div class="section" style="gap:12px">
  <div class="field">
    <label for="jae-date">별세일(또는 발인 기준일)</label>
    <input type="date" id="jae-date">
  </div>
  <div id="jae-result" class="muted">날짜를 선택하면 49재 날짜가 표시됩니다.</div>
</div>

<script>
(function(){
  const input = document.getElementById('jae-date');
  const result = document.getElementById('jae-result');
  const WD = ['일','월','화','수','목','금','토'];
  input.addEventListener('change', function(){
    if (!input.value) return;
    const [y,m,d] = input.value.split('-').map(Number);
    const base = new Date(Date.UTC(y, m-1, d));
    base.setUTCDate(base.getUTCDate() + 48);
    const wd = WD[base.getUTCDay()];
    result.innerHTML = '<strong>49재: ' + base.getUTCFullYear() + '년 ' + (base.getUTCMonth()+1) + '월 ' + base.getUTCDate() + '일 (' + wd + '요일)</strong>';
  });
})();
</script>

## 49재란

불교식 전통에서 사람이 죽은 뒤 49일 동안 7일마다 한 번씩 재(齋)를 올려 고인의 극락왕생을 기원하는 의식입니다. 돌아가신 날을 1일째로 세어 49일째 되는 날이 마지막 재, 즉 49재입니다.

## 계산 방법 (직접 셀 경우)

돌아가신 날짜에 **48일을 더하면** 49재 날짜가 됩니다. (돌아가신 날 자체가 1일째이므로)

예: 8월 22일 별세 → 49재는 10월 9일

## 49재와 기제사의 차이

- **49재**: 돌아가신 후 49일째 한 번 지내는 의식 (불교식 전통)
- **기제사(기일제사)**: 매년 돌아가신 날(기일)에 반복해서 지내는 제사

49재는 한 번, 기제사는 해마다 반복된다는 점이 가장 큰 차이입니다.

발인 이후 절차가 더 궁금하다면 <a class="action-link" href="https://easybugo.com/guide/procedure.html">3일장 장례 절차 가이드</a>도 참고하세요.
