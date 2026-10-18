#!/usr/bin/env python3
"""Checks packs/index.json and every pack file. Prints OK or a list of problems."""
import json, pathlib, sys, re
root=pathlib.Path(__file__).resolve().parent.parent/'packs'
CATS={'news','gk','history','sport','football','geography','science','music','filmtv','fooddrink','motoring'}
probs=[]
idx=json.loads((root/'index.json').read_text())
ids=set()
for p in idx.get('packs',[]):
    for k in ('id','title','file','count'):
        if k not in p: probs.append(f'index: pack missing {k}: {p}')
    f=root/p.get('file','')
    if not f.exists(): probs.append(f'index: file not found {f.name}'); continue
    if p['id'] in ids: probs.append(f'index: duplicate id {p["id"]}')
    ids.add(p['id'])
    pk=json.loads(f.read_text()); qs=pk.get('questions',[]); seen=set()
    if pk.get('id')!=p['id']: probs.append(f'{f.name}: id does not match index')
    if len(qs)!=p['count']: probs.append(f'{f.name}: index count {p["count"]} but file has {len(qs)}')
    for i,q in enumerate(qs):
        w=f'{f.name} #{i+1}'
        t=q.get('type'); text=(q.get('q') or '').strip()
        if not text: probs.append(f'{w}: no question text')
        if text.lower() in seen: probs.append(f'{w}: duplicate question')
        seen.add(text.lower())
        if q.get('cat') not in CATS: probs.append(f'{w}: bad cat {q.get("cat")}')
        if not re.match(r'^https?://',q.get('source') or ''): probs.append(f'{w}: needs a source link')
        if t=='m':
            ws=q.get('w') or []
            if not isinstance(q.get('a'),str) or len(ws)!=3 or len(set([q['a']]+ws))!=4: probs.append(f'{w}: multiple choice needs a + 3 different wrong answers')
            if any(len(x)>60 for x in [q.get('a','')]+ws): probs.append(f'{w}: an option is longer than 60 characters')
        elif t=='t':
            if not isinstance(q.get('a'),bool): probs.append(f'{w}: true/false answer must be true or false')
        elif t=='n':
            if not isinstance(q.get('a'),(int,float)): probs.append(f'{w}: number answer must be a number')
        elif t=='o':
            it=q.get('items') or []
            if len(it)!=4 or len(set(it))!=4: probs.append(f'{w}: order needs 4 different items')
        else: probs.append(f'{w}: bad type {t}')
        if len(text)>200: probs.append(f'{w}: question longer than 200 characters')
print('OK' if not probs else '\n'.join(probs))
sys.exit(1 if probs else 0)
