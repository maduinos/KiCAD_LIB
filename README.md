# Maduinos KiCad Library

Maduinos 하드웨어 작업용 개인 KiCad 라이브러리. 심볼 / 풋프린트 / 3D 모델을 한 리포에서 관리한다.
대부분 UltraLibrarian에서 받은 벤더 데이터를 정리한 것이라, **보드 발주 전 데이터시트 대조 검증이 필수**다.

## 구조

```text
symbols/
  Maduinos_FPGA.kicad_sym          AMD/Xilinx Zynq-7000, Zynq UltraScale+
  Maduinos_Memory.kicad_sym        DDR3, eMMC, QSPI NOR flash
  Maduinos_Power_Analog.kicad_sym  PMIC, ADC, LED driver
footprints/
  Maduinos_BGA.pretty/             BGA / FBGA 패키지 (16)
  Maduinos_SMD.pretty/             DFN / QFN / TSSOP / HTSSOP 패키지 (12)
3dmodels/
  Maduinos.3dshapes/               STEP 모델 (10)
kicad/
  sym-lib-table                    라이브러리 테이블 조각 (아래 설치 참고)
  fp-lib-table
tools/
  check_library.py                 무결성 검사 스크립트
```

### 네이밍 규칙

- **`.kicad_sym` 파일 하나 = KiCad 라이브러리 하나.** 부품 하나당 파일 하나로 쪼개지 말 것.
  새 부품은 카테고리에 맞는 기존 파일에 추가한다. 새 카테고리가 필요할 때만 파일을 늘리고,
  그때 `kicad/sym-lib-table`에도 한 줄 추가한다.
- **`.pretty` 폴더 이름이 곧 라이브러리 닉네임**이 된다. 심볼의 Footprint 속성은 항상
  `Maduinos_BGA:CLG400_AMD` 처럼 `라이브러리:풋프린트` 형식이어야 한다. 접두어가 없으면
  스키매틱→PCB 업데이트에서 풋프린트가 할당되지 않는다.
- **풋프린트 파일명 == 파일 안의 `(footprint "...")` 이름.** 이름에 `/`, `&`, 공백을 쓰지 않는다.
- **3D 모델 파일명 == 대응 풋프린트의 기본 이름** (`-L`/`-M` 밀도 접미어 제외).
  이 규칙 덕분에 `tools/check_library.py`가 누락/고아 모델을 자동으로 잡아낸다.

### IPC 밀도 변형 접미어

UltraLibrarian은 IPC-7351 밀도 레벨별로 풋프린트를 함께 내보낸다. 셋 다 보관하되 기본값은 노멀이다.

| 접미어 | IPC 밀도 레벨 | 용도 |
|---|---|---|
| `-M` | Level A / Most (최대) | 저비용·저정밀 조립, 손납땜, 수동 리워크 |
| 없음 | Level B / Nominal (노멀) | **기본값.** 일반 양산 조립 |
| `-L` | Level C / Least (최소) | 고밀도 보드, 정밀 조립 라인 |

`PW0016A`는 벤더가 `IPC_A`(Most) / `IPC_B`(Nominal) / `IPC_C`(Least) / `MFG`(제조사 권장) 형태로
따로 내보냈다. 심볼 기본값은 노멀인 `PW0016A-IPC_B`.

## 설치

이 라이브러리는 절대경로가 아니라 환경변수 `MADUINOS_KICAD_LIB` 로 자기 자신을 참조한다.
따라서 리포를 어디에 클론하든, 어느 PC에서든 경로 수정 없이 동작한다.

**1) 경로 변수 등록** — KiCad에서 `Preferences > Configure Paths`:

| Name | Path |
|---|---|
| `MADUINOS_KICAD_LIB` | 이 리포의 절대경로 (예: `/home/maduinos/00_GitHub/maduinos/KiCAD_LIB`) |

**2) 라이브러리 등록** — `kicad/sym-lib-table` 과 `kicad/fp-lib-table` 안의 `(lib ...)` 줄들을
KiCad 전역 테이블에 **추가**한다. 전역 테이블 위치는 보통 `~/.config/kicad/<버전>/` 이다.

> 파일을 통째로 덮어쓰지 말 것. KiCad 기본 라이브러리 등록이 전부 날아간다.
> GUI로 하려면 `Preferences > Manage Symbol Libraries`에서 파일을 하나씩 추가해도 결과는 같다.

프로젝트마다 라이브러리 버전을 고정하고 싶으면, 전역 등록 대신 두 파일을 프로젝트 폴더에
복사해 프로젝트 로컬 테이블로 쓰고 이 리포를 서브모듈로 붙인다.

**3) 3D 모델** — 풋프린트 안에 `${MADUINOS_KICAD_LIB}/3dmodels/...` 로 이미 박혀 있으므로,
1번만 되어 있으면 추가 설정이 필요 없다.

## 검사

```bash
python3 tools/check_library.py
```

괄호 균형, 파일명↔내부이름 일치, 심볼→풋프린트 링크 해석 가능 여부, 3D 모델 참조 무결성을
확인하고 문제가 있으면 exit 1. 부품을 추가하면 커밋 전에 돌릴 것.

## 검증 노트 (발주 전 체크)

- 모든 심볼 핀아웃을 **최신** 데이터시트와 대조한다. 벤더 자동생성 데이터는 개정 이력이 반영이 늦다.
- BGA는 1번 핀 방향, 볼 피치, 코트야드, 페이스트, 솔더마스크를 PCB 업체 공정 한계와 대조한다.
- **3D 모델의 원점·회전은 아직 육안 검증이 안 되어 있다.** 현재 전부 offset/rotate 0으로 들어가
  있으므로, 각 풋프린트를 처음 쓸 때 3D 뷰어에서 몸체가 패드와 맞는지 확인하고 어긋나면
  해당 `.kicad_mod`의 `(offset ...)` / `(rotate ...)` 값을 조정한다.
- 3D 모델은 기구 간섭 확인용 참고물이다. 패키지 도면 검토를 대체하지 않는다.

## 라이선스

라이선스 미선정. 선정 전까지는 Maduinos 프로젝트 외부에서 쓰기 전에 리포 소유자에게 문의할 것.
벤더에서 파생된 패키지 데이터는 원 제조사의 이용 약관을 따른다.
