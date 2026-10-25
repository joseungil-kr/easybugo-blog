# 이지부고 블로그 검색 개선 — 표본 작업 기록

- 대상 저장소: joseungil-kr/easybugo-blog
- 기준 main: 0625920a6941a4bd43bf22e11164474297a48fdf
- 작업 브랜치: content/search-intent-top10-review
- 운영 반영: 하지 않음
- 기존 Draft PR #1: 별도 유지. 이 브랜치는 PR #1을 병합하거나 대체하지 않음.

## 검색 성과 전달자료와 해석 한계

전달된 GSC 자료상 2026-08-28~09-10 노출 2,235·클릭 17에서 09-11~09-24 노출 43·클릭 0으로 급락했고, 09-04~09-05 사이 색인 보고 수치도 크게 변했다. 10/16의 '크롤링됨-현재 미색인' 295개에는 글 113, 시설 169, 카테고리 9, 페이지 목록 3, 홈 1이 포함됐다. 10/25 sitemap.xml 제출은 성공·424 URL로 전달됐다. 이 수치는 전달자료이며 이번 세션에서 GSC API를 재조회한 값이 아니다. 구체적인 제외 원인은 확정되지 않았고, 콘텐츠 품질이나 사용자 지시를 원인으로 단정하지 않는다.

## 저장소·배포 확인

- main의 현재 SHA는 위 기준 SHA와 일치했다.
- 기존 Draft PR #1은 open/draft 상태이며 base main SHA가 위 SHA, head SHA가 1b4bcaa25594b029281ab67c76f13c3a601a7461이다. PR은 회사 부고 제목 수정과 세종 시설 중복 canonical 정합성만 다룬다.
- 저장소에는 GitHub 연결 도구를 통한 파일 읽기·파일 수정·브랜치 생성·PR 생성 기능이 있다. 수정은 별도 브랜치에서만 한다.
- 저장소 트리에서 .github/workflows 파일이 확인되지 않았고 Actions runs 조회도 0건이었다. 따라서 이 연결만으로 자동 빌드·CI 실행을 입증할 수 없다. 로컬 빌드는 별도 실행·검증이 필요하다.
- 운영 main 반영·배포는 하지 않는다.

## 글 183개 1차 분류

아래 분류는 main 트리의 파일명/슬러그를 기준으로 한 작업 큐 분류다. 모든 글의 본문을 전부 읽고 의미 유사도까지 판정한 최종 감사 결과로 해석하지 않는다. 실제 통합·삭제 판단 전에는 본문과 내부 링크, 검색 의도, 기존 FAQ를 개별 대조해야 한다.

| 1차 분류 | 수 | 우선 검수 기준 |
|---|---:|---|
| 관계별 조문·위로문자 | 24 | 발신인-상주 관계, 고인 호칭, 거리감별 문구가 실제로 다른지 검수 |
| 부고 작성·발송·문구 | 47 | 부고 제목/본문/전달 채널/수신자 상황을 구분하고 예시 중복 점검 |
| 조문·상주 예절 | 19 | 관습과 의무 규정을 구분, 지역·종교 차이는 단정하지 않음 |
| 장례 절차·시설·비용 | 30 | 최신 공공/공식 출처와 기준일 확인, 출처 없는 가격은 제거 또는 보류 |
| 사망 후 행정·상속·보험 | 32 | 법령·공공기관 원문 및 시행일 확인, 법률 조언처럼 단정하지 않음 |
| 기타·계산·디지털 부고 | 31 | 도구/계산기 기능 검증, 실제 사용 절차와 콘텐츠 목적 점검 |
| **합계** | **183** | 파일 수는 저장소 트리 기준 |

### 우선순위

1. **유지·보강 우선:** 검색 의도가 분명하고 독립적인 실용 답변이 있는 글. URL과 기존 FAQ를 보존하며 정확성·사례·내부 링크를 보강한다.
2. **출처 확인 우선:** 장례 비용, 시설 운영, 공공지원, 상속·보험·신고기한, 종교·예절 등 사실 확인이 필요한 글. 출처·기준일 확인 전에는 액수나 규정을 새로 단정하지 않는다.
3. **통합 후보 검토:** 제목이 비슷하다는 이유만으로 합치지 않는다. 실제 본문·검색 의도·유입·링크를 대조한 뒤 중복 정도와 URL 변경 위험을 먼저 제시하고 승인 없이 통합하지 않는다.
4. **유지하되 차별화:** 관계별 부고·위로문자. 일부 본문이 유사해도 FAQ와 검색 상황이 다를 수 있으므로 전체 페이지 유사도로 과장하지 않는다.

## 검색 상위 표본 10개

별도 브랜치에서 다음 10개 글을 검색 목적에 맞게 보강했다. URL, 날짜, 기존 FAQ는 유지했고 일부 FAQ를 추가했다. 단순히 관계명만 바꾸거나 문장 수만 늘리는 대신, 발신인·상주 관계, 실제 사용 문구, 호칭 확인, 실수 방지, 관례와 확정 규칙의 차이를 분명히 했다.

- in-law-obituary-message: 사위/딸 및 장인·장모 호칭과 부고 제목 구분
- husbands-father-condolence-text: 직장·친구·불참 상황별 위로문자, 피할 표현
- eldest-uncle-condolence-text: 백부/숙부 차이와 사촌에게 보내는 문구
- maternal-grandmother-condolence-text: 외조모/외조부 구분과 호칭별 문구
- husbands-mother-condolence-text: 시모상/모친상 구분, 상황별 위로문자
- condolence-money-name-position: 봉투 앞면/뒷면, 소속 표기, 동명이인 대응
- wife-condolence-text: 배우자상을 당한 상주에게 보낼 말과 감정 지시 표현 회피
- guestbook-writing-guide: 부의록 기록 항목, 장례 후 활용, 개인정보 취급 주의
- mourning-armband-position: 일반적인 왼팔 관례와 현장 지침 우선
- younger-uncle-condolence-text: 숙부/백부 구분과 가족 호칭 확인

관습 정보는 '일반적', '경우가 많음'으로 표현하고 예외가 있을 수 있음을 명시했다. 조의금 액수나 시설별 운영을 보편적 규칙으로 단정하지 않았다.

## 시설 228개 검수 계획

시설 페이지는 4개 유형(장례식장·봉안시설·자연장지·화장시설)의 콘텐츠 어댑터, data/regions.json, layouts/partials/facility-items.html에서 생성되는 구조를 확인했다. 목록 렌더링은 이름·주소와 데이터가 있는 경우에만 전화, 홈페이지, 빈소/안치/화장로/주차/편의시설 정보를 출력한다.

시설별 검수 항목:
- 공공데이터 제공기관·원본 URL·자료 기준일·마지막 갱신일을 기록
- 시설명·주소·유형·지역 소속이 원본과 일치하는지 확인
- 전화·홈페이지·운영시간·요금은 원본에 있을 때만 노출하고, 없는 값은 생성하지 않음
- 같은 시설의 중복 레코드와 주소·시설명 불일치는 통합 전에 근거와 영향 확인
- 지역 설명은 데이터로 확인할 수 있는 고유 사실만 추가

이번 표본 브랜치에서는 시설 데이터, 시설 URL, sitemap, robots, canonical을 변경하지 않았다. 시설 228개 각각의 원본 데이터 대조는 아직 미완료이며 별도 검수 단계로 남긴다.

## 검증·다음 단계

- 이번 변경은 콘텐츠 10개와 이 기록 파일에 한정한다.
- GitHub 파일 수정 API가 반환한 commit SHA와 blob SHA를 기록하고, 브랜치에서 파일을 다시 읽어 diff를 검수한다.
- Hugo 빌드 및 회귀검사를 실제 실행하지 못했다면 성공으로 보고하지 않는다.
- PR은 Draft로 열어 검토 가능하게 하되, main 병합이나 운영 배포를 유발하지 않는다.
- 검색 회복은 코드 변경 완료와 별개다. GSC의 색인·노출 추세가 실제로 개선되기 전에는 회복 완료로 판단하지 않는다.


## 추가 검수 2026-10-25 — 콘텐츠 정확성 보완

이번 추가 수정은 같은 PR #2 브랜치에서 진행했다. 기존 보고서의 10개 표본 요약은 초기 단계 기록이며, 아래의 상세 표가 현재 검수 상태와 변경 SHA를 대체한다.

| 파일 | 원래 검색 의도 | 수정 전 문제 | 수정 후 고유한 정보 | 확인한 근거 | 남은 미확인 | 변경 SHA |
|---|---|---|---|---|---|---|
| in-law-obituary-message.md | 장인·장모상 표현과 부고 제목 확인 | FAQ에서 며느리는 부친상·모친상을 그대로 쓴다고 단정해 본문과 불일치 | 고인·부고 당사자·실제 전달자·관계 4개 구분. 제3자 전달 예시. 빙부·빙모는 관습적 용법이며 단일 정답으로 규정하지 않음 | 국립국어원 온라인가나다, 2026-02-03 https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&pageIndex=1&qna_seq=327052 | 실제 기관별 부고 양식은 별도 확인 필요 | c690451433de9cb84e343fd9802f4c9292b5915d |
| husbands-father-condolence-text.md | 시부상 뜻과 상주에게 보낼 위로 | 부고 제목의 일반적 표기를 발신인·당사자·대리 전달 상황과 충분히 구분하지 않음 | 지인에게 위로하는 문장, 고인 호칭을 모를 때의 문장, 대리 전달 문구를 분리 | 관계 표현을 설명형으로 재작성. 위로문구는 편집자 작성 예시 | 시부상 실제 부고 제목의 사용 빈도는 검증하지 않음 | a7bc4c7cd807f1ac297edb6903ac1f6b2fcee05d |
| eldest-uncle-condolence-text.md | 백부상 뜻, 조카 당사자 또는 지인에게 위로 | 사촌에게 보내는 문구가 중심이어서 제3자가 자기 큰아버지인 듯 부를 위험 | 조카가 자기 가족 부고를 알리는 문구와 제3자가 지인에게 보내는 위로를 분리 | 국립국어원 한국어기초사전 백부 https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=58693&captchaNumber=&comment_user_name=&nation=eng&nationCode=6&viewTypes=on&wordComment= | 가족별 호칭은 차이가 있을 수 있음 | e1beb4374f4b5470e49df91102f7e42148fc534b |
| maternal-grandmother-condolence-text.md | 외조모상 뜻과 위로문자 | 외조부/외조모 이름만 바꾸는 형태가 강하고 상황 구분이 제한적 | 외조부·외조모 차이, 친구·지인·불참 상황별 문구 보강 | 이번 단계에서 독립적인 공공 원문은 확보하지 못함. 문구는 편집자 작성 예시 | 외조모 용어 사전 원문 및 실제 사용 관행 추가 검증 | 48f866b9fa19a863076baf21caca4a61536da0db |
| husbands-mother-condolence-text.md | 시모상 뜻과 위로문자 | 모친상으로 그대로 쓴다는 단정 및 제3자 검색 의도 구분 부족 | 시모상 용어 설명, 제3자 위로와 대리 부고 전달 분리 | 관계 표현을 설명형으로 재작성. 국립국어원은 빙부·빙모 관습 용법의 한계를 설명 | 시모상 실제 제목 사용 빈도는 검증하지 않음 | 32f531724ec18e217a11ef2b4cab7d57fc441f68 |
| condolence-money-name-position.md | 봉투 이름·소속 위치 | 뒷면 왼쪽 아래와 소속 위치를 근거 범위 없이 일반 규칙처럼 설명 | 국립국어원에서 확인된 앞면 부의·근조 안내와 이름 위치에 관한 장례 예시를 구분 | 국립국어원 자료 https://www.korean.go.kr/nkview/nklife/2008_3/2008_0313.pdf | 이름·소속의 정확한 위치를 정한 최신 공공 표준은 확인하지 못함 | cda560fb8e242d347a4a76a35f7ab5ca044832b2 |
| wife-condolence-text.md | 배우자상을 당한 상주에게 위로문자 | 상황별 발신인 맥락과 근거 범위가 제한적 | 직장 관계·친구·조문 불참 문구, 감정 지시 표현 회피 | 문구는 편집자 작성 예시 | 배우자상 제목 관행 및 종교별 표현은 추가 검증 필요 | 8d1ad7a55ca52adb512d51fd675fa2d67ac0d895 |
| guestbook-writing-guide.md | 조객록/부의록 작성·관리 | 방문 방명록과 부의금 장부를 거의 같은 의미로 설명, 개인정보 법률 의무와 권고가 섞임 | 조객록/방명록은 방문 기록, 부의록은 부의금 관련 기록이라는 구분. 법률 단정 대신 안전한 관리 권고 | 우리역사넷 https://contents.history.go.kr/mobile/km/view.do?levelId=km_005_0050_0010_0010_0040 ; KCI 학술자료 https://journal.kci.go.kr/koreal/archive/articlePdf?artiId=ART001480375 ; 세림병원 장례식장 https://selimfuneral.cafe24.com/mobile/service/service.php | 시설별 양식 통합/분리 방식은 차이가 있음. 법 적용은 상황별 검토 필요 | 6d4c1e92c82cda0063b5c5b8b90943e83169ddd0 |
| mourning-armband-position.md | 완장 착용 위치·줄 의미 | 왼팔과 줄 개수 의미를 출처 없이 일반 규칙처럼 설명 | 공공 원문에서 확인된 범위와 미확인 범위를 분리 | e하늘 장사정보서비스 장례용품 가격 예시 https://www.15774129.go.kr/portal/esky/fnlfac/fac_view.do?facilitycd=7000000666&facilitygroupcd=TBC0700001&loc=price&menuId=M0001000100000000&sanbundiv=N | 왼팔 착용과 줄 개수의 전국 공통 표준은 확인하지 못함 | d17c4327ba0fabd526665a53bc5c23736aca906e |
| younger-uncle-condolence-text.md | 숙부상 뜻과 위로문자 | 사촌 중심 예시 및 백부 글과 구조가 유사해 제3자가 친족 호칭을 혼동할 위험 | 조카가 부고를 알리는 예시와 제3자가 지인에게 위로하는 예시 분리 | 국립국어원 한국어기초사전 숙부 https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=64998&captchaNumber=&comment_user_name=&nation=eng&nationCode=6&viewTypes=on&wordComment= | 사전은 숙부를 아버지의 결혼한 남동생으로 풀이. 실제 가족 호칭은 별도 확인 필요 | b29c7695e063fe53a889e81543a5622bce462727 |

### 백부·숙부 글의 공통/고유 범위

- 공통: 사전상 관계, 부고 원문과 실제 가족 호칭을 우선 확인하는 원칙, 친족 용어만으로 조의금 액수를 단정하지 않는 안내.
- 백부 글의 고유 정보: 아버지의 맏형/큰아버지 관계, 조카가 자기 큰아버지 부고를 직접 알리는 예시, 제3자가 지인에게 위로하는 예시.
- 숙부 글의 고유 정보: 아버지의 결혼한 남동생/작은아버지 관계, 조카가 자기 작은아버지 부고를 알리는 예시, 제3자 위로에서 호칭을 모를 때 관계를 생략하는 예시.
- 남은 차별화 과제: 두 문서의 제목/문단 구조가 아직 유사하다. 다음 검수에서 백부 글은 맏형의 범위, 숙부 글은 결혼한 남동생이라는 사전 범위와 일상 호칭 차이를 더 분명히 검토한다. 통합하지 않는다.

### 연결 문서: condolence-money-by-relation.md

기존 금액표는 출처·조사 방법·기준일이 제시되지 않았고, '직계가족(형제자매 등)'이라는 표현은 친족 범주를 정확하게 구분하지 않았다. 이번 브랜치에서 금액표를 제거하고 상황별 판단 기준을 안내하도록 수정했다.

- 수정 후 SHA: 41fc49b1a582ef4a1b1d7c29ef8000d1f0c61bf7
- 다른 글에 출처 없는 금액표가 있는지는 183개 본문 전체 감사 중 우선 검색 대상으로 남긴다.
- 봉투 글은 조의금 금액의 정답 근거로 연결하지 않는다.

### 시설 228개 검수 — 확인 범위만 보고

- 구조 확인: 4개 시설 유형의 콘텐츠 어댑터 파일, data/regions.json(1,633,678 bytes), layouts/partials/facility-items.html의 표시 필드를 확인했다.
- 대표 표본: 실제 시설 데이터 행을 읽고 공공 원문과 대조한 표본은 0개다. data/regions.json은 연결 도구에서 파일이 너무 커 원문 내용을 읽지 못했다.
- 원본 출처·기준일: 현재 읽은 저장소 파일만으로 data/regions.json의 출처 URL과 자료 기준일을 확정하지 못했다.
- 개별 시설 대조: 원본 대조 완료 0/228, 미완료 228/228.
- 시설 데이터·시설 URL·sitemap·robots·canonical은 변경하지 않았다.
- 다음 검수는 데이터 생성 경로 또는 원본 출처 메타데이터를 확인하고 대표 시설 표본부터 대조하는 것이다. 출처 없는 가격·배송·운영시간은 생성하지 않는다.

### 빌드와 배포 검증 한계

저장소 트리에서 .github/workflows 파일이 보이지 않고 Actions runs 조회도 0건이었다. 이는 GitHub Actions 경로의 증거가 없다는 뜻이며 Cloudflare Pages 경로가 없다는 뜻은 아니다. 2026-10-25 후속 확인에서 Cloudflare Pages check run 121125858574의 성공과 미리보기 URL이 확인되었다. 다만 미리보기 HTML을 직접 열어 렌더링·내부 링크를 확인하는 단계는 접근 실패로 미검증이다. frontmatter·FAQ·파일 저장 재조회는 별도로 확인했다.

운영 main, PR #1, 운영 사이트, robots, sitemap, canonical, 시설 데이터, DNS·권한은 변경하지 않았다. PR #2는 Draft로 유지하며 검색 회복은 별도 GSC 증거가 나오기 전까지 미확정이다.


### Cloudflare Pages 확인 — 2026-10-25

- GitHub commit check API에서 Cloudflare Pages check run을 직접 확인했다.
- 직전 head d98e37bee3250840d791777e04205c0bcf7f8f51의 Cloudflare Pages 결과: completed / success. Preview URL은 https://4a06d96e.easybugo-blog.pages.dev, branch preview는 https://content-search-intent-top10.easybugo-blog.pages.dev.
- 이 결과는 Cloudflare가 해당 SHA에 대해 미리보기 빌드/배포를 성공으로 보고했다는 증거다. 웹 열람 도구에서는 preview 페이지 URL이 접근 불가로 반환되어 실제 렌더된 본문 HTML과 내부 링크를 직접 검수하지 못했다. 따라서 빌드 성공은 확인됐으나, 실제 렌더링 검수는 미완료다.
- 이 작업 기록을 추가 수정했으므로 새 head의 Cloudflare check run이 다시 실행될 수 있다. 최종 PR head의 check 상태를 별도로 재확인한다.


## 추가 독립 검수 2 — 예문 관계·FAQ 의도·독자용 문장 (2026-10-25)

### 예문에서 고인·상주·실제 발신인 구분

시부상·시모상 대리 전달 예문의 기존 문장 "김○○님의 부고 소식을 대신 전합니다"는 김○○ 본인이 고인인 것처럼 읽힐 수 있어 수정했다.

- 시부상: "김○○ 님의 시아버님 별세 소식을 대신 전합니다."
- 시모상: "김○○ 님의 시어머님 별세 소식을 대신 전합니다."
- 장인·장모상: "김○○ 님의 장인상 소식을 대신 전합니다."처럼 누구의 장인·장모인지 밝혀 적는다.
- 백부·숙부: 조카가 직접 자기 가족의 부고를 알리는 예문과, 제3자가 지인에게 위로를 전하는 예문을 분리했다. 제3자가 고인을 자신의 큰아버지·작은아버지처럼 부르지 않도록 안내한다.
- 이름과 빈소·발인 일정은 예시임을 명시하고, 실제 안내 원문을 확인해 대체하도록 유지했다.

### main 대비 기존 FAQ 검색 의도 보존

기존 질문의 문구를 무조건 그대로 유지하는 대신, 잘못된 답변의 단정은 수정하면서 유효한 질문 의도를 유지·재구성했다.

| 파일 | main의 기존 질문 의도 | 최신 처리 및 대응 위치 |
|---|---|---|
| in-law-obituary-message.md | 빙부·빙모 뜻 | FAQ 1에서 사전 의미와 관습적 사용의 한계를 설명 |
| in-law-obituary-message.md | 며느리가 시부모 부고를 알릴 때의 표현 | 원래 질문 복원. FAQ 2에서 일률적인 제목 규칙을 단정하지 않고 관계를 풀어 쓰는 대안 제시 |
| in-law-obituary-message.md | 딸이 직접 상주로 알릴 때의 표현 | 원래 질문 복원. FAQ 3에서 딸 본인 부모와 사위의 처가 부모를 구분하고 원본 부고 확인 안내 |
| husbands-father-condolence-text.md | 시부상은 며느리 입장에서만 쓰는가 | 원래 질문 복원. FAQ 1에서 용어 뜻과 검색자가 제3자일 가능성을 구분 |
| husbands-father-condolence-text.md | 며느리에게 위로문자를 보낼 때 주의할 표현 | 원래 질문 복원. FAQ 2에서 감정·가족관계를 단정하지 않는 표현 제시 |
| husbands-mother-condolence-text.md | 시모상은 며느리 입장에서만 쓰는가 | 원래 질문 복원. FAQ 1에서 같은 원칙 적용 |
| husbands-mother-condolence-text.md | 시부상과 위로문자를 다르게 써야 하는가 | 원래 질문 복원. FAQ 2에서 고인 호칭을 관계에 맞춰 바꾸도록 답변 |
| eldest-uncle-condolence-text.md | 백부·숙부 차이 | FAQ 1 유지 |
| eldest-uncle-condolence-text.md | 평소 왕래가 적은 큰아버지상에 문자를 보내야 하는가 | 원래 질문 복원. FAQ 2에서 조카와 제3자 상황을 나눠 답변 |
| younger-uncle-condolence-text.md | 결혼하지 않은 삼촌상도 숙부상인가 | 원래 질문 복원. FAQ 2에서 사전적 숙부의 범위와 가족의 일상 호칭을 구분 |
| guestbook-writing-guide.md | 부의록에 무엇을 적는가 | FAQ 1에서 부의금 접수 기록 중심으로 수정 |
| guestbook-writing-guide.md | 부의록은 누가 관리하는가 | 원래 질문 복원. FAQ 2에서 시설·가족의 역할 분담에 따라 달라짐을 설명 |
| condolence-money-name-position.md | 앞면에 이름을 적어도 되는가 | FAQ 1 유지. 확인된 국립국어원 안내와 위치 관례의 범위를 구분 |
| wife-condolence-text.md | 처상·실인상 중 어떤 표현이 맞는가 | FAQ 1 유지 |
| wife-condolence-text.md | 자녀가 어릴 때 누구에게 위로문자를 보내는가 | FAQ 2 유지 |
| mourning-armband-position.md | 완장 위치 | FAQ 1 유지. 전국 공통 규칙은 확인되지 않았다고 명시 |
| mourning-armband-position.md | 완장은 직접 준비해야 하는가 | FAQ 2 유지. 용품 등록만으로 모든 시설의 지급 방식을 단정하지 않음 |

### 독자용 본문에서 제작 메모 제거

백부·숙부·시부·시모 글에 있던 "금액표와 친족 분류는 별도 검수 대상으로 남아 있다" 또는 유사한 내부 진행상태 표현을 제거했다. 연결 문서 condolence-money-by-relation.md의 금액표는 이미 제거되어 있으며, 독자에게는 해당 페이지를 공식 금액 기준이 아닌 참고용 판단 자료로 안내한다. 다른 표본 글에서도 "이번 검수", "검수 대상", "추후 보완" 같은 제작 진행 메모가 남았는지 확인했고, 표본 11개에서 내부 진행상태를 독자에게 알리는 문장은 발견하지 못했다. 완장 글의 조사 한계는 독자에게 의미 있는 사실 범위 설명으로 재작성했다.

### 최신 변경 SHA — 해당 파일을 다시 읽어 확인

- in-law-obituary-message.md: e98b415b3a230495050eb3ce7e853551c52def72
- husbands-father-condolence-text.md: b3ffcae59b4812ff4124b418dcc9282b23028dba
- husbands-mother-condolence-text.md: 84f7aecab9aad1f6cc05546a10aef818fddae7a5
- eldest-uncle-condolence-text.md: aba5bc9f02ef68fc1a5e13246fc22273ba4753ba
- younger-uncle-condolence-text.md: b4c809843a30f86e0dad8d72cad41c7bb3ea5d7d
- guestbook-writing-guide.md: e7287e96127374f102d105626b7345af9ad6e143
- mourning-armband-position.md: 7fe728a2e2a11ec9ea03674935c586ff37f72acd

이 목록 외의 4개 표본(in-law 외 10개 중 maternal-grandmother, condolence-money-name-position, wife-condolence-text, condolence-money-by-relation)은 이번 단계에서 추가 본문 수정이 없었다. 다만 PR 최신 head에서 파일 재조회 및 FAQ·예문 검사를 다시 수행한다.

### 빌드와 미리보기 한계

이전 head 7f4c4940ce0dd85874950295c9508bbb673fab0c의 Cloudflare Pages check run 121125858574는 성공으로 보고되었고, preview URL https://8f815013.easybugo-blog.pages.dev 가 확인되었다. 사용자 제공 독립 검수에서는 미리보기와 11개 URL의 HTTP 200이 보고되었다. 이 대화에서는 미리보기 HTML을 직접 읽지 못했으므로, 본문·내부 링크의 실제 렌더링을 직접 검증했다고 주장하지 않는다. 현재 head의 새 Cloudflare check 결과를 별도로 확인해야 한다.


### 최종 재조회용 최신 SHA 및 상태 정정

위 표의 SHA는 최초/중간 수정 시점 값이다. 아래 SHA가 추가 검수 후 해당 파일을 다시 읽어 확인한 최신 blob SHA이므로 위 표보다 우선한다.

- in-law-obituary-message.md: 5b23251ec607b7469ebc78b830ebe4e6b89f083a
- husbands-father-condolence-text.md: 64070f658af4a6ebd9593c304dec1612ea512d68
- husbands-mother-condolence-text.md: 72755a4e5d40694894f3e7ce2cb0eac606227117
- eldest-uncle-condolence-text.md: e8a87a24c273108ffc81c0fa32688fcdf8d891d8
- younger-uncle-condolence-text.md: 2e590e1030555ae51cb86ff4abcdf2fa2e800dce
- guestbook-writing-guide.md: 07b24778cf793fa10aba5781c1d63306019c63a4
- mourning-armband-position.md: 78418f25395342a4d17f636f2c37c662ae2e54f1
- maternal-grandmother-condolence-text.md: 48f866b9fa19a863076baf21caca4a61536da0db
- condolence-money-name-position.md: cda560fb8e242d347a4a76a35f7ab5ca044832b2
- wife-condolence-text.md: 8d1ad7a55ca52adb512d51fd675fa2d67ac0d895
- condolence-money-by-relation.md: 41fc49b1a582ef4a1b1d7c29ef8000d1f0c61bf7

추가 수정 후 다시 확인한 FAQ 질문은 main의 기존 질문 의도를 유지하면서 답변을 정확하게 수정했다. 백부의 '평소 왕래가 적었던 경우', 숙부의 '결혼 안 한 삼촌상' 질문을 복원했고, in-law의 딸·며느리 질문과 시부·시모의 기존 질문도 복원했다. 잘못된 예전 답변은 복원하지 않았다.

Cloudflare check run 121125858574와 미리보기 URL 8f815013에 대한 HTTP 200 및 새 본문 확인은 사용자 제공 독립 검수 결과로 기록한다. 이 세션의 웹 열람 도구는 해당 preview URL에 접근할 수 없어 실제 HTML 소스의 직접 재검수는 수행하지 못했다. 미리보기의 X-Robots-Tag noindex는 미리보기 환경의 신호이며 운영 색인 복구의 증거가 아니다.


## 추가 표본 편집 — 봉투 위치·완장 안내·딸의 부고 제목 (2026-10-25)

이번 범위는 세 문서에 한정했다. 나머지 글은 수정하지 않았다.

### 1) condolence-money-name-position.md

- **원래 의도:** 봉투 앞면과 뒷면에서 이름·소속을 실제 어디에 적는지 알고 싶음.
- **수정 전 문제:** 이름과 소속 위치에 관한 설명은 있었지만, 독자가 바로 따라 쓸 수 있는 위치 도식이 없었음.
- **수정:** 앞면 '賻儀(부의)'와 뒷면 이름·소속을 구분한 ASCII 텍스트 도식을 추가. 도식은 편집자가 만든 배치 예시이며 공식 표준 도식이라고 주장하지 않음.
- **원문 확인:** 분당차병원 장례식장 '장례상식·조의금' 안내는 초상 봉투 문구로 부의가 가장 일반적이며 근조·조의·전의 등도 사용한다고 설명함: https://bundang.chamc.co.kr/funeral/ProcInfo/commonSense.aspx
- **위치 참고:** 충청 장례길잡이의 부의금 봉투 표기 안내는 뒷면 이름 위치와 소속 표기 예시를 설명함: https://doeum.kr/magazine/blog/%EC%9E%A5%EB%A1%80_%EC%98%88%EC%A0%88/condolence-money-envelope-writing-guide
- **확인 한계:** 분당차병원 원문에서 이름의 정확한 위치 도식은 확인되지 않았으므로 병원 원문이 그 위치를 정한다고 서술하지 않음. 위치 도식은 편집 예시로 분리.
- **최신 blob SHA:** dbba94ff94f5053e67197951048b468e0b8c32ff

### 2) mourning-armband-position.md

- **원래 의도:** 완장을 어느 팔·어느 위치에 착용하는지, 줄 수는 무엇을 뜻하는지 알고 싶음.
- **수정 전 문제:** 전국 공통 기준을 확인하지 못했다는 설명이 답변의 대부분을 차지했고, 실제 기관의 사례가 없었음.
- **원문 확인 A:** 충북대학교병원 장례식장 장례예절 페이지는 완장 줄 수별 대상을 설명함: 두 줄은 아들과 사위(아들이 없으면 장손), 한 줄은 기혼 복인, 무줄은 미혼 복인(주로 손자). https://www.cbnuh.or.kr/funeral/sub05_03.do
- **원문 확인 B:** 삼고상조의 장례 가이드는 완장을 위팔에 두르고 왼팔에 착용하는 사례를 설명하며, 지역·가풍에 따른 차이가 있을 수 있다고 밝힘: https://samgolife.co.kr/magazine/blog/f-guide/%EC%83%81%EC%9E%A5%EC%99%84%EC%9E%A5-%EC%A2%85%EB%A5%98%EC%99%80%EC%B0%A9%EC%9A%A9%EC%9C%84%EC%B9%98
- **수정:** 해당 자료를 기관별 사례로 범위를 한정해 본문에 연결. 완장 가격표는 착용법의 근거로 사용하지 않음.
- **확인 한계:** 위 두 원문이 전국 공통 규칙을 정하는 것은 아님. 충북대학교병원 원문은 줄 수별 대상을 설명하지만 왼팔 위치는 명시하지 않음. 삼고상조 원문은 왼팔·위팔 위치를 설명하지만 모든 시설에 적용된다고 단정할 수 없음.
- **최신 blob SHA:** 4059442f5924005329831b87d53cc9db44903310

### 3) in-law-obituary-message.md

- **원래 의도:** 딸이 본인 부모의 부고를 직접 알릴 때 어떤 제목을 쓸지 알고 싶음.
- **수정 전 문제:** 답변이 원본 부고와 관계를 확인하라는 안내에 머물고, 실제 제목 예시가 없었음.
- **수정:** 아버지의 경우 '[부고] 김○○ 님의 부친 故 이○○ 님 별세', 어머니의 경우 '[부고] 김○○ 님의 모친 故 이○○ 님 별세'를 예시로 추가. 상주(딸)와 고인(돌아가신 부모)을 별도 표기하고, 이름·일정은 예시임을 명시.
- **근거 범위:** 제목은 관계를 분명히 하기 위해 직접 작성한 실용 예시이며, 국립국어원이 이를 유일한 공식 제목으로 정했다는 주장은 하지 않음. 빙부·빙모 관습 용례의 한계는 국립국어원 온라인가나다 답변을 인용함: https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&pageIndex=1&qna_seq=327052
- **최신 blob SHA:** b38a9ee748f202158ae66ed1e6d4b09c2c11a3c2

### 최신 표본 SHA와 확인 상태

위 세 SHA는 수정 후 파일을 다시 읽어 확인한 blob SHA다. 최신 PR head에 대해서는 별도로 Cloudflare Pages check run을 확인한다. 빌드 성공과 실제 HTML 소스 열람은 별도 검증으로 취급하며, 미리보기 접근 실패를 성공으로 간주하지 않는다.
