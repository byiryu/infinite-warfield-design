#!/bin/bash
# 고아 페이지 검사 — push 전 실행 (ApplicationProject/_docs/workflow.md §8.7)
# 규칙: 모든 .html 은 인덱스 체인(루트 index → 프로젝트 index → 페이지)에서 도달 가능해야 한다.
#  - 일반 페이지: 다른 html 어딘가에서 파일명 참조 존재해야 함
#  - 하위 index.html: 디렉토리 밖에서 그 디렉토리로 들어오는 링크(`{dir}/` 또는 `{dir}/index.html`) 존재해야 함
cd "$(dirname "$0")" || exit 1
fail=0
# .unlisted — 의도적 비공개(unlisted) 경로 prefix 목록. 인덱스 비연결 허용 (URL 직접 접근 전용, noindex 메타 의무)
unlisted=""
[ -f .unlisted ] && unlisted=$(grep -v '^#' .unlisted | grep -v '^$')
is_unlisted(){ for p in $unlisted; do case "$1" in "$p"*) return 0;; esac; done; return 1; }
while IFS= read -r f; do
  rel="${f#./}"
  if is_unlisted "$rel"; then
    grep -q 'name="robots" content="noindex' "$rel" || { echo "UNLISTED WITHOUT NOINDEX: $rel"; fail=1; }
    continue
  fi
  base="$(basename "$rel")"
  dir="$(dirname "$rel")"
  if [ "$base" = "index.html" ]; then
    [ "$rel" = "index.html" ] && continue   # 루트 랜딩은 진입점
    dirbase="$(basename "$dir")"
    if ! grep -rl --include="*.html" -e "${dirbase}/index.html" -e "${dirbase}/\"" . 2>/dev/null | grep -v "^\./${dir}/" | grep -q .; then
      echo "ORPHAN INDEX: $rel  (부모 인덱스에서 ${dirbase}/ 링크 필요)"
      fail=1
    fi
  else
    if ! grep -rl --include="*.html" "$base" . 2>/dev/null | grep -v "^\./${rel}$" | grep -q .; then
      echo "ORPHAN: $rel  (어느 인덱스에서도 참조 없음)"
      fail=1
    fi
  fi
done < <(find . -name "*.html" -not -path "./.git/*")
# 죽은 placeholder 링크 검사 (href="#" disabled 카드 금지)
if grep -rn --include="*.html" 'class="link disabled"' . >/dev/null 2>&1; then
  echo "DEAD LINK (disabled placeholder):"
  grep -rn --include="*.html" 'class="link disabled"' .
  fail=1
fi
[ $fail -eq 0 ] && echo "OK — 고아 페이지 0 · 죽은 링크 0"
exit $fail
