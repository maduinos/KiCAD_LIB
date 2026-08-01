#!/usr/bin/env python3
"""라이브러리 무결성 검사.

  - 심볼/풋프린트 s-expression 괄호 균형
  - 풋프린트 파일명 == 내부 footprint 이름
  - 심볼의 Footprint 속성이 "라이브러리:이름" 형식이고 실제로 존재하는지
  - 모든 풋프린트가 (model ...) 를 갖고, 그 STEP 파일이 실재하며, 미사용 모델이 없는지

실행: python3 tools/check_library.py   (문제 있으면 exit 1)
"""
import pathlib, re, sys
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
for f in sorted((root/"symbols").glob("*.kicad_sym")):
    t=f.read_text()
    names=re.findall(r'\n  \(symbol "([^"]+)"',t)
    fps=re.findall(r'\(property "Footprint" "([^"]*)"',t)
    b=balanced(t); ok &= b
    print(f"{f.name}: 괄호={'OK' if b else 'FAIL'} 심볼={len(names)}")
    for n,fp in zip(names,fps): print(f"    {n:24s} -> {fp}")

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

print("\n== 심볼->풋프린트 링크 해석 ==")
for f in sorted((root/"symbols").glob("*.kicad_sym")):
    for n,fp in zip(re.findall(r'\n  \(symbol "([^"]+)"',f.read_text()),
                    re.findall(r'\(property "Footprint" "([^"]*)"',f.read_text())):
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
print(f"모델 파일 {len(models)}개, 참조된 것 {len(used)}개, 미사용 {sorted(models-used)}")
if nomodel: print(f"  !! model 블록 없는 풋프린트 {len(nomodel)}개: {nomodel}"); ok=False
print("\n결과:", "ALL OK" if ok else "문제 있음")
sys.exit(0 if ok else 1)
