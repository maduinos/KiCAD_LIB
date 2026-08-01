#!/usr/bin/env python3
"""라이브러리 무결성 검사.

  - 심볼/풋프린트 s-expression 괄호 균형 (KiCad 10 .kicad_symdir 구조)
  - 풋프린트 파일명 == 내부 footprint 이름
  - 심볼의 Footprint 속성이 "라이브러리:이름" 형식이고 실제로 존재하는지
  - 모든 풋프린트가 (model ...) 를 갖고, 그 STEP 파일이 실재하며, 미사용 모델이 없는지

실행: python3 tools/check_library.py   (문제 있으면 exit 1)
"""
import pathlib, re, sys, os
root = pathlib.Path(__file__).resolve().parent.parent

def balanced(t):
    d=0; instr=esc=False
    for c in t:
        if esc: esc=False
        elif instr:
            if c=="\\": esc=True
            elif c=='"': instr=False
        else:
            if c=='"': instr=True
            elif c=="(": d+=1
            elif c==")":
                d-=1
                if d<0: return False
    return d==0

ok=True
print("== 심볼 라이브러리 ==")
sym_links=[]
for d in sorted((root/"symbols").glob("*.kicad_symdir")):
    files=sorted(d.glob("*.kicad_sym"))
    print(f"{d.name}: 심볼 {len(files)}개")
    for f in files:
        t=f.read_text(); b=balanced(t); ok &= b
        names=re.findall(r'\(symbol "([^"]+)"',t)[:1]
        fps=re.findall(r'\(property "Footprint" "([^"]*)"',t)[:1]
        if not names: print(f"    !! {f.name}: symbol 없음"); ok=False; continue
        if names[0]!=f.stem: print(f"    !! {f.name}: 내부명 {names[0]} != 파일명"); ok=False
        if not b: print(f"    !! {f.name}: 괄호 FAIL")
        fp=fps[0] if fps else ""
        sym_links.append((names[0],fp))
        print(f"    {names[0]:24s} -> {fp}")

UPSTREAM = pathlib.Path(os.environ.get("KICAD_UPSTREAM_DIR",
              pathlib.Path.home()/"03_Hardware/kicad-libraries"))/"kicad-footprints"
print("\n== 풋프린트 라이브러리 ==")
fpnames={}
for d in sorted((root/"footprints").glob("*.pretty")):
    lib=d.name[:-7]; fpnames[lib]=set()
    for f in sorted(d.glob("*.kicad_mod")):
        t=f.read_text(); b=balanced(t); ok &= b
        internal=re.search(r'\(footprint\s+"?([^"\s)]+)"?',t).group(1)
        stem=f.stem; fpnames[lib].add(stem)
        flag=[]
        if not b: flag.append("괄호FAIL")
        if internal!=stem: flag.append(f"이름불일치({internal})")
        if flag: ok=False; print(f"  !! {lib}:{stem}  {' '.join(flag)}")
    print(f"{lib}.pretty: {len(fpnames[lib])}개")

upstream_ok = UPSTREAM.is_dir()
if upstream_ok:
    for d in sorted(UPSTREAM.glob("*.pretty")):
        fpnames.setdefault(d.name[:-7], set()).update(f.stem for f in d.glob("*.kicad_mod"))
    print(f"업스트림 {UPSTREAM}: 라이브러리 {len(list(UPSTREAM.glob('*.pretty')))}개 인식")
else:
    print(f"!! 업스트림 없음 ({UPSTREAM}) - 공식 라이브러리 링크는 검사 생략")

print("\n== 심볼->풋프린트 링크 해석 ==")
for n,fp in sym_links:
    if ":" not in fp: print(f"  !! {n}: 접두어 없음 '{fp}'"); ok=False; continue
    lib,name=fp.split(":",1)
    if lib not in fpnames: print(f"  !! {n}: 라이브러리 '{lib}' 없음"); ok=False
    elif name not in fpnames[lib]: print(f"  !! {n}: 풋프린트 '{name}' 없음"); ok=False
    else: print(f"  OK {n:24s} -> {fp}")

print("\n== 3D 모델 참조 ==")
models={p.name for p in (root/"3dmodels/Maduinos.3dshapes").glob("*")}
used=set(); nomodel=[]
for f in sorted((root/"footprints").glob("*.pretty/*.kicad_mod")):
    refs=re.findall(r'\(model\s+"([^"]+)"',f.read_text())
    if not refs: nomodel.append(f.stem); continue
    for r in refs:
        used.add(r.rsplit("/",1)[-1])
        if r.rsplit("/",1)[-1] not in models:
            print(f"  !! {f.stem}: 모델파일 없음 {r}"); ok=False
detached = sorted(models-used)
print(f"모델 파일 {len(models)}개, 이 리포 풋프린트가 참조 {len(used)}개")
if detached:
    print(f"  분리 모델 {len(detached)}개 (공식 풋프린트용, 3dmodels/MODELS.md 참고):")
    for d in detached: print(f"    {d}")
if nomodel: print(f"  !! model 블록 없는 풋프린트 {len(nomodel)}개: {nomodel}"); ok=False
print("\n결과:", "ALL OK" if ok else "문제 있음")
sys.exit(0 if ok else 1)
