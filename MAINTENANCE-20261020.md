# 2026-10-20 사이트맵 정책 정합성 수정

/categories/, /tags/의 기존 noindex,follow 의도를 유지하며 sitemap에서 Kind=taxonomy 두 목록만 제외한다. 개별 category/tag term과 기존 글 URL·canonical·robots는 유지한다. 모바일 320/360/390px와 PC에서 보고서의 가로 잘림은 재현되지 않아 CSS는 수정하지 않는다.
검증: Hugo 빌드, sitemap 424 URL, taxonomy 두 URL 제외 및 HTML noindex 유지. 배포: 기존 main push Cloudflare 빌드. 롤백: 이 커밋 revert.
