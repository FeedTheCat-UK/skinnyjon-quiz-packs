# Skinny Jon Quiz Night — monthly question packs

The Quiz Night game (Skinny Jon Customs Entertainment Centre) checks this repo for new packs.
On the TV's setup screen the host taps **Check for new packs**, reviews every question
(untick anything wrong) and only then adds the pack. Nothing goes into a quiz unreviewed.

## Files
- `packs/index.json` — the list of packs, newest first.
- `packs/YYYY-MM.json` — one pack per month.
- `tools/validate.py` — run `python3 tools/validate.py` before pushing. It must print `OK`.

## index.json
```json
{"version":1,"packs":[{"id":"2026-11","title":"November 2026","file":"2026-11.json","count":240,"created":"2026-11-01"}]}
```

## Pack format
```json
{"id":"2026-11","title":"November 2026","created":"2026-11-01","covers":"October 2026",
 "questions":[
  {"cat":"news","type":"m","q":"Question?","a":"Right answer","w":["Wrong 1","Wrong 2","Wrong 3"],"source":"https://..."},
  {"cat":"news","type":"t","q":"A statement.","a":true,"source":"https://..."},
  {"cat":"sport","type":"n","q":"How many…?","a":42,"unit":"goals","source":"https://..."},
  {"cat":"news","type":"o","q":"Put these in order, earliest first","items":["First","Second","Third","Fourth"],"source":"https://..."}
 ]}
```
- `type`: `m` multiple choice (1 right + 3 wrong), `t` true/false (`a` is true/false),
  `n` nearest number (`a` is a number, `unit` optional), `o` put in order (`items` in the CORRECT order — the game shuffles them).
- `cat`: `news` (shows as "This Month"), or one of `gk history sport football geography science music filmtv fooddrink motoring`.
- `source`: a link that proves the answer. Every question needs one.
- Keep it UK-pub-quiz friendly: no politics-baiting, nothing grim or tragic as quiz fodder.
