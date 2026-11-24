"""Chatterbox narration renderer: renders every queue.jsonl entry missing from cache/ (one sentence per entry)."""
import sys, os, json, time, torch, torchaudio
sys.path.insert(0, '/home/claude/cbxwork')
torch.set_num_threads(2)
from cbx_load import load
D = '/home/claude/narr'
q = {}
for l in open(f'{D}/queue.jsonl'):
    x = json.loads(l); q[x['key']] = x
todo = [x for x in q.values() if not os.path.exists(f'{D}/cache/{x["key"]}.wav')]
todo.sort(key=lambda x: (x.get('order', 0), x['voice']))
todo = todo[:int(os.environ.get('BATCH', '12'))]   # the model's memory creeps up per take; restart often
print('todo', len(todo), flush=True)
m = load(); cur = None
for i, x in enumerate(todo):
    c = (x['voice'], x['ex'])
    if c != cur:
        m.prepare_conditionals(f'{D}/refs/{x["voice"]}.wav', exaggeration=x['ex']); cur = c
    t0 = time.time()
    torch.manual_seed(x.get('seed', 7))
    w = m.generate(x['text'], exaggeration=x['ex'], cfg_weight=x['cfg'], temperature=0.7)
    torchaudio.save(f'{D}/cache/{x["key"]}.tmp.wav', w, m.sr); os.replace(f'{D}/cache/{x["key"]}.tmp.wav', f'{D}/cache/{x["key"]}.wav')
    print(i + 1, len(todo), x['voice'], round(time.time() - t0, 1), round(w.shape[-1] / m.sr, 2), x['text'][:60], flush=True)
print('DONE', flush=True)
