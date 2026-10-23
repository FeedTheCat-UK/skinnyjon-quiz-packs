#!/usr/bin/env python3
"""Checks media/pictures.json: required fields, 3 distinct wrong answers, every image file present."""
import json, pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent / 'media'
d = json.load(open(root / 'pictures.json')); bad = []; ids = set()
CATS = {'gk', 'history', 'sport', 'football', 'geography', 'science', 'music', 'filmtv', 'fooddrink', 'motoring'}
for q in d.get('pics', []):
    w = q.get('w', [])
    if q.get('id') in ids: bad.append(('duplicate id', q.get('id')))
    ids.add(q.get('id'))
    if q.get('cat') not in CATS: bad.append(('cat', q.get('id')))
    if len(w) != 3 or len(set(w + [q.get('a')])) != 4: bad.append(('options', q.get('id')))
    if q.get('fx', 'none') not in ('none', 'pix', 'zoom'): bad.append(('fx', q.get('id')))
    if not q.get('credit'): bad.append(('credit', q.get('id')))
    if not (root / q.get('img', '')).exists(): bad.append(('missing image', q.get('img')))
for b in d.get('balls', []):
    if b.get('id') in ids: bad.append(('duplicate id', b.get('id')))
    ids.add(b.get('id'))
    if not (0 <= b.get('bx', -1) <= 1 and 0 <= b.get('by', -1) <= 1): bad.append(('ball position', b.get('id')))
    if not b.get('credit'): bad.append(('credit', b.get('id')))
    if not (root / b.get('img', '')).exists(): bad.append(('missing image', b.get('img')))
for x in bad: print('PROBLEM', *x)
print('OK' if not bad else f'{len(bad)} problems', f"({len(d.get('pics', []))} pictures, {len(d.get('balls', []))} Spot the Ball)")
sys.exit(1 if bad else 0)
