# 2026-10-20 사이트맵 정책 정합성 수정

/categories/, /tags/의 기존 noindex,follow 의도를 유지하며 sitemap에서 Kind=taxonomy 두 목록만 제외한다. 개별 category/tag term과 기존 글 URL·canonical·robots는 유지한다. 모바일 320/360/390px와 PC에서 보고서의 가로 잘림은 재현되지 않아 CSS는 수정하지 않는다.
검증: Hugo 빌드, sitemap 424 URL, taxonomy 두 URL 제외 및 HTML noindex 유지. 배포: 기존 main push Cloudflare 빌드. 롤백: 이 커밋 revert.


# 2026-10-21 지역 제목 구분

광주·대구·인천 서구 장례식장 페이지가 동일한 제목과 설명을 사용하는 문제를 공개 응답에서 확인했다. 4개 기존 콘텐츠 어댑터가 시군구 페이지를 생성할 때 기존 데이터의 시도명을 제목·설명 앞에 붙인다. 시도 허브와 세종처럼 시도·시군구명이 같은 경우는 중복 표기하지 않는다.

Hugo 빌드 및 지역 페이지 224개 검사 완료: 시군구 154개 HTML만 변경, sitemap 424개 URL 집합 유지, canonical·링크 목적지 유지. 세 도시의 동일 제목 1종이 구별되는 제목 3종으로 바뀌는 회귀검사를 통과했다. 시설 데이터·전화·주소·기존 URL은 그대로다. 배포/공개 결과는 Naver-SEO-Lab/operations/2026-10-21-diagnostic-completion에서 관리한다.
