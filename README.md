# infinite-warfield-design

infinite-warfield(좌우 대치 코스트 실시간 소환 게임)의 **디자인 시각화 보드** 공개 레포.
출시 전 디자인 검토용 — 렌더 보드·와이어프레임·에셋 추적·분석 보드.

- **랜딩:** [`index.html`](index.html) → GitHub Pages `https://byiryu.github.io/infinite-warfield-design/`
- **보드:** `sanity/*.html`(렌더·와이어) · 루트 `*.html`(개요·에셋·코덱스·밸런스·감사)
- **상태 규약:** 진행 중(검토/결정 대기) = 점선·비활성(dimmed) · 확정 = 활성 · 구버전 = archived
- **고아 0:** 모든 `.html` 은 인덱스 체인에서 도달 가능. `check_orphans.sh`(pre-commit 강제)

## 소유 / SoT
- 이 레포 = **시각화 보드만**(디자인 세션 소유·`previews push` 미러).
- 디자인 SoT(.md: brief·design-system·wireframes·asset-manifest) = `byiryu/infinite-warfield`(비공개) `design/`.
- spec·PLAN·balance-plan·ideas 캡처 = `byiryu/infinite-warfield`(비공개) 루트(PM).

## 로컬
```
# 작업 위치 = projects/infinite-warfield/design/boards/ (프로젝트 레포에선 gitignore)
git config user.name byiryu && git config user.email byiryustudio@gmail.com
cp hooks/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit   # author + 고아 검사
./check_orphans.sh   # push 전 수동 검사도 가능
```

폰 리뷰 = Pages URL 직접 접근(로컬 서버 불요). 보드는 self-contained(이미지 base64 임베드).
