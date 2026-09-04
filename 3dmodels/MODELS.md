> 만든 사람: maduinos<br>
> 문서 만든 날짜: 2026-08-01<br>
> https://maduinos.blogspot.com/

# 3D 모델 대응표

KiCad 공식 라이브러리는 **풋프린트에 `(model ...)` 참조는 있지만 STEP 파일이 실제로는 없는**
경우가 많다 (기여자가 3D를 안 올린 패키지). 아래 STEP는 UltraLibrarian에서 받은 벤더 형상으로,
공식이 못 채우는 그 빈틈을 메운다. 풋프린트 자체는 공식 것을 쓴다.

| STEP 파일 | 붙일 풋프린트 | 공식 3D 유무 |
|---|---|---|
| `CLG400_AMD.step` | `Package_BGA:Xilinx_CLG400` | **없음** — 이 파일 필요 |
| `CLG400_ZYNQ-7000_AMD.step` | `Package_BGA:Xilinx_CLG400` | **없음** — 위와 택일 |
| `FFG676_FFV676_AMD.step` | `Package_BGA:Xilinx_FFG676` | **없음** — 이 파일 필요 |
| `KLMBG2JENB-B041_SAM.step` | `Package_BGA:LFBGA-153_11.5x13mm_Layout14x14_P0.5mm` | **없음** — 이 파일 필요 |
| `DAP32_4P36X4P11.step` | `Package_SO:HTSSOP-32-1EP_6.1x11mm_P0.65mm_EP5.2x11mm_Mask4.11x4.36mm` | **없음** — 이 파일 필요 |
| `RSL0048B.step` | `Package_DFN_QFN:QFN-48-1EP_6x6mm_P0.4mm_EP4.3x4.3mm` | **없음** — 이 파일 필요 |
| `BGA625C80P25X25_2100X2100X343N.step` | `Package_BGA:BGA-625_21.0x21.0mm_Layout25x25_P0.8mm` | 있음 (공식 것 써도 됨) |
| `PW0016A.step` | `Package_SO:TSSOP-16_4.4x5mm_P0.65mm` | 있음 (공식 것 써도 됨) |
| `FBGA98_K4B4G1646E-BCMA_SAM.step` | `Maduinos_BGA:FBGA98_K4B4G1646E-BCMA_SAM` | 풋프린트도 이 리포 것 (참조 내장) |
| `W-PDFN-8MLP8_W9_MRN.step` | `Maduinos_SMD:W-PDFN-8MLP8_W9_MRN` | 풋프린트도 이 리포 것 (참조 내장) |

## 붙이는 방법

아래 두 개는 이 리포의 풋프린트 안에 `(model ...)`로 이미 박혀 있어 할 일이 없다.

- `FBGA98_K4B4G1646E-BCMA_SAM`
- `W-PDFN-8MLP8_W9_MRN`

나머지는 공식 풋프린트를 쓰므로 보드에서 직접 붙인다. PCB 편집기에서 해당 풋프린트를 선택 →
`Footprint Properties` → `3D Models` 탭 → 아래 경로를 추가:

```
${MADUINOS_KICAD_LIB}/3dmodels/Maduinos.3dshapes/<파일명>.step
```

같은 부품을 여러 보드에서 반복해서 쓸 거라면, 공식 풋프린트를 프로젝트 로컬 라이브러리로
복사한 뒤 거기에 `(model ...)`을 넣어 두는 편이 낫다. 공식 라이브러리 원본은 수정하지 말 것 —
AppImage를 새 버전으로 교체하면 사라진다.

## 주의

모든 STEP의 offset/rotate가 0으로 되어 있고 **육안 검증 전이다.** 처음 붙일 때 3D 뷰어에서
몸체가 패드에 맞는지 확인하고, 어긋나면 3D Models 탭에서 offset/rotation을 조정한다.
