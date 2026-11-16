#!/usr/bin/env python3
"""Regenerate recording assets from the script worker's SLIDES.json."""
import json, re
from pathlib import Path
root = Path(__file__).resolve().parents[1]
raw = json.loads((root / 'SLIDES.json').read_text())
assert 12 <= len(raw['slides']) <= 14
sources = {}
for key, value in raw['sources'].items():
    sources[key] = {'title': {'TOUR':'TOuR · method','REFIT':'ReFIT · method','TTT':'TTT-Embed · method','DISCO':'DISCo · coverage','FIQA':'FiQA · local report','H8':'HotpotQA H8 · local report','LEDGER':'Prior source ledger'}.get(key,key), 'url': value if value.startswith('https://') else 'SOURCE_LEDGER.md', 'locator': value if value.startswith('https://') else 'Local source record; see the source ledger.'}
slides=[]
for i, s in enumerate(raw['slides'], 1):
    narration = re.sub(r'^\[Pointer: (.*?)\]\s*', '', s['speaker_notes'], flags=re.S)
    pointer = re.match(r'^\[Pointer: (.*?)\]', s['speaker_notes'])
    refs = list(dict.fromkeys(x['id'] for x in s['source_refs']))
    if i == 13 and 'H8' not in refs: refs.append('H8')
    assert all(ref in sources for ref in refs)
    slides.append({'number':i,'id':f's{i:02}','kind':'recording','title':s['title'],'subtitle':s['subtitle'],'chapter':s['role'].title(),'evidence':s['role'].upper(),'takeaway':s['slide_bullets'][-1], 'items':s['slide_bullets'], 'pointers':[pointer.group(1)] if pointer else [], 'refs':refs,'notes':[{'id':f'S{i:02}.01','text':narration,'refs':refs}], 'wordCount':len(narration.split()),'secondsAt130Wpm':s['duration_seconds']})
assert sum(s['wordCount'] for s in slides) <= 1700
out={'meta':{'title':raw['title'],'team':'COEOUS','project':'COEOUS · IRE','task':'coeus-recording-20261116'},'sources':sources,'slides':slides}
text=json.dumps(out,ensure_ascii=False,indent=2)+'\n'
(root/'content.json').write_text(text)
(root/'content.js').write_text('window.DECK = '+text.rstrip()+';\n')
lines=['# COEOUS — recording script','','Estimated nine minutes with deliberate pacing and transitions.','']
for s in slides:
    lines += [f"## {s['number']:02}. {s['title']}",'',f"Target: {s['secondsAt130Wpm']} seconds.",'',s['notes'][0]['text'],'','Sources: '+', '.join(s['refs']),'']
(root/'PRESENTATION_SCRIPT.md').write_text('\n'.join(lines))
print(f"Built {len(slides)} slides, {sum(s['wordCount'] for s in slides)} spoken words, {sum(s['secondsAt130Wpm'] for s in slides)} seconds planned")
