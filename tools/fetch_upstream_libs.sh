#!/usr/bin/env bash
# 검증된 서드파티 KiCad 라이브러리를 업스트림에서 받아온다.
#
# 이 리포(KiCAD_LIB)는 "공식 라이브러리에 없는 커스텀 부품"만 담는다.
# 공식/서드파티 라이브러리는 각자의 업스트림 git 리포로 따로 두고 여기서 관리한다.
# 리포 안에 복사해 넣지 않는 이유: 라이선스가 분리돼 있고, 업스트림이 독립적으로
# 갱신되며, 3D 모델만 3.7GB라 커스텀 라이브러리 히스토리를 오염시킨다.
#
# 사용법:
#   tools/fetch_upstream_libs.sh            # 받기 (이미 있으면 건너뜀)
#   tools/fetch_upstream_libs.sh --update   # 고정 태그를 KICAD_LIB_TAG로 갱신
set -euo pipefail

DEST="${KICAD_UPSTREAM_DIR:-$HOME/03_Hardware/kicad-libraries}"
# KiCad 프로그램 버전과 반드시 일치시킬 것. KiCad 10 = 10.0.x
TAG="${KICAD_LIB_TAG:-10.0.5}"
GL="https://gitlab.com/kicad/libraries"

mkdir -p "$DEST"
cd "$DEST"

clone_tag() {  # $1=리포명 $2=태그
	if [ -d "$1/.git" ]; then
		echo "== $1: 이미 있음 ($(git -C "$1" describe --tags --always 2>/dev/null))"
		[ "${1:-}" ] && [ "${DO_UPDATE:-0}" = 1 ] && {
			echo "   -> $2 로 갱신"
			git -C "$1" fetch --depth 1 origin "refs/tags/$2:refs/tags/$2"
			git -C "$1" checkout -q "$2"
		}
		return
	fi
	echo "== $1 @ $2 받는 중..."
	git clone --depth 1 -b "$2" -q "$GL/$1.git"
}

clone_plain() {  # $1=URL $2=디렉터리명
	if [ -d "$2/.git" ]; then echo "== $2: 이미 있음"; return; fi
	echo "== $2 받는 중..."
	git clone --depth 1 -q "$1" "$2"
}

[ "${1:-}" = "--update" ] && DO_UPDATE=1 || DO_UPDATE=0
export DO_UPDATE

# KiCad 공식 라이브러리 (KLC 심사를 거친 검증본, CC-BY-SA 4.0 + exception)
clone_tag kicad-symbols   "$TAG"
clone_tag kicad-footprints "$TAG"
clone_tag kicad-packages3D "$TAG"   # 약 3.7GB

# Digi-Key 공식 KiCad 라이브러리 (Digi-Key 카탈로그 대조, CC-BY-SA 4.0)
clone_plain https://github.com/Digi-Key/digikey-kicad-library.git digikey-kicad-library

echo
echo "완료. 위치: $DEST"
du -sh "$DEST"/*/ 2>/dev/null || true
cat <<'EOS'

다음 단계 — KiCad > Preferences > Configure Paths 에 아래를 등록:
  KICAD10_SYMBOL_DIR     <위 경로>/kicad-symbols
  KICAD10_FOOTPRINT_DIR  <위 경로>/kicad-footprints
  KICAD10_3DMODEL_DIR    <위 경로>/kicad-packages3D
  MADUINOS_KICAD_LIB     이 리포의 절대경로

각 업스트림 리포 안의 sym-lib-table / fp-lib-table 이 위 변수를 그대로 쓰므로,
그 파일들의 (lib ...) 줄을 KiCad 전역 테이블에 합치면 등록이 끝난다.
EOS
